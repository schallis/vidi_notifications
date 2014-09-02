import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from vidi_notifications.utils import to_vidi_format
from vidi_notifications.signals import vidispine_item_modify


class TestJobs(TestCase):

    def setUp(self):
        self.vs_item_id = None

    def test_started(self):
        post_data = {
            'itemId': 'VX-ITEM',
            'broadcast_ready': 'True'
        }

        def test_listener(sender, vs_item_id, request, *args, **kwargs):
            self.vs_item_id = vs_item_id

        vidispine_item_modify.connect(test_listener)

        data = to_vidi_format(post_data)
        response = self.client.post(reverse('modify_notify'),
                                    json.dumps(data), "text/json")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'handled modification signal')
        self.assertEquals(self.vs_item_id, 'VX-ITEM')
