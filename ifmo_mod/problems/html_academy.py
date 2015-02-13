import json
import requests

from capa.inputtypes import InputTypeBase, Attribute
from capa.correctmap import CorrectMap
from capa.responsetypes import LoncapaResponse, ResponseError
from ifmo_mod.utils import get_current_ssoid


class HTMLAcademyInput(InputTypeBase):
    template = 'problems/htmlacademy.html.mako'
    tags = ['htmlacademyinput']

    @classmethod
    def get_attributes(cls):
        return [
            Attribute('name', None),
            Attribute('shortname', None),
            Attribute('element', None),
            Attribute('userid', None),
        ]


class HTMLAcademyResponse(LoncapaResponse):

    tags = ['htmlacademyresponse']
    allowed_inputfields = ['htmlacademyinput']
    max_inputfields = 1

    academy_url = 'https://htmlacademy.ru/api/get_progress?course={shortname}&ifmo_user_id={user}'

    def setup_response(self):
        input_field = self.inputfields[0]
        input_field.set('userid', get_current_ssoid())

    def get_score(self, student_answers):

        # Here can be a cycle to have several html academies inputs, now we have only one
        input_id = self.answer_ids[0]

        input_field = {
            'user': student_answers[input_id + '_user'],
            'name': student_answers[input_id + '_name'],
            'shortname': student_answers[input_id + '_shortname'],
            'element': student_answers[input_id + '_element'],
        }

        # Do request towards html academy
        ext_response = self.do_external_request(input_field['user'], input_field['shortname'])

        points_earned = 0

        # Find course we are checking
        for el in ext_response:
            # FIXME Pretty brave assumption, make it error-prone
            if int(input_field['element']) == el['course_number']:
                # Ew, gross!
                points_earned = float(el['tasks_completed']) / el['tasks_total'] * self.get_max_score()
                points_earned = round(points_earned * 100) / float(100)
                break

        msg = "Your total score: %s" % (points_earned,)
        status = 'incorrect' if points_earned == 0 else 'correct' if points_earned == 1 else 'partially'

        return CorrectMap(self.answer_id, status, npoints=points_earned, msg=msg)

    def get_answers(self):
        return {}

    @classmethod
    def do_external_request(cls, ssoid=0, shortname=''):

        # FIXME Hardcoded url
        url = cls.academy_url.format(user=ssoid, shortname=shortname)
        try:
            request = requests.post(url)
        except Exception:
            raise ResponseError('Cannot connect to HTMLAcademy')

        if (not request.text) or (not request.text.strip()):
            raise ResponseError('Empty answer from HTMLAcademy')

        try:
            response_json = json.loads(request.text)
        except Exception:
            raise ResponseError('Cannot parse response from HTMLAcademy')

        return response_json
