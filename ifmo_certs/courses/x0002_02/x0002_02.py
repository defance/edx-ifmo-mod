# -*- coding: utf-8 -*-

from ifmo_certs import CertificateBase
from path import path


class X0002_02(CertificateBase):  # noqa

    source_files = {
        'Honor': 'certificate-honor.html',
        'Simple': 'certificate.html'
    }
    source_dir = path(__file__).dirname() + '/resources/'
    course_id = 'ITMO/x0002.02/2015_02'
    course_name = 'x0002.02 Создание веб-интерфейсов с помощью HTML и CSS'
