from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from ifmo_certs import CertificateBase, CertSys, CertificateError

# from ifmo_certs.courses.x0005_00 import X0005_00
from ifmo_certs.courses.x0008_00 import *
from ifmo_certs.courses.x0005_01 import *
from ifmo_certs.courses.x0002_01 import *
from ifmo_certs.courses.x0003_01 import *
from ifmo_certs.courses.x0009_00 import *
from ifmo_certs.courses.x0007_00 import *
from ifmo_certs.courses.x0001_02 import *
from ifmo_certs.courses.x0004_01 import *
from ifmo_certs.courses.x0006_00 import *
from ifmo_certs.courses.x0008_01 import *
from ifmo_certs.courses.x0005_02 import *
from ifmo_certs.courses.x0009_01 import *
from ifmo_certs.courses.x0007_01 import *
from ifmo_certs.courses.x0002_02 import *
from ifmo_certs.courses.x0003_02 import *
from ifmo_certs.courses.x0001_03 import *
from ifmo_certs.courses.x0008_02 import *
from ifmo_certs.courses.x0005_03 import *
from ifmo_certs.courses.x0009_02 import *
from ifmo_certs.courses.x0006_01 import *
from ifmo_certs.courses.x0007_02 import *
from ifmo_certs.courses.x0004_02 import *


class Command(BaseCommand):
    args = '-i <input_file> -c <course> [-o <output_directory>] [-s <strategy: ignore|update|fail>]'
    help = 'Create certificates'

    certificates = {
        # 'x0005_00': X0005_00,
        'x0008_00': X0008_00,
        'x0005_01': X0005_01,
        'x0002_01': X0002_01,
        'x0003_01': X0003_01,
        'x0009_00': X0009_00,
        'x0007_00': X0007_00,
        'x0001_02': X0001_02,
        'x0004_01': X0004_01,
        'x0006_00': X0006_00,
        'x0008_01': X0008_01,
        'x0005_02': X0005_02,
        'x0009_01': X0009_01,
        'x0007_01': X0007_01,
        'x0002_02': X0002_02,
        'x0003_02': X0003_02,
        'x0001_03': X0001_03,
        'x0008_02': X0008_02,
        'x0005_03': X0005_03,
        'x0009_02': X0009_02,
        'x0006_01': X0006_01,
        'x0007_02': X0007_02,
        'x0004_02': X0004_02,
    }

    option_list = BaseCommand.option_list + (
        make_option('-o', '--output',
                    dest='output', default='/ifmo/var/certificates',
                    help="Output path. Must be writeable."),
        make_option('-i', '--input',
                    dest='input', default=None,
                    help="CVS file with following lines: <user_id>,<percentage_0-100>,<cert_type>"),
        make_option('-s', '--strategy',
                    dest='strategy', default='update',
                    choices=['ignore', 'update', 'fail'],
                    help="Strategy"),
        make_option('-c', '--course',
                    dest='course', default=None,
                    # choices=[certificates.keys()],
                    help="Course one of following: %s" % certificates.keys()),
    )

    def handle(self, *args, **options):

        print "Generating certificates"

        if options.get('course') is None:
            raise CommandError('Course is not specified.')

        sys = CertSys(strategy=options.get('strategy'), generate=True, storage_prefix=options.get('output'))

        try:
            with open(options.get('input'), 'r') as f:
                for line in f:
                    certificate = self.certificates[options.get('course')].from_string(line.strip(), sys)
                    certificate.process()
        except Exception as e:
            raise CommandError(e)

        print "All certificates generated"

