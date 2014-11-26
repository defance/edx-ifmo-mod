from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from ifmo_certs import CertificateBase, CertSys, CertificateError

from ifmo_certs.courses.x0005_00 import X0005_00
from ifmo_certs.courses.x0008_00 import X0008_00


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    certificates = {
        'x0005_00': X0005_00,
        'x0008_00': X0008_00
    }

    option_list = BaseCommand.option_list + (
        make_option('-o', '--output',
                    dest='output', default='/tmp/edx-ifmo-certs/',
                    help="Output path. Must be writeable."),
        make_option('-i', '--input',
                    dest='input', default=None,
                    help="CVS file with following lines: <user_id>,<percentage_0-100>,<cert_type>"),
        make_option('-s', '--strategy',
                    dest='strategy', default='ignore',
                    choices=['ignore', 'update', 'fail'],
                    help="Strategy"),
        make_option('-c', '--course',
                    dest='course', default=None,
                    # choices=[certificates.keys()],
                    help="Course"),
    )

    def handle(self, *args, **options):

        print "Generating certificates"

        print options

        if options.get('course') is None:
            raise CommandError('Course is not specified.')

        sys = CertSys(strategy='update', generate=True, storage_prefix='/tmp')

        try:
            with open(options.get('input'), 'r') as f:
                for line in f:
                    certificate = self.certificates[options.get('course')].from_string(line, sys)
                    certificate.process()
        except Exception as e:
            raise CommandError(e)

        print "All certificates generated"

