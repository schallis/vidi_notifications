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
import collections
import logging

from django.http import HttpResponse
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt

from ZonzaRest.job import ZJob

from .utils import from_vidi_format
from .signals import (vidispine_upload, vidispine_new_version,
                      vidispine_item_modify)

log = logging.getLogger(__name__)


signal_map = collections.defaultdict(str, {
    'UPLOAD': vidispine_upload,
    'RAW_IMPORT': vidispine_upload,
    'PLACEHOLDER_IMPORT': vidispine_upload,
    'ESSENCE_VERSION': vidispine_new_version,
})


def get_data(request):
    raw_data = request.raw_post_data
    json_dict = json.loads(raw_data)
    return from_vidi_format(json_dict)

def handle_error(request):
    raw_data = request.raw_post_data
    snippet = raw_data[:20]
    msg = "Error interpreting notification. Notfications must " \
          "be sent as JSON in the format Vidispine provides. " \
          "Notification began with '{}'".format(snippet)
    log.exception(msg)
    return HttpResponse(msg, status=400)


class BaseNotificationView(View):

    def get(self, request, *args, **kwargs):
        """A dummy endpoint that Devops can use to confirm the service is up"""
        return HttpResponse('The notification service is active. Real ' \
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

        job = ZJob(json_dict=job_data)
        job_type = job.type
        signal = signal_map[job_type]

        if signal:
            log.debug('Sending signal for job {}'.format(signal))
            signal.send(sender=self, job=job, request=request)

        log.debug("Got job status: {0} {1}".format(job.status, job.jobId))
        if job.status in ["FINISHED", "FINISHED_WARNING"]:
            return HttpResponse('got finished job')
        elif job.status in ["FAILED_TOTAL", "ABORTED"]:
            return HttpResponse('got failed job')
        elif job.status in ["STARTED", "READY"]:
            return HttpResponse('got started job')
        else:
            log.exception("Unknown job status. {0}".format(job.status))
            return HttpResponse('unknown job', status=400)


class ModifyView(BaseNotificationView):
    """Handle vidispine item modify notifications"""

    def post(self, request, *args, **kwargs):
        try:
            modify_data = get_data(request)
        except (ValueError, KeyError):
            return handle_error(request)

        item_id = modify_data['itemId']
        log.debug('Sending signal for item modification')
        vidispine_item_modify.send(sender=self, vs_item_id=item_id, request=request)
        return HttpResponse('handled modification signal')
