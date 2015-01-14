from courseware.models import StudentModule
from django.core.management.base import BaseCommand, CommandError
from ifmo_mod.utils import do_external_request
from opaque_keys.edx.keys import CourseKey
from optparse import make_option
from student.models import CourseEnrollment
from xmodule.modulestore.django import modulestore
from xml.etree import ElementTree as ET
from xmodule.modulestore.exceptions import ItemNotFoundError

import json


class Command(BaseCommand):
    """
    The fix is pulling out AcademicNT grades. Some students are too lazy or something to click Check button
     after doing labs on AcademicNT. This one does not perform Check-click for themselves but does
     external request towards AcademicNT and pull out all scores available for all AcademicNT modules
     in the course.

    This is old-style AcademicNT blocks. It uses CapaProblem with xml markup and CapaResponseType as base,
     not XBlock.

    Overall algorithm:
     1. Get list of all modules in the course
     2. Detect whether this is AcademicNT module
     3. Make a call towards AcademicNT for this module params (like course_id)
     4. Update user score if it is needed

    Notice, that there is no chance to get date of AcademicNT task being completed. It can be completed past due.
    """

    option_list = BaseCommand.option_list + (
        make_option('-c', '--course',
                    dest='course', default=None,
                    help="Course id"),
        make_option('--save',
                    action='store_true',
                    dest='save_changes',
                    default=False,
                    help='Persist the changes that were encountered. If not set, no changes are saved.'),
    )

    url = "http://de.ifmo.ru/api/public/getMark?pid={sso_id}&courseid={course_id}&unitid={unit_id}"

    report = {
        'skipped': 0,
        'visited': 0,
        'not_started': 0,
        'changed': 0,
        'academic_calls': 0,
        'errors': 0
    }

    def get_academicnt_data(self, student_module):

        try:
            course_module = modulestore().get_item(student_module.module_state_key)
        except ItemNotFoundError:
            print "ItemNotFoundError: %s" % student_module.module_state_key
            return None

        try:
            data = ET.fromstring(course_module.data.encode('utf8'))
            node = data.findall('./academicntresponse/academicntinput')

            if len(node) is 0:
                return None

            if len(node) is not 1:
                raise CommandError('Some module has several academicntresponse/academicntinput fields.')

            return node[0].attrib

        except Exception as e:
            raise CommandError(e)

    def handle(self, *args, **options):

        print "Updating AcademicNT scores, strategy save_changes=%s" % options.get('save_changes')

        course_id = options.get('course')
        if course_id is None:
            raise CommandError('Course is not set.')

        course = CourseKey.from_string(course_id)

        # Get module list, we need only problem types
        modules = StudentModule.objects.filter(course_id=course, module_type='problem')

        # Iterate over all modules
        for module in modules:

            # if module.student.username != '148838':
            #     continue

            # Extract html academy modules only
            data = self.get_academicnt_data(module)
            if data is None:
                self.report['skipped'] += 1
                continue

            self.report['visited'] += 1
            # print "StudentModule id=%s user_id=%s user_username=%s" % (
            #     module.id, module.student.id, module.student.username
            # )
            need_save = False

            # Perform external request
            url = self.url.format(**{
                'sso_id': module.student.username,
                'course_id': data['courseid'],
                'unit_id': data['unitid']
            })
            score = do_external_request(url)
            self.report['academic_calls'] += 1

            # Try to cast response to float
            try:
                score = round(float(score))/float(100)
            except Exception:
                self.report['not_started'] += 1
                continue

            # Just skip zero-scored
            if score == 0:
                self.report['not_started'] += 1
                continue

            # Update all data
            if module.grade != score:
                module.grade = score
                need_save = True

            # Check field max_grade, it is needed to be displayed in progress
            if module.max_grade != 1:
                module.max_grade = 1
                need_save = True

            correctness = 'correct' if score == 100 else 'incorrect' if score == 0 else 'partial'

            # We need to add something to 'student_answers' and 'correct_map' for grade being visible
            state = json.loads(module.state)

            # We have already all inputs listed, update answers and map using this list
            for input_element in state['input_state'].keys():

                # Check existence of correct_map
                if 'correct_map' not in state:
                    state['correct_map'] = {}
                    need_save = True

                # If it is empty -- student has not tried
                if input_element not in state['correct_map']:
                    state['correct_map'] = {input_element: {'npoints': score, 'correctness': correctness}}
                    need_save = True

                # Otherwise -- just update score
                else:
                    cm = state['correct_map'][input_element]
                    old_score = cm.get('npoints', 0)
                    if old_score != score:
                        cm.update({'npoints': score, 'correctness': correctness})
                        need_save = True

                # Check existence of correct_map
                if 'student_answers' not in state:
                    state['student_answers'] = {}
                    need_save = True

                # Update student_answers, it can contain any dummy (looks like hack because of template bug)
                if input_element + "_course" not in state['student_answers']:
                    state['student_answers'] = {
                        input_element: 'graded-by-command',
                        input_element + "_course": 'graded-by-command'
                    }
                    need_save = True

            if need_save:
                print "Change module id={id} user_id={user_id} username={user_name} location={location}".format(**{
                    'id': module.id,
                    'user_id': module.student.id,
                    'user_name': module.student.username,
                    'location': module.module_state_key
                })
                self.report['changed'] += 1

            if options.get('save_changes') and need_save:
                module.state = json.dumps(state)
                module.save()

        print "All done: visited={visited} changed={changed} not_started={not_started} skipped={skipped} " \
              "htmlacademycalls={academic_calls}".format(**self.report)