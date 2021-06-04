from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.http import response, HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import SetPasswordForm

from django.contrib.auth import authenticate, login
from account.forms import *

from django.core.mail import EmailMultiAlternatives
# from english.settings import * #1
from django.views import View
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator, delete_user_is_not_activate
from django.template.loader import render_to_string
from english.settings import *
from smtplib import  SMTPAuthenticationError


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        email = request.POST.get('email').lower()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        age = int(request.POST.get('age'))
        if CustomUser.objects.filter(email=request.POST.get('email')).exists() or \
            CustomUser.objects.filter(email__iexact=request.POST.get('email')):
            messages.error(request, message='Пользователь с таким адресом' + 
                            ' электронной почты уже существует')
            form = RegisterForm()
            return render(request, 'register/register.html', {'form': form})
        if password1 != password2:
            messages.error(request, message='Пароли не совпадают')
            form = RegisterForm()
            return render(request, 'register/register.html', {'form': form})
        if len(password1) < 8:
            messages.error(request, message='слишком короткий пароль минимум 8 символов')
            form = RegisterForm()
            return render(request, 'register/register.html', {'form': form}) 
        if 100 < age > 1:
            messages.error(request, message='Вы указали невозможный возраст')
            form = RegisterForm()
            return render(request, 'register/register.html', {'form': form})      
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            user = form.save()
            user.is_active = False
            user.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('account:activate', kwargs={
                                    'uidb64': uidb64,
                                    'token': token_generator.make_token(user)})
            activate_url = 'https://privatenglishtutor.ru/'+link
            data = {
                'activate_url': activate_url,
            }
            html_body = render_to_string('email/email_body.html', {'activate_url': activate_url})
            email_subject = 'Активация аккаунта'
            email = EmailMultiAlternatives(
                email_subject,
                html_body,
                EMAIL_HOST_USER,
                [user.email],
            )
            email.attach_alternative(html_body, "text/html")
            # email.send()
            try:
                email.send()
                message = messages.success(request, message='Регистрация прошла ' +
                'успешно. Для активации аккаунта пройдите по ссылке отправленной на' + 
                ' указанную вами почту.В случе отсутствия письма проверьте папку спан.')
                return HttpResponseRedirect(reverse_lazy('account:login', message))
            except SMTPAuthenticationError:
                print('error')
                message = messages.error(request, message='Ошибка сервера обратитесь к преподавателю')
                return HttpResponseRedirect(reverse_lazy('account:login', message))
            else:
                message = messages.error(request, message='Ошибка сервера обратитесь к преподавателю')
                return HttpResponseRedirect(reverse_lazy('account:login', message))

    else:
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'register/register.html', {'form': form})
    return render(request, 'register/register.html', {'form': form})


class ResetPasswordView(PasswordResetView):
    template_name = 'register/password_reset_form.html'
    form_class = MyPassResetForm
    email_template_name = 'email/password_reset_email.html'
    html_email_template_name = 'email/password_reset_email.html'
    subject_template_name = 'register/subject_theme.txt'
    success_url = reverse_lazy('account:password_reset_done')

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            if CustomUser.objects.filter(email=request.POST.get('email')).exists() and \
                CustomUser.objects.get(email__iexact=request.POST.get('email')).is_active == True:
                return super().dispatch(request, *args, **kwargs)
            elif CustomUser.objects.filter(email=request.POST.get('email')).exists() and \
                CustomUser.objects.get(email__iexact=request.POST.get('email')).is_active == False:
                user = CustomUser.objects.get(email__iexact=request.POST.get('email'))
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                user_profile = CustomUser()
                link = reverse('account:activate', kwargs={
                                        'uidb64': uidb64,
                                        'token': token_generator.make_token(user)})
                activate_url = 'http://'+domain+link
                data = {
                    'activate_url': activate_url,
                }
                html_body = render_to_string('email/email_body.html', {'activate_url': activate_url})
                email_subject = 'Активация аккаунта'
                email = EmailMultiAlternatives(
                    email_subject,
                    html_body,
                    EMAIL_HOST_USER,
                    [user.email],
                )
                email.attach_alternative(html_body, "text/html")
                email.send()
                message = messages.success(request, message='Ваш адрес электронной почты' +
                ' не был активирован.Для активации вашего аккаунта пройдите по ссылке отправленной' + 
                ' на указанную вами почту.')
                return HttpResponseRedirect(reverse_lazy('account:login', message))
            else:
                message = messages.error(request, message='Вы пытались отправить ' +
                'сообщение на незарегестрированный адрес электронной почты.' + 
                'Пройдите регистрацию или введите зарегестрированный адрес.')
                return HttpResponseRedirect(reverse_lazy('account:login', message))
        return super().dispatch(request, *args, **kwargs)


class ResetPasswordDoneView(PasswordResetDoneView):
    template_name = 'register/password_reset_done.html'
    success_url = reverse_lazy('account:password_reset_complete')


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'register/password_reset_confirm.html'
    # form_class = MySetPassForm
    success_url = reverse_lazy('account:password_reset_complete')


class ResetPasswordCompleteView(PasswordResetCompleteView):
    template_name = 'register/password_reset_complete.html'
    # form_class = MyPassResetForm


class VerificationView(View):
    """Отправка токена"""
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=id)
            if not token_generator.check_token(user, token):
                return render(request, 'email/error_link.html')
            if user.is_active:
                return redirect('account:login')
            user.is_active = True
            user.save()
            # message.success(request, 'Аккаунт активирован')
            return redirect('account:login')
        except Exception as ex:
            pass
        return redirect('account:login')


def user_login(request):
    """Вход в аккаунт"""
    template_name = 'register/login.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            email = cleaned_data['email'].lower()
            password = cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user.is_staff:
                delete_user_is_not_activate()
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse_lazy('english_teacher:main_info'))
                else:
                    return HttpResponse("Пользователь не зарегестрирован")
            else:
                form = LoginForm()
                messages.error(request, message='Такого пользователя не существует')
                return render(request, template_name, {'form': form})
    else:
        form = LoginForm()
    return render(request, template_name, {'form': form})


class CustomLogoutView(LogoutView):
    """Выход из аккаунта"""
    template_name = 'register/logout.html'