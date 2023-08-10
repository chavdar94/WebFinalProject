from django.urls import reverse_lazy
from pathlib import Path
import os

from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', None)

DEBUG = bool(int(os.getenv('DEBUG', 1)))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split()

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.core',
    'apps.forum',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.NoDjangoAdminForEndUserMiddleware',
]

ROOT_URLCONF = 'dev_forum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.background.background_image',
            ],
        },
    },
]

WSGI_APPLICATION = 'dev_forum.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv('DB_NAME', None),
        "USER": os.getenv('DB_USER', None),
        "PASSWORD": os.getenv('DB_PASSWORD', None),
        "HOST": os.getenv('DB_HOST', None),
        "PORT": os.getenv('DB_PORT', None),
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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static_files'
]

STATIC_ROOT = os.getenv('STATIC_ROOT', BASE_DIR / 'staticfiles')

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

FILE_UPLOAD_PERMISSIONS = 0o644

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core.AppUser'

LOGIN_URL = reverse_lazy('sign-in')
LOGIN_REDIRECT_URL = reverse_lazy('home')

LOGOUT_REDIRECT_URL = reverse_lazy('home')

# Social logins
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    },
}
ACCOUNT_FORMS = {
    'login': 'WebFinalExam.base.forms.SignInForm',
    'signup': 'WebFinalExam.base.forms.RegisterForm'
}
# Fixes `username` error when using custom User with no `username` field
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# SMTP configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', None)
EMAIL_PORT = os.getenv('EMAIL_PORT', None)
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', False)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', None)

# INTERNAL_IPS = [
#     '127.0.0.1',
# ]


# Jet themes
# more themes and customization here https://jet.readthedocs.io/en/latest/config_file.html#jet-themes
JET_THEMES = [
    {
        'theme': 'default',  # theme folder name
        'color': '#47bac1',  # color of the theme's button in user menu
        'title': 'Default'  # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',  # Set the desired log level here (INFO, DEBUG, etc.)
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            # Set the desired log level here (INFO, DEBUG, etc.)
            'level': 'INFO',
            'propagate': False,
        },
    },
}
