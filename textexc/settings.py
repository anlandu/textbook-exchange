import os
import django_heroku
import psycopg2

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bzlj_!^o$51mc-3zb^xg87$0u=ygwuo*(+(57fk1^=0w4zs#j-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# OAUTH 2 ID and Secret: keep this private
CLIENT_ID = '926789688582-6hj6sj5kcquk9o6hc4proqh9p266v6mj.apps.googleusercontent.com'
CLIENT_SECRET = 'VKJy7twp3ZHgG8wUoGFxv3yx'

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'textbook_exchange.apps.TextbookExchangeConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'payments',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]
#Set-up for Django-Private-Chat
#Link: https://django-private-chat.readthedocs.io/en/latest/readme.html

CHAT_WS_SERVER_HOST = 'localhost'
CHAT_WS_SERVER_PORT = 5002
CHAT_WS_SERVER_PROTOCOL = 'ws'
DATETIME_FORMAT = "d.m.Y H:i:s"

AUTH_USER_MODEL = 'textbook_exchange.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'textexc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'textexc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'project_103_pineapple_seals', #stored in project directory
        'USER': 'pineappleseals_admin',
        'PASSWORD': 'pineappleseals',
        'HOST': '', #default = 127.0.0.1
        'PORT': '', #default = 5432
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

SITE_ID = 1

# Images
# https://matthiasomisore.com/web-programming/display-image-in-a-django-template-using-imagefield/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# ALL AUTH CONFIG
ACCOUNT_LOGOUT_REDIRECT_URL ='/'
LOGIN_REDIRECT_URL = '/login/redirect/'
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '926789688582-6hj6sj5kcquk9o6hc4proqh9p266v6mj.apps.googleusercontent.com',
            'secret': 'VKJy7twp3ZHgG8wUoGFxv3yx',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
    }
}

#Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'pineappleseals@gmail.com'
EMAIL_HOST_PASSWORD = 'Sherriff2020!'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
ADMINS = [('Pineapple Seals Admin', 'pineappleseals@gmail.com')]

TWILIO_ACCT_SID='ACf0385517838b0c0e46062e41663cd6c8'
TWILIO_AUTH_TOKEN='85d5a9285958fda0dbac2fded8f6b4f8'
TWILIO_CHAT_SID='IS8bf9f457e4224899919366c2902f6835' #change
TWILIO_SYNC_SID='IS7086992d661eb157e6b5149543febb51'
TWILIO_API_SID='SK9c7fe6717da5318751e61ca951dd784e'
TWILIO_API_SECRET='YP8YzQNQw8K1VM9bgiFlezje0MckJenx'

STATIC_ROOT = os.path.join(BASE_DIR, 'textbook_exchange/static/textbook_exchange/')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'textbook_exchange/static/textbook_exchange/'),)
django_heroku.settings(locals())
