# -*- coding: utf-8 -*-

from ifmo_certs import CertificateBase
from path import path


class X0008_01(CertificateBase):  # noqa

    source_files = {
        'Honor': 'certificate-honor.html',
        'Simple': 'certificate.html'
    }
    source_dir = path(__file__).dirname() + '/resources/'
    course_id = 'ITMO/x0008.01/2015_01'
    course_name = 'x0008.01 Введение в технологии веб-программирования (Javascript)'
