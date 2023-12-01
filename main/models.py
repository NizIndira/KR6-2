from django.db import models
from django.utils import timezone

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    """Модель для клиента сервиса рассылок"""

    client_name = models.CharField(max_length=30, verbose_name='имя')
    client_email = models.EmailField(max_length=100, verbose_name='email')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

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

    def get_status(self):
        now = timezone.now()
        if self.start_time < now < self.completion_time:
            self.status = "started"
        elif now > self.completion_time:
            self.status = "completed"
        self.save()
        return self.status

    def __str__(self):
        return f'{self.message}: {self.frequency}'

    class Meta:
        """Представление написания рассылки в админке"""

        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Log(models.Model):
    """Модель логов рассылки"""

    STATUS_CHOICE = (
        ("success", "Успешно"),
        ("failed", "Неуспешно"),
    )
    mailing = models.ForeignKey(Mailing, verbose_name='рассылка', on_delete=models.CASCADE)
    last_attempt = models.DateTimeField(verbose_name='время последней попытки')
    status = models.CharField(max_length=7, choices=STATUS_CHOICE, verbose_name='статус попытки')

    def __str__(self):
        return f'{self.mailing} ({self.last_attempt}) - {self.status}'

    class Meta:
        """Представление написания логов в админке"""

        verbose_name = 'лог'
        verbose_name_plural = 'логи'
