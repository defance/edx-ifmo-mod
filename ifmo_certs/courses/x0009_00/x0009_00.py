# -*- coding: utf-8 -*-

from ifmo_certs import CertificateBase
from path import path


class X0009_00(CertificateBase):  # noqa

    source_files = {
        '"Honor"': 'certificate-honor.html',
        '"Simple"': 'certificate.html'
    }
    source_dir = path(__file__).dirname() + '/resources/'
    course_id = 'ITMO/x0009.00/2014_10'
    course_name = 'x0009.00 Введение в технологии веб-программирования (PHP)'
