from path import path
from django.conf import settings

import edxmako


def patch_templates():
    template_path = path(__file__).dirname() / 'templates'
    edxmako.paths.add_lookup('main', template_path, prepend=True)


def run():
    patch_templates()
