"""
Set up notifications in Vidispine
=================================

POST to /API/notification::

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

The handler code below assumes that the Vidispine has been told to send JSON.


Result of notifications
=======================

All notifications received that have a known type dispatch corresponding
Django signals allow arbitrary code to be actioned easily.
"""
import json
import logging

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from .tasks import job_view_task, modify_view_task
from .utils import from_vidi_format

log = logging.getLogger(__name__)


def get_data(request):
    return from_vidi_format(json.loads(request.body))


def handle_error(request):
    msg = (
        "Error interpreting notification. Notfications must "
        "be sent as JSON in the format Vidispine provides. "
        "Notification began with '%s'"
    )
    log.exception(msg, request.body[:20])
    return HttpResponse(msg, status=400)


class BaseNotificationView(View):

    def get(self, request, *args, **kwargs):
        """A dummy endpoint that Devops can use to confirm the service is up"""
        return HttpResponse('The notification service is active. Real '
                            'notifications must use the POST method.')

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(BaseNotificationView, self).dispatch(*args, **kwargs)


class JobsView(BaseNotificationView):
    """Handle /vs/jobs notifications"""

    def post(self, request, *args, **kwargs):
        try:
            job_data = get_data(request)
        except (ValueError, KeyError):
            return handle_error(request)

        if hasattr(
            settings,
            'USE_CELERY_FOR_NOTIFICATIONS'
        ) and not settings.USE_CELERY_FOR_NOTIFICATIONS:
            job_view_task(job_data)
        else:
            job_view_task.delay(job_data)

        job_status = job_data['status']
        job_id = job_data['jobId']

        log.debug("Got job status: {0} {1}".format(job_status, job_id))
        if job_status in ["FINISHED", "FINISHED_WARNING"]:
            return HttpResponse('got finished job')
        elif job_status in ["FAILED_TOTAL", "ABORTED"]:
            return HttpResponse('got failed job')
        elif job_status in ["STARTED", "READY"]:
            return HttpResponse('got started job')
        else:
            log.exception("Unknown job status. {0}".format(job_status))
            return HttpResponse('unknown job', status=400)


class ModifyView(BaseNotificationView):
    """Handle vidispine item modify notifications"""

    def post(self, request, *args, **kwargs):
        try:
            modify_data = get_data(request)
        except (ValueError, KeyError):
            return handle_error(request)

        modify_view_task.delay(modify_data)

        return HttpResponse('handled modification signal')
