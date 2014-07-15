from path import path
# from django.conf import settings
from .patch import (course, problem,)

import edxmako

import logging
log = logging.getLogger(__name__)


def patch_templates():
    template_path = path(__file__).dirname() / 'templates'
    edxmako.paths.add_lookup('main', template_path, prepend=True)


def run():
    patch_templates()
    course.patch()
    problem.patch()
