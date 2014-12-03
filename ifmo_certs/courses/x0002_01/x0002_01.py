# -*- coding: utf-8 -*-

from ifmo_certs import CertificateBase
from path import path


class X0002_01(CertificateBase):  # noqa

    source_files = {
        'Honor': 'certificate-honor.html',
        'Simple': 'certificate.html'
    }
    source_dir = path(__file__).dirname() + '/resources/'
    course_id = 'ITMO/x0002.01/2014_09'
    course_name = 'x0002.01 Создание веб-интерфейсов с помощью HTML и CSS'
