from hwwutils.django.signals import UniqueSignal

vidispine_upload = UniqueSignal(providing_args=["job", "request"])
vidispine_new_version = UniqueSignal(providing_args=["job", "request"])
vidispine_item_modify = UniqueSignal(providing_args=["vs_item_id", "request"])
