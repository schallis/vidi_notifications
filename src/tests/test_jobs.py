import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from mock import MagicMock, patch

from vidi_notifications.signals import vidispine_shape_import
from vidi_notifications.tasks import job_view_task
from vidi_notifications.utils import to_vidi_format

from tests.utils import mock_signal_receiver


class TestJobs(TestCase):

    def setUp(self):
        self.base_post_data = {
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

    def test_started(self):
        post_data = self.base_post_data.copy()
        post_data.update({
            'currentStepStatus': 'STARTED',
            'status': 'STARTED'
        })
        data = to_vidi_format(post_data)
        response = self.client.post(
            reverse('jobs_notify'),
            json.dumps(data),
            content_type="text/json"
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'got started job')

    def test_failed(self):
        post_data = self.base_post_data.copy()
        post_data.update({
            'currentStepStatus': 'FAILED_FATAL',
            'status': 'FAILED_TOTAL'
        })
        data = to_vidi_format(post_data)
        response = self.client.post(
            reverse('jobs_notify'),
            json.dumps(data),
            content_type="text/json"
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'got failed job')

    def test_success(self):
        post_data = self.base_post_data.copy()
        post_data.update({
            'currentStepStatus': 'FINISHED',
            'status': 'FINISHED'
        })
        data = to_vidi_format(post_data)
        response = self.client.post(
            reverse('jobs_notify'),
            json.dumps(data),
            content_type="text/json"
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'got finished job')

    def test_unknown(self):
        post_data = self.base_post_data.copy()
        post_data.update({
            'currentStepStatus': 'UNKNOWN',
            'status': 'UNKNOWN'
        })
        data = to_vidi_format(post_data)
        response = self.client.post(
            reverse('jobs_notify'),
            json.dumps(data),
            content_type="text/json"
        )
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.content, 'unknown job')

    def test_service_up_url(self):
        # Devops are making these exact assertions with Nagios
        response = self.client.get(reverse('jobs_notify'))
        self.assertEquals(response.status_code, 200)
        self.assertIn('otificat', response.content)

    def test_import_shape(self):
        post_data = self.base_post_data.copy()
        post_data.update({
            'type': 'SHAPE_IMPORT',
            'status': 'FINISHED'
        })

        call_back = MagicMock(spec=lambda _: True)

        vidispine_shape_import.connect(call_back)
        data = to_vidi_format(post_data)

        self.client.post(
            reverse('jobs_notify'),
            json.dumps(data),
            content_type="text/json"
        )

        self.assertTrue(call_back.called, 'signal not caught or fired')

    @patch('vidi_notifications.views.job_view_task')
    def test_import_shape_test_task(self, job_view_task):
        post_data = self.base_post_data.copy()
        post_data.update({
            'type': 'SHAPE_IMPORT',
            'status': 'FINISHED'
        })

        data = to_vidi_format(post_data)

        self.client.post(
            reverse('jobs_notify'),
            json.dumps(data),
            content_type="text/json"
        )

        job_view_task.delay.assert_called_once_with(post_data)

    def test_job_view_task(self):
        post_data = self.base_post_data.copy()
        post_data.update({
            'type': 'SHAPE_IMPORT',
            'status': 'FINISHED'
        })

        with mock_signal_receiver(vidispine_shape_import) as receiver:
            job_view_task.delay(post_data)
            self.assertEqual(1, receiver.call_count)

    def test_notification_callback_without_celery(self):
        settings.USE_CELERY_FOR_NOTIFICATIONS = False

        post_data = self.base_post_data.copy()
        post_data.update({
            'currentStepStatus': 'STARTED',
            'status': 'STARTED'
        })
        data = to_vidi_format(post_data)
        response = self.client.post(
            reverse('jobs_notify'),
            json.dumps(data),
            content_type="text/json"
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'got started job')
