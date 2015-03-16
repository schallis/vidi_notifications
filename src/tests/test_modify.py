import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from mock import ANY, patch

from vidi_notifications.signals import vidispine_item_modify
from vidi_notifications.tasks import modify_view_task
from vidi_notifications.utils import to_vidi_format
from tests.utils import mock_signal_receiver


class TestJobs(TestCase):

    def setUp(self):
        self.payload = {
            'itemId': 'VX-ITEM',
            'broadcast_ready': 'True'
        }
        self.vidispine_payload = to_vidi_format(self.payload)

    def tearDown(self):
        if hasattr(settings, 'USE_CELERY_FOR_NOTIFICATIONS'):
            del settings.USE_CELERY_FOR_NOTIFICATIONS

    @patch('vidi_notifications.views.modify_view_task')
    def test_started_no_celery(self, modify_view_task):
        settings.USE_CELERY_FOR_NOTIFICATIONS = False

        response = self.client.post(
            reverse('modify_notify'),
            json.dumps(self.vidispine_payload),
            content_type="text/json"
        )

        modify_view_task.assert_called_once_with(self.payload)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'handled modification signal')

    @patch('vidi_notifications.views.modify_view_task')
    def test_started(self, modify_view_task):
        response = self.client.post(
            reverse('modify_notify'),
            json.dumps(self.vidispine_payload),
            content_type="text/json"
        )

        modify_view_task.delay.assert_called_once_with(self.payload)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'handled modification signal')

    def test_modify_task(self):
        with mock_signal_receiver(vidispine_item_modify) as receiver:
            modify_view_task.delay(self.payload)

            receiver.assert_called_once_with(
                signal=ANY,
                vs_item_id='VX-ITEM',
                sender=ANY
            )
