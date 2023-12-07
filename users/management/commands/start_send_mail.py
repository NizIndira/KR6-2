from django.core.management import BaseCommand
from main.services import send_mailing_task


class Command(BaseCommand):
    """Класс для отправки сообщений через командную строку"""

    def handle(self, *args, **options):
        send_mailing_task()