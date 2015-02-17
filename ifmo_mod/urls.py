from django.conf import settings
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'partners$', 'ifmo_mod.views.partners'),
    url(r'^external/ant/(?P<course>[0-9]+)/(?P<unit>[0-9]+)(?:/(?P<ssoid>\w+))?$', 'ifmo_mod.views.ant_external', name='ant_external'),  # noqa

    url(r'^summary$', 'ifmo_mod.views.summary'),
    url(r'^summary_handler$', 'ifmo_mod.views.summary_handler'),

    url(r'^courses/{}/date_check$'.format(settings.COURSE_ID_PATTERN), 'ifmo_mod.views.date_check', name="date_check"),
)