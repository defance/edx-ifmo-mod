from certificates.models import GeneratedCertificate
from django.contrib.auth.models import User
from opaque_keys.edx.keys import CourseKey
from subprocess import Popen, PIPE

import hashlib
import os
import weasyprint

from . import utils


class CertificateError(Exception):
    pass


class CertificateBase(object):

    type = ''  # Honor, Simple or Others
    user_id = 0
    percent = 0  # 0-100

    # HTML File
    source_dir = ''
    source_files = {}
    course_id = 'ITMO/x0003.00/2014'
    course_name = ''

    certificate_obj = None
    course_key = None

    certsys = None

    @classmethod
    def from_string(cls, str, certsys):
        params = str.split(',')
        return cls(params[0], params[1], params[2], certsys)

    def __init__(self, user_id, percent, type, certsys):
        self.user_id = user_id
        self.percent = percent
        self.type = type
        self.certsys = certsys

        self.course_key = CourseKey.from_string(self.course_id)

        try:
            self.certificate_obj = GeneratedCertificate.objects.get(user_id=self.user_id, course_id=self.course_key)
        except GeneratedCertificate.DoesNotExist:
            pass

    def generate(self):

        # Get source file
        source_file = self.source_files[self.type] if self.type in self.source_files else None

        if source_file is None:
            print "Wanted to generate certificate for user_id=%s with mode=%s but have no file specified" % \
                  (self.user_id, self.type)
            return false

        source_file = "%s/%s" % (self.source_dir, source_file)

        if not os.path.isfile(source_file):
            print "Wanted to generate certificate for user_id=%s with mode=%s but have no file: %s" % \
                  (self.user_id, self.type, source_file)

        utils.ensure_dir(self.pdf_local_location)

        string = utils.get_file_contents(source_file).format(
            student_name=self.student_printed_name.encode('utf-8'),

            title='{course_name}'.format(
                student_name=self.student_printed_name.encode('utf8'),
                course_name=self.course_name
            )
        )
        p = Popen(['weasyprint', '--base-url', self.source_dir, '-', self.pdf_local_filename], stdin=PIPE)
        p.communicate(input=string)

        print "Generated certificate for user_id=%s" % (self.user_id,)

    def create(self):
        self.certificate_obj = GeneratedCertificate(
            user_id=self.user_id,
            course_id=self.course_id,
            grade=self.grade,
            status=self.certificate_status
        )
        if self.certificate_status == 'downloadable':
            self.certificate_obj.download_url = self.pdf_url_filename
        else:
            self.certificate_obj.download_url = ''
        self.certificate_obj.save()

    def update(self):
        self.certificate_obj.grade = self.grade
        if self.certificate_status == 'downloadable':
            self.certificate_obj.download_url = self.pdf_url_filename
        else:
            self.certificate_obj.download_url = ''
        self.certificate_obj.status = self.certificate_status
        self.certificate_obj.save()

    def process(self):

        if self.certificate_obj is None:
            print "Certificate object is created"
            self.create()

        else:

            if self.certsys.strategy == 'fail':
                raise CertificateError('Strategy is set to "fail". Certificate already exists for user_id=%s' % self.user_id)

            elif self.certsys.strategy == 'update':
                print "Certificate for user_id=%s is updated" % self.user_id
                self.update()

            elif self.certsys.strategy == 'ignore':
                pass

            else:
                raise CertificateError('Strategy is unknown. Certificate for user_id=%s exists' % self.user_id)

        if self.certsys.need_generate and self.certificate_status == 'downloadable':
            self.generate()

    @property
    def grade(self):
        return float(self.percent) / 100

    @property
    def course_sha1(self):
        return self._sha1(self.course_id)

    @property
    def user_sha1(self):
        return self._sha1(str(self.user_id))

    @property
    def pdf_relative_location(self):
        return "%s/%s" % (self.course_sha1, self.user_sha1)

    @property
    def pdf_url_location(self):
        return "%s/%s" % (self.certsys.url_prefix, self.pdf_relative_location)

    @property
    def pdf_url_filename(self):
        return "%s/%s" % (self.pdf_url_location, self.certsys.file_name)

    @property
    def pdf_local_location(self):
        return "%s/%s" % (self.certsys.storage_prefix, self.pdf_relative_location)

    @property
    def pdf_local_filename(self):
        return "%s/%s" % (self.pdf_local_location, self.certsys.file_name)

    def _sha1(self, str):
        return hashlib.sha1(str + self.certsys.secret).hexdigest()

    @property
    def certificate_status(self):
        return 'downloadable' if self.type in ['"Honor"', '"Simple"'] else 'notpassing'

    @property
    def student_name(self):
        user = User.objects.get(id=self.user_id)
        return user.profile.name

    @property
    def student_printed_name(self):
        return "<br/>".join(self.student_name.split(None, 1))
