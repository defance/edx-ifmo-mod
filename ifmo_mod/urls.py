from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'partners$', 'ifmo_mod.views.partners'),
    url(r'^external/ant/(?P<course>[0-9]+)/(?P<unit>[0-9]+)(?:/(?P<ssoid>\w+))?$', 'ifmo_mod.views.ant_external', name='ant_external'),  # noqa

    url(r'^summary$', 'ifmo_mod.views.summary')
)