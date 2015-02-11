# -*- coding: utf-8 -*-

from ifmo_certs import CertificateBase
from path import path


class X0006_00(CertificateBase):  # noqa

    source_files = {
        'Honor': 'certificate-honor.html',
        'Simple': 'certificate.html',
    }
    source_dir = path(__file__).dirname() + '/resources/'
    course_id = 'ITMO/x0006.00/2014_11'
    course_name = 'x0006.00 Основы электромеханических систем'
