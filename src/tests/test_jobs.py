import json
from mock import MagicMock

from django.core.urlresolvers import reverse
from django.test import TestCase

from vidi_notifications.utils import to_vidi_format
from vidi_notifications.signals import vidispine_shape_import

base_post_data = {
    'item': 'VX-ITEM',
    'jobId': 'VX-JOB',
    'currentStepNumber': '2',
    'action': 'UPDATE',
    'started': '2010-08-31T14:01:19.991+02:00',
    'type': 'UPLOAD',
    'totalSteps': '5',
    'user': 'test-user',
    'sequenceNumber': '0',
}


class TestJobs(TestCase):

    def test_started(self):
        post_data = base_post_data.copy()
        post_data.update({
            'currentStepStatus': 'STARTED',
            'status': 'STARTED'
        })
        data = to_vidi_format(post_data)
        response = self.client.post(reverse('jobs_notify'),
                                    json.dumps(data), "text/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'got started job')

    def test_failed(self):
        post_data = base_post_data.copy()
        post_data.update({
            'currentStepStatus': 'FAILED_FATAL',
            'status': 'FAILED_TOTAL'
        })
        data = to_vidi_format(post_data)
        response = self.client.post(reverse('jobs_notify'),
                                    json.dumps(data), "text/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'got failed job')

    def test_success(self):
        post_data = base_post_data.copy()
        post_data.update({
            'currentStepStatus': 'FINISHED',
            'status': 'FINISHED'
        })
        data = to_vidi_format(post_data)
        response = self.client.post(reverse('jobs_notify'),
                                    json.dumps(data), "text/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'got finished job')

    def test_unknown(self):
        post_data = base_post_data.copy()
        post_data.update({
            'currentStepStatus': 'UNKNOWN',
            'status': 'UNKNOWN'
        })
        data = to_vidi_format(post_data)
        response = self.client.post(reverse('jobs_notify'),
                                    json.dumps(data), "text/json")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.content, 'unknown job')

    def test_service_up_url(self):
        # Devops are making these exact assertions with Nagios
        response = self.client.get(reverse('jobs_notify'))
        self.assertEquals(response.status_code, 200)
        self.assertIn('otificat', response.content)

    def test_import_shape(self):
        post_data = base_post_data.copy()
        post_data.update({
            'type': 'SHAPE_IMPORT',
            'status': 'FINISHED'
        })

        call_back = MagicMock(spec=lambda _: True)

        vidispine_shape_import.connect(call_back)
        data = to_vidi_format(post_data)
        self.client.post(reverse('jobs_notify'),
                         json.dumps(data), "text/json")

        self.assertTrue(call_back.called, 'signal not caught or fired')
