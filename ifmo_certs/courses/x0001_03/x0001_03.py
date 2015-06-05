# -*- coding: utf-8 -*-

from ifmo_certs import CertificateBase
from path import path


class X0001_03(CertificateBase):  # noqa

    source_files = {
        'Simple': 'certificate.html'
    }
    source_dir = path(__file__).dirname() + '/resources/'
    course_id = 'ITMO/x0001.03/2015_03'
    course_name = 'x0001.03 Методы и алгоритмы теории графов'
