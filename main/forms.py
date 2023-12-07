from django import forms

from main.models import Mailing, Client, Message


class StyleFormMixin:
    """Класс-миксин для стилизации форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_active":
                field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    """Класс для генерации формы создания рассылки"""

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)
        # Добавляем поле с клиентами из модели клиентов и фильтруем только своих клиентов
        self.fields['clients'].queryset = self.fields['clients'].queryset.filter(owner=owner)
        # Добавляем поле с сообщениями из модели сообщений и фильтруем только свои сообщения
        self.fields['message'].queryset = Message.objects.filter(owner=owner)
        # Предлагаем к показу выбора только тему сообщения
        choices = [(message.id, message.message_subject) for message in self.fields['message'].queryset]
        self.fields['message'].widget = forms.Select(
            choices=[('', '--------')] + choices,  # Добавляем пустой элемент в список выбора
            attrs={'class': 'form-control'}
        )

    class Meta:
        model = Mailing
        exclude = ('owner', 'last_sent')


class MailingUpdateManagerForm(StyleFormMixin, forms.ModelForm):
    """Форма у рассылки для менеджеров-модераторов сервиса"""

    class Meta:
        model = Mailing
        fields = ["is_active"]


class ClientForm(StyleFormMixin, forms.ModelForm):
    """Класс для генерации формы создания клиентов-получателей рассылки"""

    class Meta:
        model = Client
        exclude = ('owner',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    """Класс для генерации формы рассылочного сообщения"""

    class Meta:
        model = Message
        exclude = ('owner',)
