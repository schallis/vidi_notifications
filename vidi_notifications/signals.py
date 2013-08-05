from hwwutils.django.signals import UniqueSignal

vidispine_upload = UniqueSignal(providing_args=["job", "request"])
