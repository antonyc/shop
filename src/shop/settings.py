# coding: utf-8

import os
from collections import namedtuple

ROOT_PATH = '/usr/lib/amadika/shop'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

HOST_NAME = 'amadika.ru'
SERVER_EMAIL = 'shop@amadika.ru'

ADMINS = (
    # ('Anton Chaporgin', 'chaporginanton@yandex.ru'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'amadika_shop',                      # Or path to database file if using sqlite3.
        'USER': 'shop_admin',                      # Not used with sqlite3.
        'PASSWORD': 'password',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB; SET names utf8;'
        }, 
    }
}

MONGO_DATABASES={'default':{'NAME': 'shop',
                            'HOST': '127.0.0.1'
}}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

LOCALE_PATHS = ('/usr/share/amadika/shop/locale', )
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/usr/share/amadika/shop/media/'
UPLOAD_PATH = 'user_uploads'
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/usr/share/amadika/shop/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'y_mu8x5q*c(i%&lf$7!)n9uw#&kw6q(uoi^!mm62!afb*w^r$y'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    '/usr/lib/amadika/shop/templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
#    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.gis',
    'catalog',
    'orders',
    'administration',
    'pages',
    'users',
    'loginza',
    'south',
    'utils',
    'cart',
    'geonames',
    'geocoding',
    'email_generators',
    'business_events',
    'compress',
    'django.contrib.humanize',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

AUTH_PROFILE_MODULE = 'users.UserProfile'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'loginza.authentication.LoginzaBackend',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
        'default': {
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'admin_must_know': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': 0,
        },
        'django': {
            'handlers': [],
            'propagate': True,
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': [],
        'level': 'INFO',
    }

}

ImageSize = namedtuple('ImageSize', 'width height')


THUMBNAILS = {'large': ImageSize._make((750, 600)),
              'big': ImageSize._make((400, 400)),
              'bigger': ImageSize._make((150, 150)),
              'common': ImageSize._make((110, 110,)),
              'small': ImageSize._make((60, 60))}

THUMBNAIL_SIZE = THUMBNAILS['common']

LOGINZA_DEFAULT_PROVIDERS_SET = 'google,facebook,vkontakte,twitter'
LOGINZA_AMNESIA_PATHS = ('/accounts/final_step/','/accounts/login/')

COMPRESS = True
from deployment import list_of_files

try:
    from local_settings import *
except ImportError:
    pass

try:
    from secret_settings import *
except ImportError:
    pass

# Это для отладки, если у вас вдруг не собирается статика.
# print list_of_files(STATIC_ROOT, 'css')

COMPRESS_JS = {
    'all': {
        'source_filenames': list_of_files(STATIC_ROOT, 'js'),
        'output_filename': 'all.js'
    },
    'galleriffic': {
        'source_filenames': (os.path.join(STATIC_ROOT, 'js/jquery.gallerific.js'),),
        'output_filename': 'galleriffic.js'
    }
}
COMPRESS_CSS = {
    'screen': {
        'source_filenames': list_of_files(STATIC_ROOT, 'css'),
        'output_filename': 'css/screen.css'
    },
    'private': {
        'source_filenames': list_of_files(STATIC_ROOT, 'css'),
        'output_filename': 'css/private.css'
    }
}
