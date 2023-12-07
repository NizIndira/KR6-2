from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from main.forms import StyleFormMixin
from django import forms


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "phone", "country", "avatar", "password1", "password2"]


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "phone", "country", "avatar"]

    def __init__(self, *args, **kwargs):
        """Скрытие поля с паролем"""
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class PasswordForm(StyleFormMixin, forms.Form):
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data


class UserUpdateManagerForm(StyleFormMixin, UserChangeForm):
    """Форма у пользователей для менеджеров-модераторов сервиса"""

    class Meta:
        model = User
        fields = ["is_active"]

    def __init__(self, *args, **kwargs):
        """Скрытие поля с паролем"""

        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
