from .base import *

import dj_database_url
import os


DEBUG = False

ADMINS = [
    ('John Johnson', 'john@educa.magnisale.com'),
]

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}


# Email server configuration
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = config('SERVER_EMAIL')
MAILGUN_API_KEY = config('MAILGUN_API_KEY')  
MAILGUN_SENDER_DOMAIN = config('MAILGUN_SENDER_DOMAIN')

# Cache settings
REDIS_URL = config('REDIS_URL')
CACHES['default']['LOCATION'] = REDIS_URL
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [REDIS_URL]

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
