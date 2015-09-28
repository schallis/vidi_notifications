# coding: utf-8
import collections
import logging

from celery.task import task
from django.conf import settings

from .signals import (
    vidispine_item_modify,
    vidispine_new_version,
    vidispine_shape_import,
    vidispine_transcode,
    vidispine_upload,
    vidispine_copy_file,
)
from .utils import JobObject


CONFIG = getattr(settings, 'CELERY_VIDI_NOTIFICATION_CONFIG', {})
TASK_CONFIG = {
    'ignore_result': True,
}
TASK_CONFIG.update(CONFIG)
if 'name' in TASK_CONFIG:
    del TASK_CONFIG['name']


signal_map = collections.defaultdict(str, {
    'UPLOAD': vidispine_upload,
    'RAW_IMPORT': vidispine_upload,
    'PLACEHOLDER_IMPORT': vidispine_upload,
    'SHAPE_IMPORT': vidispine_shape_import,
    'ESSENCE_VERSION': vidispine_new_version,
    'TRANSCODE': vidispine_transcode,
    'COPY_FILE': vidispine_copy_file,
})


log = logging.getLogger(__name__)


@task(name='JOB_VIDI_NOTIFICATION', **TASK_CONFIG)
def job_view_task(job_data):
    job = JobObject(job_data)

    signal = signal_map[job.type]
    if signal:
        log.debug('Sending signal for job {}'.format(signal))
        signal.send(sender=job_view_task.__name__, job=job)


@task(name='MODIFY_VIDI_NOTIFICATION', **TASK_CONFIG)
def modify_view_task(modify_data):
    log.debug('Sending signal for item modification')

    vidispine_item_modify.send(
        sender=modify_view_task.__name__,
        vs_item_id=modify_data['itemId'],
        full_data=modify_data
    )
