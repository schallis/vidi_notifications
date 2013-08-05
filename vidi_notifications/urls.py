from django.conf.urls.defaults import patterns, url

from .views import JobsView

urlpatterns = patterns('',
    url(r'^jobs/?$', JobsView.as_view(), name='jobs_notify'),
)
