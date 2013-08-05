DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'HOST': '',
        'NAME': 'test.db',
        'PASSWORD': u'********************',
        'PORT': '',
        'USER': 'my_user'
    }
}

ROOT_URLCONF='vidi_notifications.urls'

SECRET_KEY = '***'
ALLOWED_HOSTS = '*'

VIDISPINE_REPLACE_URLS = {}

VIDISPINE_URL = 'http://do-not-use'
VIDISPINE_USERNAME = 'test'
VIDISPINE_PASSWORD = 'test'
VIDISPINE_PORT = '9100'
