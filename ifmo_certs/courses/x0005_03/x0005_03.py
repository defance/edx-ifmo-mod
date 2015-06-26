# -*- coding: utf-8 -*-

from ifmo_certs import CertificateBase
from path import path


class X0005_03(CertificateBase):  # noqa

    source_files = {
        'Simple': 'certificate.html',
    }
    source_dir = path(__file__).dirname() + '/resources/'
    course_id = 'ITMO/x0005.03/2015_04'
    course_name = 'x0005.03 RoboEd - Практическая робототехника'
