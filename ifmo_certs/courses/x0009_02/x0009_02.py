# -*- coding: utf-8 -*-

from ifmo_certs import CertificateBase
from path import path


class X0009_02(CertificateBase):  # noqa

    source_files = {
        'Simple': 'certificate.html',
        'Honor': 'certificate-honor.html',
    }
    source_dir = path(__file__).dirname() + '/resources/'
    course_id = 'ITMO/x0009.02/2015_04'
    course_name = 'x0009.02 Введение в технологии веб-программирования (PHP)'
