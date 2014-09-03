from django.conf import settings


def pytest_configure():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'mydatabase',
            }
        },
        ROOT_URLCONF='vidi_notifications.urls',
        VIDISPINE_REPLACE_URLS={},
        VIDISPINE_URL='http://do-not-use',
        VIDISPINE_USERNAME='test',
        VIDISPINE_PASSWORD='test',
        VIDISPINE_PORT='9100',
    )
