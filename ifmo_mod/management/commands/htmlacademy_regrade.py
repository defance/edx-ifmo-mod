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
    The fix is pulling out HTML Academy grades. Some students are too lazy or something to click Check button
     after doing courses on HTML Academy. This one does not perform Check-click for themselves but does
     external request towards HTML academy and pull out all scores available for all HTML academy modules
     in the course.

    This is old-style HTML Academy blocks. It uses CapaProblem with xml markup and CapaResponseType as base,
     not XBlock.

    Overall algorithm:
     1. Get list of all modules in the course
     2. Detect whether this is HTML academy module
     3. Make a call towards HTML Academy for this module params (like course_id)
     4. Update user score if it is needed

    Notice, that there is no chance to get date of HTML Academy task being completed. It can be completed past due.
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

    url = 'https://htmlacademy.ru/api/get_progress?course=%s&ifmo_user_id=%s'

    report = {
        'skipped': 0,
        'visited': 0,
        'not_started': 0,
        'changed': 0,
        'htmlacademy_calls': 0
    }

    htmlacademy_cache = {}

    def get_htmlacademy_data(self, input):

        try:
            module = modulestore().get_item(input.module_state_key)
        except ItemNotFoundError:
            print "ItemNotFoundError: %s" % input.module_state_key
            return None

        try:
            data = ET.fromstring(module.data.encode('utf8'))
            node = data.findall('./htmlacademyresponse/htmlacademyinput')

            if len(node) is 0:
                return None

            if len(node) is not 1:
                raise CommandError('Some module has several htmlacademyresponse/htmlacademyinput fields.')

            return node[0].attrib

        except Exception as e:
            raise CommandError(e)

    def handle(self, *args, **options):

        def get_element_data(courses_data, course_number):
            for i in courses_data:
                if str(i['course_number']) == course_number:
                    return i
            return None

        print "Updating HTML academy scores, strategy save_changes=%s" % options.get('save_changes')

        course_id = options.get('course')
        if course_id is None:
            raise CommandError('Course is not set.')

        course = CourseKey.from_string(course_id)

        # Get module list, we need only problem types
        modules = StudentModule.objects.filter(course_id=course, module_type='problem')

        # Iterate over all modules
        for module in modules:

            # Extract html academy modules only
            data = self.get_htmlacademy_data(module)
            if data is None:
                self.report['skipped'] += 1
                continue

            self.report['visited'] += 1
            print "StudentModule id=%s user_id=%s user_username=%s" % (
                module.id, module.student.id, module.student.username
            )
            need_save = False

            # Perform some cache here, minimize html-academy url calls
            cache_key = (data['shortname'], module.student.username)

            # Try obtain server response from cache
            if cache_key in self.htmlacademy_cache:
                htmlacademy_data = self.htmlacademy_cache[cache_key]

            # Otherwise perform external request
            else:
                htmlacademy_url = self.url % cache_key
                response = do_external_request(htmlacademy_url)
                self.report['htmlacademy_calls'] += 1
                # Parse data
                try:
                    htmlacademy_data = json.loads(response)
                except Exception:
                    # User is probably not registered
                    htmlacademy_data = None

                self.htmlacademy_cache[cache_key] = htmlacademy_data

            # If we have no data from html academy -- skip this module
            if htmlacademy_data is None:
                self.report['not_started'] += 1
                continue

            # Extract specific course element
            element_data = get_element_data(htmlacademy_data, data['element'])

            # Calculate new score
            new_score = element_data['tasks_completed']/float(element_data['tasks_total'])
            correctness = 'incorrect' if new_score is 0 else 'correct' if new_score is 1.0 else 'partial'

            # Update all data
            if module.grade != new_score:
                module.grade = new_score
                need_save = True

            # Check field max_grade, it is needed to be displayed in progress
            if module.max_grade != 1.0:
                module.max_grade = 1.0
                need_save = True

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
                    state['correct_map'] = {input_element: {'npoints': new_score, 'correctness': correctness}}
                    need_save = True

                # Otherwise -- just update score
                else:
                    cm = state['correct_map'][input_element]
                    old_score = cm.get('npoints', 0)
                    if old_score != new_score:
                        cm.update({'npoints': new_score, 'correctness': correctness})
                        need_save = True

                # Check existence of correct_map
                if 'student_answers' not in state:
                    state['student_answers'] = {}
                    need_save = True

                # Update student_answers, it can contain any dummy
                if input_element not in state['student_answers']:
                    state['student_answers'] = {input_element: 'graded-by-command'}
                    need_save = True

            if need_save:
                self.report['changed'] += 1

            if options.get('save_changes') and need_save:
                module.state = json.dumps(state)
                module.save()

        print "All done: visited={visited} changed={changed} not_started={not_started} skipped={skipped} " \
              "htmlacademycalls={htmlacademy_calls}".format(**self.report)