# -*- coding: utf-8 -*-

# Django settings for plannerarena.org project.
import os
gettext = lambda s: s

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('ROBO Design', 'robodesign@gmail.com'),
)

MANAGERS = ADMINS

PROJECT_PATH=os.path.dirname( os.path.realpath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'site.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Bucharest'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

LANGUAGES = [
    ('en', 'English'),
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static_collected')

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
    os.path.join(PROJECT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'q&dfmuf2!h1+(zqd*27w0$1m9l-=us9nz+o5@^^cyv1s2$-@8j'

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
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
)

ROOT_URLCONF = 'plannerarena_org.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.i18n',
  'django.core.context_processors.request',
  'django.core.context_processors.media',
  'django.core.context_processors.static',
  'django.contrib.messages.context_processors.messages',
  'cms.context_processors.media',
  'sekizai.context_processors.sekizai',
  'robo_utils.context_processors.sites',
)

CMS_TEMPLATES = (
    ('pages/default.html', u'Pagină generică'),
    ('pages/sitemap.html', u'Hartă site'),
    ('pages/contact.html', u'Pagină de contact'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'cms',
    'mptt',
    'menus',
    'sekizai',
    'cms.plugins.link',
    'cms.plugins.text',
    'cmsplugin_htmlsitemap',
    'robo_utils',
    'contact',
    'south',
    'problems',
    'tst'
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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'contact': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL='cucu@example.com'
RECAPTCHA_PUBLIC_KEY='6LfElcoSAAAAAAuVn9jC5HfVrg-zAh_TACcOXLfZ'
RECAPTCHA_PRIVATE_KEY='6LfElcoSAAAAAAMLodEIqls0rbT5KTKQ1pWG0ZlI'
RECAPTCHA_THEME='clean'


# django-cms options

CMS_PLACEHOLDER_CONF = {
    'pages/default.html page_content': {
        "plugins": ('TextPlugin', 'PicturePlugin', 'FilePlugin', 'FolderPlugin', 'FilerImagePlugin', 'FilerFilePlugin', 'FilerFolderPlugin', 'LinkPlugin'),
        'name': u'Page content',
    },
    'pages/sitemap.html page_content': {
        "plugins": ('HtmlSitemapPlugin', 'TextPlugin', 'LinkPlugin'),
        'name': u'Site map content',
        'limits': {'HtmlSitemapPlugin': 1},
    },
    'pages/contact.html page_content': {
        'plugins': ('PicturePlugin', 'TextPlugin', 'FilerImagePlugin', 'LinkPlugin'),
        'name': u'Contact information',
    },
    'contact_form': {
        'plugins': ('ContactPlugin'),
        'name': u'Contact form',
        'limits': {'ContactPlugin': 1},
    },
}

#CMS_URL_OVERWRITE=False

CMS_TEMPLATE_INHERITANCE=False
CMS_SOFTROOT=True

