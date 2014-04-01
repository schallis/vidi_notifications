vidi_notifications
==================

:Info: A Django application for handling Vidispine callbacks and raising
       signals
:Requirements: See setup.py


Set up notifications in Vidispine
=================================

POST the following XML to /API/notification::

    <NotificationDocument xmlns="http://xml.vidispine.com/schema/vidispine">
        <action>
            <http synchronous="false">
                <retry>3</retry>
                <contentType>application/json</contentType>
                <url>http://<app_url>:8000/notify/jobs</url>
                <method>POST</method>
                <timeout>5</timeout>
            </http>
        </action>
        <trigger>
            <job>
                <update/>
                <placeholder>false</placeholder>
            </job>
        </trigger>
    </NotificationDocument>

and also this one::

    <NotificationDocument xmlns="http://xml.vidispine.com/schema/vidispine">
        <action>
            <http synchronous="false">
                <retry>3</retry>
                <contentType>application/json</contentType>
                <url>http://<app_url>:8000/notify/modify</url>
                <method>POST</method>
                <timeout>5</timeout>
            </http>
        </action>
        <trigger>
            <modify/>
        </trigger>
    </NotificationDocument>



All handler code assumes that the Vidispine has been told to send JSON.


Running unit tests
------------------

::

    $ DJANGO_SETTINGS_MODULE=test_settings nosetests


Manually testing
----------------

You can manually send notifications to the module using a REST client to test
the signals. The notifications are in a slightly different format to that sent
by the signal and can be converted using ``utils.to_vidi_format()``.

An example notification to ``/jobs/``::

    {"field": [
        {"value": "FINISHED", "key": "status"},
        {"value": "0", "key": "sequenceNumber"},
        {"value": "2010-08-31T14:01:19.991+02:00", "key": "started"},
        {"value": "VX-JOB", "key": "jobId"},
        {"value": "FINISHED", "key": "currentStepStatus"},
        {"value": "test-user", "key": "user"},
        {"value": "5", "key": "totalSteps"},
        {"value": "VX-ITEM", "key": "item"},
        {"value": "UPDATE", "key": "action"},
        {"value": "2", "key": "currentStepNumber"},
        {"value": "UPLOAD", "key": "type"}
    ]}


Signals
-------

**Warning:** Each upload signal may be called multiple times so handler code should check for
appropriate statuses e.g. FINISHED if needed.

+-----------------------+-------------------------------------------------------------------+
| Signal                | Description                                                       |
+=======================+===================================================================+
| vidispine_upload      | Called multiple times to report the status of each import job     |
|                       | (using any import method)                                         |
+-----------------------+-------------------------------------------------------------------+
| vidispine_shape_import| Called when an shape is imported                                  |
+-----------------------+-------------------------------------------------------------------+
| vidispine_item_modify | Called when an item's metadata is modified                        |
+-----------------------+-------------------------------------------------------------------+
