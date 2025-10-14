from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, UserLoginForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_welcome_email(user.email)
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.email}! Вы успешно зарегистрировались.')
            return redirect('catalog:home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.email}!')
            return redirect('catalog:home')
        else:
            messages.error(request, 'Неверная электронная почта или пароль.')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('catalog:home')


def send_welcome_email(email):
    subject = 'Добро пожаловать в SkyStore!'
    message = '''Добро пожаловать в SkyStore!

Благодарим вас за регистрацию в нашем интернет-магазине.
Теперь вам доступны все функции платформы.

С уважением,
Команда SkyStore'''

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Ошибка отправки письма: {e}")
