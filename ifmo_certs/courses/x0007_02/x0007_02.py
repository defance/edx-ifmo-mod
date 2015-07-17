# -*- coding: utf-8 -*-

from ifmo_certs import CertificateBase
from path import path


class X0007_02(CertificateBase):  # noqa

    source_files = {
        'Honor': 'certificate-honor.html',
    }
    source_dir = path(__file__).dirname() + '/resources/'
    course_id = 'ITMO/x0007.02/2015_04'
    course_name = 'x0007.02 RoboEd - Основы робототехники'
