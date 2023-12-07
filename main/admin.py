from django.contrib import admin

from main.models import Client, Message, Mailing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Представление раздела - "Клиенты" в админке"""

    list_display = ('client_name', 'client_email', 'comment')
    search_fields = ('client_name', 'client_email', 'comment',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Представление раздела - "Сообщения" в админке"""

    list_display = ('message_subject', 'message_text')
    search_fields = ('message_subject', 'message_text',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Представление раздела - "Рассылка" в админке"""

    list_display = ('id', 'is_active', 'start_time', 'completion_time', 'frequency', 'status', 'message')
    search_fields = ('start_time', 'completion_time', 'frequency', 'status', 'message', 'is_active',)
