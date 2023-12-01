# Generated by Django 4.2.7 on 2023-11-30 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=30, verbose_name='имя')),
                ('client_email', models.EmailField(max_length=100, verbose_name='email')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='комментарий')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_subject', models.CharField(max_length=180, verbose_name='тема письма')),
                ('message_text', models.TextField(verbose_name='cообщение')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'сообщения',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='старт рассылки')),
                ('completion_time', models.DateTimeField(verbose_name='завершение рассылки')),
                ('frequency', models.CharField(choices=[('daily', 'ежедневно'), ('weekly', 'еженедельно'), ('monthly', 'ежемесячно')], default='daily', max_length=30, verbose_name='периодичность')),
                ('status', models.CharField(choices=[('created', 'Создана'), ('completed', 'Завершена'), ('started', 'Запущена')], default='created', max_length=20, verbose_name='статус')),
                ('is_active', models.BooleanField(default=True, verbose_name='статус активности')),
                ('clients', models.ManyToManyField(to='main.client', verbose_name='клиенты')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.message', verbose_name='сообщение')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_attempt', models.DateTimeField(verbose_name='время последней попытки')),
                ('status', models.CharField(choices=[('success', 'Успешно'), ('failed', 'Неуспешно')], max_length=7, verbose_name='статус попытки')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.mailing', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'лог',
                'verbose_name_plural': 'логи',
            },
        ),
    ]