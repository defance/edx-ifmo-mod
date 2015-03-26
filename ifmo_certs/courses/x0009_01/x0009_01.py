# -*- coding: utf-8 -*-

from ifmo_certs import CertificateBase
from path import path


class X0009_01(CertificateBase):  # noqa

    source_files = {
        'Honor': 'certificate-honor.html',
        'Simple': 'certificate.html'
    }
    source_dir = path(__file__).dirname() + '/resources/'
    course_id = 'ITMO/x0009.01/2015_01'
    course_name = 'x0009.01 Введение в технологии веб-программирования (PHP)'
