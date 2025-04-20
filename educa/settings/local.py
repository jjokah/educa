from .base import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email server configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

import mimetypes
mimetypes.add_type('application/javascript', '.js', True)
mimetypes.add_type('text/css', '.css', True)