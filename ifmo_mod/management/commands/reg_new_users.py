# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from student.models import UserProfile, CourseEnrollment
from opaque_keys.edx.keys import CourseKey
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.exceptions import ItemNotFoundError

import codecs

class Command(BaseCommand):

    args = '-i <input_file> -c <course>'
    help = 'Register new users and enroll them on course'

    courses = {
        'x0009.00': 'ITMO/x0009.00/2014_10',  # 'php',
        'x0008.00': 'ITMO/x0008.00/2014_09',  # 'js',
        'x0007.00': 'ITMO/x0007.00/2014_10',  # 'основы робототехники',
        'x0005.01': 'ITMO/x0005.01/2014_09',  # 'практическая робототехника'
    }

    option_list = BaseCommand.option_list + (
        make_option('-i', '--input',
                    dest='input', default=None,
                    help=("CVS file with following lines: "
                         "<sso_id>,<last_name>,<first_name>,<middle_name>,<birth_date>,<sex>,<country>")),
        make_option('-o', '--output',
                    dest='output', default=None,
                    help=("CVS file with following lines: "
                         "<id>,<sso_id>")),
        make_option('-c', '--course',
                    dest='course', default=None,
                    help="Course one of following: %s" % courses.keys()),
    )

    report = {
        'registered': 0,
        'enrolled': 0,
    }

    @classmethod
    def get_sex_latin(cls, cyrillic):
        if cyrillic == 'М':
            return 'm'
        elif cyrillic == 'Ж':
            return 'f'
        else:
            return 'o'

    @classmethod
    def get_or_create_user(cls, source):

        (sso_id, last_name, first_name, middle_name, birth_date, sex, country, _) = source.split(';', 7)
        registered = False

        try:
            user = User.objects.get(username=sso_id)

        except User.DoesNotExist:
            user = User.objects.create(
                username=sso_id,
                last_name=last_name, first_name=first_name,
                email="%s@niuitmo.ru" % sso_id
            )

            profile = UserProfile.objects.create(
                user_id=user.id,
                name='%s %s %s' % (last_name, first_name, middle_name),
                location=country,
                gender=cls.get_sex_latin(sex),
                year_of_birth=birth_date.split(' ')[0].split('.')[-1]
            )

            user.save()
            profile.save()
            registered = True

        return user, registered

    @classmethod
    def enroll_user(cls, user, course_str):

        course_key = CourseKey.from_string(course_str)
        created = False

        try:
            course = modulestore().get_course(course_key)
        except ItemNotFoundError:
            raise CommandError("Course does not exist: %s" % course_str)

        try:
            enrollement = CourseEnrollment.objects.get(
                user=user,
                course_id=course_key
            )
        except CourseEnrollment.DoesNotExist:
            enrollement = CourseEnrollment.objects.create(
                user=user,
                course_id=course_key,
                mode="honor",
                is_active=True
            )
            created = True

        return created

    def handle(self, *args, **options):

        if options.get('course') is None:
            raise CommandError('Course is not specified.')

        if options.get('input') is None:
            raise CommandError('Input file is not specified.')

        if options.get('output') is None:
            raise CommandError('Output file is not specified.')

        try:
            with open(options.get('input'), 'r') as f, open(options.get('output'), 'w') as f2:
                for line in f:

                    user, registered = self.get_or_create_user(line)
                    f2.write("%s,%s\n" % (user.id, user.username))

                    if registered:
                        self.report['registered'] += 1

                    enrolled = self.enroll_user(user, options.get('course'))
                    if enrolled:
                        self.report['enrolled'] += 1

        except Exception as e:
            raise CommandError(e)

        print "Registered users: %(registered)s.\nEnrolled users: %(enrolled)s." % self.report
        print "All done."
