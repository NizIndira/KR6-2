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

    class Meta:
        model = Mailing
        fields = "__all__"


class ClientForm(StyleFormMixin, forms.ModelForm):
    """Класс для генерации формы создания клиентов-получателей рассылки"""

    class Meta:
        model = Client
        fields = "__all__"


class MessageForm(StyleFormMixin, forms.ModelForm):
    """Класс для генерации формы рассылочного сообщения"""

    class Meta:
        model = Message
        fields = "__all__"
