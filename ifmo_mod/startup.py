from django.conf import settings
from django.conf.urls import include, url
from path import path
from .patch import (course, problem,)

import edxmako

import logging
log = logging.getLogger(__name__)


def patch_templates():
    template_path = path(__file__).dirname() / 'templates'
    edxmako.paths.add_lookup('main', template_path, prepend=True)


def _patch_variant_url(app_name, urls_module):
    app_urls = __import__('%s.urls' % (app_name,), fromlist=['urlpatterns'])
    app_urls.urlpatterns.insert(0, url(r'', include(urls_module)))

def patch_urls():
    try:
        _patch_variant_url('lms', 'ifmo_mod.urls')
    except Exception:
        pass


def patch_middleware():
    settings.MIDDLEWARE_CLASSES += ('crequest.middleware.CrequestMiddleware',)


def run():
    patch_templates()
    patch_urls()
    course.patch()
    problem.patch()
    patch_middleware()

