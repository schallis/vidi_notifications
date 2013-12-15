from hwwutils.django.signals import UniqueSignal

vidispine_upload = UniqueSignal(providing_args=["job", "request"])
vidispine_new_version = UniqueSignal(providing_args=["job", "request"])
