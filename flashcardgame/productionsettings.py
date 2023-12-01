import os
import secrets
from pathlib import Path

import dj_database_url
from pathlib import Path
import boto3


print("USING PRODUCTION SETTINGS   >:)")

"""
SETTINGS ADDED FROM HEROKU DOCS
"""
####################   B E G I N   ##########################
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    default=secrets.token_urlsafe(nbytes=64),
)


IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ

# SECURITY WARNING: don't run with debug turned on in production!
if not IS_HEROKU_APP:
    DEBUG = True


if IS_HEROKU_APP:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = []
######################## E N D  ##############################






# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

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


DEBUG = False



INSTALLED_APPS = [

    ##### H E R O K U    B U L L S H I T #######################
    "whitenoise.runserver_nostatic",
    ##### "serves static files my ass!  ##############"
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
    ##### H E R O K U    B U L L S H I T #######################
    "whitenoise.middleware.WhiteNoiseMiddleware",
    ##### "serves static files my ass!  ##############"
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



AUTH_USER_MODEL = 'flashcardgameapp.User_Profile'
#SCHEMA_NAME= os.environ.get('SCHEMA_NAME')
SCHEMA_NAME='flashcardgames'
DB_USER= os.environ.get('DB_USER')
DB_PASSWORD= os.environ.get('DB_PASSWORD')



########## H E R O K U    B U L L S H I T #############
if IS_HEROKU_APP:

    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        ),
    }

#######################################################
else:

    DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',#<- Defines the Mysql backend in django.
        'NAME': SCHEMA_NAME, #<--------- Name of schema in MySQL 
        'USER': DB_USER,     #<--------- User Name 
        'PASSWORD': DB_PASSWORD,  #<- Password
        'HOST': '127.0.0.1',  #<---------Stays 127.0.0.1 Unless you host your Mysql DB on a server.
        'PORT': '3306', #<----------------Port 3306 is the standard port for mysql
        'OPTIONS': {  
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
        }      
        
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

AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',

]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


############ H E R O K U    B U L L S H I T ##############

# Have to replace my real static path --> STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'flashcardgameapp')
# with this...
STATIC_ROOT= BASE_DIR /"staticfiles"
########################################################
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'flashcardgameapp', 'static','flashcardgameapp')]




print(f"STATIC FILES DIRS-{STATICFILES_DIRS}")
print(f"Static root is {STATIC_ROOT}")


########### H E R O K U    B U L L S H I T ####################
#STORAGES = {
#    # Enable WhiteNoise's GZip and Brotli compression of static assets:
#    # https://whitenoise.readthedocs.io/en/latest/django.html#add-compression-and-caching-support
#    "staticfiles": {
#        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#    },
#}
###############################################################


#Taking out the email info because I dont want heroku to throw a god damn fit.

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#EMAIL_HOST='smtp.gmail.com'
#EMAIL_PORT=587
#EMAIL_HOST_USER=os.environ.get('email')
#EMAIL_HOST_PASSWORD=os.environ.get('mailpass')
#EMAIL_USE_TLS= True
#EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'



