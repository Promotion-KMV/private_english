from django import forms
from django.contrib.auth.password_validation import validate_password 
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth.forms import PasswordResetForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


from django.core.mail import EmailMultiAlternatives
from english.settings import *
from django.views import View
from django.template.loader import render_to_string


from english_teacher.models import *
from .views import *


class RegisterForm(forms.ModelForm):
    """Форма регистрации нового пользователя"""
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Пароль повторно', widget=forms.PasswordInput())

    MIN_LENGTH = 4

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'age', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError('Почта с таким адресом уже зарегестрированна')
        return email

    def clean_password1(self):
        password = self.data.get('password1')
        validate_password(password)
        if password != self.data.get('password2'):
            raise forms.ValidationError('Пароли не соврадают')
        return password

    def save(self, *args, **kwargs):
        user = super(RegisterForm, self).save(*args, **kwargs)
        user.set_password(self.cleaned_data["password1"])
        user.save()

        return user


class LoginForm(forms.Form):
    """Форма входа в аккаунт"""
    email = forms.CharField(label='Email', widget=forms.EmailInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        fields = ["email", "password"]

    def clean(self):
        email = self.cleaned_data.get("email").lower()
        password = self.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError(
                "Поле Email или Password заполнены не верно. Проверьте Caps Lock. Или смените язык ввода"
            )
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        return user


class BootstrapStylesMixin:
    field_names = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.field_names:
            for fieldname in self.field_names:
                self.fields[fieldname].widget.attrs = {'class': 'form-control'}

        else:
            raise ValidationError('The field_names must be set')


class MyPassResetForm(BootstrapStylesMixin, PasswordResetForm):
    field_names = ['email']


class MySetPassForm(BootstrapStylesMixin, SetPasswordForm):
    field_names = ['new_password1', 'new_password2']
