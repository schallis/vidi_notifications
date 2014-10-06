from django.conf.urls import patterns, url

from .views import JobsView, ModifyView

urlpatterns = patterns(
    '',
    url(r'^jobs/?$', JobsView.as_view(), name='jobs_notify'),
    url(r'^modify/?$', ModifyView.as_view(), name='modify_notify'),
)
