import os
import tempfile

import environ
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

env = environ.Env(DEBUG=(bool, False))

try:
    environ.Env.read_env(env.str('ENV_PATH', '.env'))
except:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

SECRET_KEY = env('MCE_SECRET_KEY', default='fa(=utzixi05twa3j*v$eaccuyq)!-_c-8=sr#hih^7i&xcw)^')

DEBUG = env('MCE_DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = [
    '127.0.0.1',
    '192.168.56.1',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    'django_select2',
    'django_filters',
    'django_extensions',
    'daterangefilter',

    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_yasg',
    'corsheaders',

    'formtools',
    'taggit',
    'mptt',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',

    "mce_django_app.apps.MceAppConfig",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

ROOT_URLCONF = 'project_test.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [
        #     os.path.join(BASE_DIR, 'templates'),
        #],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            #'loaders': [
            #    ('django.template.loaders.cached.Loader', [
            #        'django.template.loaders.filesystem.Loader',
            #        'django.template.loaders.app_directories.Loader',
            #    ])
            #],
        },
    },
]

WSGI_APPLICATION = 'project_test.wsgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

DATABASES = {
    'default': env.db(default='sqlite:////tmp/mce-django-app-test-sqlite.db'),
}

AUTH_USER_MODEL = 'mce_django_app.User'

#LOGIN_URL = 'admin:login'
#LOGIN_URL = '/accounts/login/'
#LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    #"allauth.account.auth_backends.AuthenticationBackend",
    #'guardian.backends.ObjectPermissionBackend',
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # 'OPTIONS': {
        #     'min_length': 9,
        # }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LOCALE_PATHS = ( os.path.join(BASE_DIR, 'locale'), )

LANGUAGES = [
  ('en', _('English')),
  ('fr', _('French')),
]

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = tempfile.gettempdir()

SITE_ID = env('MCE_SITE_ID', default=1, cast=int)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'debug': {
            'format': '%(asctime)s - [%(name)s] - [%(process)d] - [%(module)s] - [line:%(lineno)d] - [%(levelname)s] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[%(process)d] - %(asctime)s - %(name)s: [%(levelname)s] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'debug'
        },
        #'db_log': {
        #    'class': 'mce_django_app.db_log_handler.DatabaseLogHandler'
        #},
    },
    'loggers': {
        '': {
            'handlers': ['console'], #'db_log'],
            'level': env('MCE_LOG_LEVEL', default='DEBUG'),
            'propagate': False,
        },
        'urllib3': {'level': 'ERROR'},
        'chardet': {'level': 'WARN'},
        'cchardet': {'level': 'WARN'},
    },
}


TEST_RUNNER = 'project_test.runner.PytestTestRunner'

DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE = 10
DJANGO_DB_LOGGER_ENABLE_FORMATTER = False

#CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
)


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        # FIXME: 'mce_django_app.api.common.views.CustomObjectPermissions'
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25,
    'ORDERING_PARAM': 'sort',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

DJOSER = {
    "SEND_ACTIVATION_EMAIL": False,
    "PASSWORD_RESET_CONFIRM_URL": "#/password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "#/username/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "#/activate/{uid}/{token}",
    #"SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": ["http://test.localhost/"],
    'SERIALIZERS': {
        # TODO: 'user': 'mce_django_app.api.account.serializers.CustomUserSerializer',
    }
}


TAGGIT_CASE_INSENSITIVE = True

MCE_CHANGES_ENABLE = False

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'EDX_URL': "https://draft.navoica.pl",
#     }
# }

#ORGS_SLUGFIELD = 'django_extensions.db.fields.AutoSlugField'

#DDF_DEBUG_MODE = True

# DEBUG_TOOLBAR_CONFIG = {
#     "ENABLE_STACKTRACES": True,
#     "ENABLE_STACKTRACES_LOCALS": True
# }

SWAGGER_SETTINGS = {
    'LOGIN_URL': reverse_lazy('admin:login'),
    #'LOGOUT_URL': '/admin/logout',
    'PERSIST_AUTH': True,
    'REFETCH_SCHEMA_WITH_AUTH': True,
    'REFETCH_SCHEMA_ON_LOGOUT': True,

    'DEFAULT_INFO': 'mce_django_app.api.urls.swagger_info',

    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'in': 'header',
            'name': 'Authorization',
            'type': 'apiKey',
        },
        #'OAuth2 password': {
        #    'flow': 'password',
        #    'scopes': {
        #        'read': 'Read everything.',
        #        'write': 'Write everything,',
        #    },
        #    'tokenUrl': OAUTH2_TOKEN_URL,
        #    'type': 'oauth2',
        #},
        'Query': {
            'in': 'query',
            'name': 'auth',
            'type': 'apiKey',
        },
    },
    #'OAUTH2_REDIRECT_URL': OAUTH2_REDIRECT_URL,
    #'OAUTH2_CONFIG': {
    #    'clientId': OAUTH2_CLIENT_ID,
    #    'clientSecret': OAUTH2_CLIENT_SECRET,
    #    'appName': OAUTH2_APP_NAME,
    #},
    "DEFAULT_PAGINATOR_INSPECTORS": [
        #'testproj.inspectors.UnknownPaginatorInspector',
        'drf_yasg.inspectors.DjangoRestResponsePagination',
        'drf_yasg.inspectors.CoreAPICompatInspector',
    ]
}

REDOC_SETTINGS = {
    'SPEC_URL': ('schema-json', {'format': '.json'}),
}
