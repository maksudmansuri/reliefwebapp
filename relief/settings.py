"""
Django settings for relief project.
Generated by 'django-admin startproject' using Django 3.2.5.
For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path
from os import path, pardir
import django_heroku
# import django_heroku
import dj_database_url 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cq&8ek!(y7z)db8vek(ul2p37o_gd%^s_o^mj102l&)*k9+sds'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',   
    'radmin',
    'hospital',
    'doctor',
    'accounts.apps.AccoumtsConfig',
    'lab',
    'pharmacy',
    'front',
    'patient',
    'discount',
    'cart',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_multiple_model',
    'channels',
    'chat',
    'mathfilters',
    'django.contrib.humanize',
    'drf_yasg',
    'coreapi',
    'rest_framework_swagger',
    'django_filters',
    'storages',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'accounts.LoginCheckMiddleWare.LoginCheckMiddleWare',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]



ROOT_URLCONF = 'relief.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'chat.context_processors.headernotifications',
                'chat.context_processors.patientcancel',
                'patient.context_processors.basket',
                'radmin.context_processors.Badgeson',
                'radmin.context_processors.BadgeNewAppointment',
            ],
        }, 
    },
]
AUTH_USER_MODEL="accounts.CustomUser"

SITE_ID = 1 

TIME_INPUT_FORMATS = ('%H:%M',)

REST_FRAMWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly'
        'rest_framework.permissions.IsAuthenticated',
        #  'rest_framework.permissions.IsAdminUser'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'knox.auth.TokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'accounts.EmailBackEnd.EmailBackEnd',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',

        ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsSetPagination',
    'PAGE_SIZE':1,
    # 'REST_SESSION_LOGIN' : False
   
}
# WSGI_APPLICATION = 'relief.wsgi.application'

ASGI_APPLICATION = 'relief.asgi.application'

#for channels only
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

LOGIN_REDIRECT_URL = "/"

LOGIN_URL='dologin'
LOGOUT_URL = 'dologout'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
   'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE':'django.db.backends.mysql',
        'NAME':'medicalbd',
        'USER':'root',
        'PASSWORD':'Aot567@lk',
        'HOST':'localhost',
        'PORT':'3306'
    }
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'Token',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/





STATICFILE_STORAGE = "whitenoise.storage.CompressedMainfestStaticFilesStorage"

BASE_URL="http://127.0.0.1:8000"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_CONFIRMATION_PERIOD_DAYS = 1
SIMPLE_EMAIL_CONFIRMATION_PERIOD = timedelta(days=EMAIL_CONFIRMATION_PERIOD_DAYS)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'intellecttec@gmail.com'
EMAIL_HOST_PASSWORD ="bzsgrxiakqlxfqjz"
EMAIL_PORT = 587

STATIC_URL = '/static/'
MEDIA_URL = '/images/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_ROOT = BASE_DIR / 'static/images'
STATIC_ROOT = BASE_DIR / 'staticfiles'

REST_FRAMEWORK = {'DEFAULT_SCHEMA_CLASS':'rest_framework.schemas.coreapi.AutoSchema'} 
django_heroku.settings(locals())
# USE_S3 = os.getenv('USE_S3') == 'TRUE'
# if USE_S3:
AWS_ACCESS_KEY_ID = 'AKIAYKYQ6HVHTWX4OPWG'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'uniqueupgradebooking'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_QUERYSTRING_AUTH = False
# AWS_S3_ENDPOINT_URL = 'https://uniqueupgradebooking.s3.amazonaws.com'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_SIGNATURE_VERSION = 's3v4'
# AWS_S3_REGION_NAME = 'us-east-1'
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
AWS_LOCATION='static'
# AWS_QUERYSTRING_AUTH = False
# AWS_MEDIA_LOCATION='media'

# PUBLIC_MEDIA_LOCATION = 'media'
# MEDIA_ROOT = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN,AWS_MEDIA_LOCATION)
# AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'relief.storage.MediaStore' 
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' 
# else:    
# MEDIA_URL = "/media/"

# MEDIA_ROOT=os.path.join(BASE_DIR,"media")

STATIC_ROOT = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN,AWS_LOCATION)
# STATIC_ROOT=os.path.join(BASE_DIR,"static")
# STATIC_URL='/static/'
# print(STATIC_ROOT)
# print(STATIC_URL)
# print(MEDIA_ROOT)
# print(MEDIA_URL)

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "staticfiles"),      
# ]
# print(STATICFILES_DIRS)


