# -*- coding: utf-8 -*-

from ifmo_certs import CertificateBase
from path import path


class X0001_02(CertificateBase):  # noqa

    source_files = {
        'Simple': 'certificate.html'
    }
    source_dir = path(__file__).dirname() + '/resources/'
    course_id = 'ITMO/x0001.02/2014_11'
    course_name = 'x0001.02 Теория графов'
