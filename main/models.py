import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone

from main.email_sender import send_mail_task

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    """Модель для клиента сервиса рассылок"""

    client_name = models.CharField(max_length=30, verbose_name='имя')
    client_email = models.EmailField(unique=True, verbose_name='email')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    # Зависимость от владельца клиента
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец клиента',
                              **NULLABLE)

    def __str__(self):
        return f'{self.client_name}, {self.client_email}'

    class Meta:
        """Представление написания заголовков для клиента в админке"""

        verbose_name = "клиент"
        verbose_name_plural = "клиенты"


class Message(models.Model):
    """Модель рассылочного сообщения"""

    message_subject = models.CharField(max_length=180, verbose_name='тема письма')
    message_text = models.TextField(verbose_name='cообщение')
    # Зависимость от владельца сообщения
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец сообщения',
                              **NULLABLE)

    def __str__(self):
        return f'{self.message_subject}, {self.message_text}'

    class Meta:
        """Представление написания заголовков для письма в админке"""

        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"


class Mailing(models.Model):
    """Модель рассылки"""

    FREQUENCY_CHOICE = (
        ("daily", "ежедневно"),
        ("weekly", "еженедельно"),
        ("monthly", "ежемесячно"),
    )

    STATUS_CHOICE = (
        ("created", "Создана"),
        ("completed", "Завершена"),
        ("started", "Запущена"),
    )

    start_time = models.DateTimeField(verbose_name='старт рассылки')
    completion_time = models.DateTimeField(verbose_name='завершение рассылки')
    frequency = models.CharField(max_length=30, choices=FREQUENCY_CHOICE, default='daily',
                                 verbose_name='периодичность')
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='created', verbose_name='статус')
    message = models.ForeignKey(Message, verbose_name='сообщение', on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, verbose_name='клиенты')
    is_active = models.BooleanField(default=True, verbose_name='статус активности')
    last_sent = models.DateTimeField(verbose_name='последняя отправка', **NULLABLE)
    # Зависимость от владельца рассылки
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец рассылки',
                              **NULLABLE)

    def get_status(self):
        """ Метод для получения статуса рассылки """

        return self.status

    @classmethod
    def get_objects_for_send(cls):
        """ Возвращает список рассылок для отправки """

        now = timezone.now()
        objects_list = []

        for m in cls.objects.all():
            # Условие, если нет даты последней отправки,
            # или с даты последней отправки прошло больше одного дня, больше 7 дней, больше 30 дней
            is_daily_valid = not m.last_sent or m.last_sent <= now - datetime.timedelta(days=1)
            is_weekly_valid = not m.last_sent or m.last_sent <= now - datetime.timedelta(days=7)
            is_monthly_valid = not m.last_sent or m.last_sent <= now - datetime.timedelta(days=30)

            if all([
                # время и дата окончания больше или равно текущему времени
                m.frequency == 'daily',
                # last_sended должен быть вчерашним днем
                is_daily_valid,
                # статус должен быть либо created либо completed
                m.status in ['created', 'completed'],
                # время начала меньше или равно текущему времени
                m.start_time.time() < now.time(),
                # время и дата  начала меньше или равно текущему времени
                m.start_time < now,
                # время и дата окончания больше или равно текущему времени
                now < m.completion_time
            ]):
                objects_list.append(m)

            elif all([
                # время и дата окончания больше или равно текущему времени
                m.frequency == 'weekly',
                # last_sended должен быть меньше на 7 дней, чем текущая дата
                is_weekly_valid,
                # статус должен быть либо created либо completed
                m.status in ['created', 'completed'],
                # время начала меньше или равно текущему времени
                m.start_time.time() < now.time(),
                # время и дата  начала меньше или равно текущему времени
                m.start_time < now,
                # время и дата окончания больше или равно текущему времени
                now < m.completion_time
            ]):
                objects_list.append(m)

            elif all([
                # время и дата окончания больше или равно текущему времени
                m.frequency == 'monthly',
                # last_sended должен быть меньше на 30 дней, чем текущая дата
                is_monthly_valid,
                # статус должен быть либо created либо completed
                m.status in ['created', 'completed'],
                # время начала меньше или равно текущему времени
                m.start_time.time() < now.time(),
                # время и дата  начала меньше или равно текущему времени
                m.start_time < now,
                # время и дата окончания больше или равно текущему времени
                now < m.completion_time
            ]):
                objects_list.append(m)

        return objects_list

    def send(self):
        """  Отправляет рассылку  """

        self.status = "started"
        self.save()

        # Получение всех клиентов рассылки
        clients = self.clients.all()

        # Отправка сообщения каждому клиенту
        subject = self.message.message_subject
        message = self.message.message_text

        recipient_list = []
        for client in clients:
            recipient_list.append(client.client_email)

        try:
            count = send_mail_task(subject, message, recipient_list)
        except Exception as e:
            Log.objects.create(
                mailing=self,
                last_attempt=timezone.now(),
                status="failed",
                message=f"Не удалось отправить сообщение. Ошибка: {e}"
            )
        else:
            Log.objects.create(
                mailing=self,
                last_attempt=timezone.now(),
                status="success",
                message=f"Сообщений отправлено: {count}<br>"
                        f"Получателей рассылки: {len(recipient_list)}"
            )

        # Меняем текущий статус на completed и сохраняем текущее время отправки в last_sent
        self.status = 'completed'
        self.last_sent = timezone.now()
        self.save()


    def __str__(self):
        return f'{self.message}: {self.frequency}'

    class Meta:
        """Представление написания рассылки в админке"""

        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ('can_manager_view', 'Разрешение для менеджера на просмотр рассылки'),
        ]


class Log(models.Model):
    """Модель логов рассылки"""

    STATUS_CHOICE = (
        ("success", "Успешно"),
        ("failed", "Неуспешно"),
    )
    mailing = models.ForeignKey(Mailing, verbose_name='рассылка', on_delete=models.CASCADE)
    last_attempt = models.DateTimeField(verbose_name='время последней попытки')
    status = models.CharField(max_length=7, choices=STATUS_CHOICE, verbose_name='статус попытки')
    message = models.CharField(max_length=200, verbose_name='сообщение', **NULLABLE)

    def __str__(self):
        return f'{self.mailing} ({self.last_attempt}) - {self.status}'

    class Meta:
        """Представление написания логов в админке"""

        verbose_name = 'лог'
        verbose_name_plural = 'логи'
