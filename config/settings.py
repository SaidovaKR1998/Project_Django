import os
from pathlib import Path
from dotenv import load_dotenv
from django.conf.global_settings import STATICFILES_DIRS

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = []

# ДОБАВЛЯЕМ ПРИЛОЖЕНИЕ USERS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog',
    'blog',
    'users',  # ← ДОБАВЛЯЕМ НОВОЕ ПРИЛОЖЕНИЕ
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ОБНОВЛЯЕМ TEMPLATES ДЛЯ ПРАВИЛЬНОЙ РАБОТЫ С ШАБЛОНАМИ
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← ДОБАВЛЯЕМ ЭТУ СТРОКУ
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'  # ← МЕНЯЕМ НА РУССКИЙ

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ⭐⭐⭐ ДОБАВЛЯЕМ НОВЫЕ НАСТРОЙКИ ДЛЯ АУТЕНТИФИКАЦИИ ⭐⭐⭐

# Указываем кастомную модель пользователя
AUTH_USER_MODEL = 'users.User'

# Настройки для аутентификации
LOGIN_REDIRECT_URL = '/'  # куда перенаправлять после входа
LOGOUT_REDIRECT_URL = '/'  # куда перенаправлять после выхода
LOGIN_URL = '/users/login/'  # куда перенаправлять неавторизованных пользователей

# Настройки для отправки email (для приветственных писем)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # для разработки
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = 'noreply@skystore.com'

# Для продакшена раскомментируйте и настройте:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.yandex.ru'
# EMAIL_PORT = 465
# EMAIL_USE_SSL = True
# EMAIL_HOST_USER = 'your_email@yandex.ru'
# EMAIL_HOST_PASSWORD = 'your_password'
