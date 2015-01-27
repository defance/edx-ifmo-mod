# -*- coding: utf-8 -*-

from ifmo_certs import CertificateBase
from path import path


class X0004_01(CertificateBase):  # noqa

    source_files = {
        'Honor': 'certificate.html'
    }
    source_dir = path(__file__).dirname() + '/resources/'
    course_id = 'ITMO/x0004.01/2014_11'
    course_name = 'x0004.01 Создание продвинутых веб-интерфейсов с помощью HTML5 и CSS3'
