# -*- coding: utf-8 -*-

from ifmo_certs import CertificateBase
from path import path


class X0003_01(CertificateBase):  # noqa

    source_files = {
        '"Simple"': 'certificate.html',
    }
    source_dir = path(__file__).dirname() + '/resources/'
    course_id = 'ITMO/x0003.01/2014_09'
    course_name = 'x0003.01 Линейные электрические цепи'
