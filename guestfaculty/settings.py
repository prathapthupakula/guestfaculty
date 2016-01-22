"""
Django settings for guestfaculty project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pc!e_kw^9$heli$5-z0x#q6&kk$(vu(w8k$^jq*rm$(fb$-0z-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'admin_report',
    'facultyapp',
    'gfplan',
    'timetable',
    'reports',	
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'django.contrib.sites',
	'allauth',
	'allauth.account',	
	#'allauth.socialaccount',
    'import_export',
    'django_object_actions',
    'flat',
)

# Settings for AllAuth Application for Signup
SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_USERNAME_REQUIRED=False
LOGIN_REDIRECT_URL = "/application"


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
)

ROOT_URLCONF = 'guestfaculty.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
				'django.core.context_processors.request',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    #'django.contrib.auth.backends.RemoteUserBackend',
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'guestfaculty.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


DATABASES = {
 'default': { 
        'ENGINE': 'mysql.connector.django', 
        'NAME': 'gfaculty',                     
        'USER': 'gfuser',
        'PASSWORD': 'gfuser123',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = False

USE_L10N = False

USE_TZ = False

#MEDIA_URL = "http://192.168.1.177/django/guestfaculty/"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'local_static')

#TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\','/'),)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'reporting@varnatech.com'
EMAIL_HOST_PASSWORD = '$epo1234'
EMAIL_USE_SSL = True

#DEFAULT_FROM_EMAIL = 'noreply@wilp.bits-pilani.ac.in'
#EMAIL_HOST = 'server.trendmaxi.com'
#EMAIL_PORT = 587
#EMAIL_HOST_USER = 'brilamail@trendmaxi.com'
#EMAIL_HOST_PASSWORD = 'kvn_456Bits'
#EMAIL_USE_TLS = True

DATE_FORMAT = 'N j, Y'

#ldap server details
LDAP_SERVER = 'ldap://172.22.2.87/'
LDAP_BASE_DN = 'ou=people,dc=bits-pilani,dc=ac,dc=in'

#CUSTOM
APPLICATION_URL = 'http://gf-varnatech.ka-sites.space/application/'

try:
    from local_settings import *
except:
    pass

