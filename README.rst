vidi_notifications
==================

:Info: A Django application for handling Vidispine callbacks and raising
       signals
:Requirements: See setup.py


Running tests
-------------

::

    $ DJANGO_SETTINGS_MODULE=test_settings nosetests


Signals
-------

**Warning:** Each signal may be called multiple times so handler code should check for
appropriate statuses e.g. FINISHED if needed.

+------------------+-------------------------------------------------------------------+
| Signal           | Description                                                       |
+==================+===================================================================+
| vidispine_upload | Called multiple times to report the status of each import job     |
|                  | (using any import method)                                         |
+------------------+-------------------------------------------------------------------+
