# -*- coding: utf-8 -*-

from ifmo_certs import CertificateBase
from path import path


class X0004_02(CertificateBase):  # noqa

    source_files = {
        'Honor': 'certificate-honor.html',
        'Simple': 'certificate.html',
    }
    source_dir = path(__file__).dirname() + '/resources/'
    course_id = 'ITMO/x0004.02/2015_04'
    course_name = 'ITMO/x0004.02/2015_04'
