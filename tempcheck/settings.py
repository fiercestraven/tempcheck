"""
Django settings for tempcheck project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kma66lvr0y#_+7rcwlbpgdk-v5*s(8djf1=tg=hw*j2f%b#)x9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
# cors: https://stackoverflow.com/questions/35760943/how-can-i-enable-cors-on-django-rest-framework
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'corsheaders',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    # https://stackoverflow.com/questions/56711082/reverse-django-admin-urls
    'django_extensions',
    'tcapp.apps.TcappConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# fv - add vercel or fly or whatever here when deploying
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
]

ROOT_URLCONF = 'tempcheck.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'tcreact/build'], 
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

WSGI_APPLICATION = 'tempcheck.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "tempcheck",
        "USER": "admin_fv",
        "PASSWORD": "woo.donor.toolkit",
        "HOST": "localhost",
        "PORT": "",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Belfast'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# from https://medium.com/@meric.emmanuel/how-to-connect-django-with-create-react-app-d1581139cad1
STATIC_URL = 'static/'
STATIC_ROOT = '.static'
STATICFILES_DIRS = [
    'tcreact/build/'
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = "/tcapp/accounts/login/"
LOGIN_REDIRECT_URL = "/tcapp/lectures/"
LOGOUT_REDIRECT_URL = "/admin/"

# See: https://github.com/iMerica/dj-rest-auth/blob/master/demo/demo/settings.py
REST_SESSION_LOGIN = True
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'optional'

# See: https://dj-rest-auth.readthedocs.io/en/latest/installation.html
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'tcapp-auth'

REST_FRAMEWORK = {
    # fv - uncomment the permission and pagination classes after setting up authentication w next.js
    # Use Django's standard `django.contrib.auth` permissions, or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # fv - added this per dj-rest-auth docs; not sure if the session one will break anythihng
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # fv - check this!! is this going to be a problem if a student is in and React can't access their modules?
        # let only staff view the api: https://www.django-rest-framework.org/api-guide/permissions/
        'rest_framework.permissions.IsAdminUser',
    ],
}

# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#access-token-lifetime
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=300),
}

# fv - per https://github.com/iMerica/dj-rest-auth/blob/master/demo/demo/settings.py, not sure if needed?
SWAGGER_SETTINGS = {
    'LOGIN_URL': 'login',
    'LOGOUT_URL': 'logout',
}

# fv - hope to remove later? or at least change to localhost:8000 + deployment
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# fv - not sure if needed; per https://github.com/iMerica/dj-rest-auth/blob/master/demo/demo/settings.py
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'