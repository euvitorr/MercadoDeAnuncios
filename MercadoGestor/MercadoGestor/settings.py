import os

from decouple import Csv, config
from dj_database_url import parse as dburl
from django.contrib import messages
from django.shortcuts import resolve_url
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
# SECRET_KEY = 'q)mb%7m#peqf359_314y4!8-#j1taz3*f!ce0h#5o#qq57)czr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*', 'localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    # default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    # apps
    'users',
    'core',
    'subscribe',
    'integration',
    'products',

    # thrid apps
    'storages',
    'widget_tweaks',
    'admin_reorder',
    'embed_video',
    "django_extensions",
    # social apps
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',

    # the social providers
    # 'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'admin_reorder.middleware.ModelAdminReorder',

]


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
)

ROOT_URLCONF = 'MercadoGestor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'templates', 'allauth')],
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

WSGI_APPLICATION = 'MercadoGestor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

default_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': config('DATABASE_URL', default=default_url, cast=dburl),

}


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


USE_S3 = config('USE_S3', cast=bool, default=False)

if USE_S3:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'static'
    AWS_DEFAULT_ACL = None

    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    STATICFILES_STORAGE = 'MercadoGestor.storage_backends.StaticStorage'

    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'MercadoGestor.storage_backends.PublicMediaStorage'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/static'),
]

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Email Configuration
SENDGRID_API_KEY = config('SENDGRID_API_KEY')
EMAIL_BACKEND = config('EMAIL_BACKEND')
DEFAULT_FROM_MAIL = config('DEFAULT_FROM_MAIL')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY


SITE_ID = config("SITE_ID", cast=int, default=1)
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'users:profile'
AUTH_USER_MODEL = 'users.User'
LOGOUT_REDIRECT_URL = '/'

# social auth
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7

# allauth forms
ACCOUNT_FORMS = {
    'login': 'allauth.account.forms.LoginForm',
    'signup': 'users.forms.SignUpForm',
    'add_email': 'allauth.account.forms.AddEmailForm',
    'change_password': 'allauth.account.forms.ChangePasswordForm',
    'set_password': 'allauth.account.forms.SetPasswordForm',
    'reset_password': 'allauth.account.forms.ResetPasswordForm',
    'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
    'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
}


if DEBUG:
    INTERNAL_IPS = config('INTERNAL_IPS', default='127.0.0.1', cast=Csv())



ADMIN_REORDER = (
    {
        'app': 'integration',
        'label': 'Integrações',
        'models': (
            'integration.ValidML',
        )
    },
    {
        'app': 'products',
        'label': 'Produtos',
        'models': (
            'products.Product',
            'products.ProductLink',
        )
    },
    {
        'app': 'core',
        'label': 'Questionários',
        'models': (
            "core.Question", "core.QuestionCategory",
        )
    },
    {
        'app': 'subscribe',
        'label': 'Inscrições',
        'models': (
            'subscribe.Contacts', 'subscribe.Subscribe',
        )
    },
        {
        'app': 'users',
        'label': 'Usuários',
        'models': (
            'users.User','users.Address'
        )
    },

)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d: %(message)s'
        },
        'simple': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
        'MercadoGestor': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
