"""
Django settings for flashcards project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import boto3
import os
from pathlib import Path
import django_heroku
import dj_database_url
from decouple import config
import boto3
import dj_database_url
import psycopg2

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print("------------------------PRODUCTION SETTINGS TRIGGERED---------------------")



SECRET_KEY = os.environ["SECRET_KEY"]

##############A M A Z O N   M E D I A   P A T H S###################
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')            #
AWS_SECRET_ACCESS_KEY =os.environ.get('AWS_SECRET_ACCESS_KEY')     #
AWS_STORAGE_BUCKET_NAME =os.environ.get('S3_BUCKET')               #
CLOUDFRONT_URL = 'https://d17usxoyp786nd.cloudfront.net/'          #
DJANGO_STATIC = True                                               #
DJANGO_STATIC_FILE_PROXY = 'cloudfront.file_proxy'                 #
COMPRESS_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
COMPRESS_ENABLED= True
COMPRESS_URL= CLOUDFRONT_URL
STATIC_URL = '/static/'
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' <---ACTIVATE this when going to deployment
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = CLOUDFRONT_URL
CLOUDFRONT_PUB_KEY=os.getenv('CLOUDFRONT_PUB')
CLOUDFRONT_SECRET=os.getenv('CLOUDFRONT_SECRET')
AWS_DEFAULT_ACL='public-read'
AWS_S3_CUSTOM_DOMAIN = CLOUDFRONT_URL                              #
####################################################################


CSRF_COOKIE_SECURE=True

SESSION_COOKIE_SECURE=True
DEBUG = False


print("!!!!!!!!!!!!!!!!!!!!!!!!!allowed host BEFORE!!!!!!!!!!!!!")

ALLOWED_HOSTS = ['*',]


print("!!!!!!!!!!!!!!!!!!!!!!!!!allowed host AFTER !!!!!!!!!!!!!")

django_heroku.settings(locals())



# Application definition

INSTALLED_APPS = [
     "whitenoise.runserver_nostatic",
    'flashcardgameapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    
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



ROOT_URLCONF = 'flashcardgameapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'flashcardgameapp', 'templates', 'flashcardgameapp')],
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

WSGI_APPLICATION = 'flashcardgame.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

AUTH_USER_MODEL = 'flashcardgameapp.User_Profile'
#SCHEMA_NAME= os.environ.get('SCHEMA_NAME')
SCHEMA_NAME='flashcardgames'
DB_USER= os.environ.get('DB_USER')
DB_PASSWORD= os.environ.get('DB_PASSWORD')


#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#SECURE_SSL_REDIRECT = True



DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        } 
    }



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',

]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'flashcardgameapp', 'static','flashcardgameapp')]


STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "static/"


STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'flashcardgameapp')


print(f"STATIC FILES DIRS-{STATICFILES_DIRS}")
print(f"Static root is {STATIC_ROOT}")

STORAGES = {
    # Enable WhiteNoise's GZip and Brotli compression of static assets:
    # https://whitenoise.readthedocs.io/en/latest/django.html#add-compression-and-caching-support
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
WHITENOISE_KEEP_ONLY_HASHED_FILES = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER=os.environ.get('email')
EMAIL_HOST_PASSWORD=os.environ.get('mailpass')
EMAIL_USE_TLS= True
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'



