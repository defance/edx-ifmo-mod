from capa.inputtypes import InputTypeBase
from capa.correctmap import CorrectMap
from capa.responsetypes import LoncapaResponse, ResponseError

import json
import requests

from ifmo_mod.utils import (get_current_ssoid, get_current_request, get_current_uri,)


class HTMLAcademyInput(InputTypeBase):
    template = 'problems/htmlacademy/input.html.mako'
    tags = ['htmlacademyinput']

    def setup(self):
        self.course_name = self.xml.get('name')
        self.course_shortname = self.xml.get('shortname')
        self.course_element = self.xml.get('element')
        self.userid = get_current_ssoid()

    def _extra_context(self):
        return {
            'course_name': self.course_name,
            'course_shortname': self.course_shortname,
            'course_element': self.course_element,
            'userid': self.userid,
        }


class HTMLAcademyResponse(LoncapaResponse):

    tags = ['htmlacademyresponse']
    allowed_inputfields = ['htmlacademyinput']
    max_inputfields = 1

    def setup_response(self):
        self.answer_fields = self.inputfields[0]
        # FIXME Why must this be doubled here and in inputfields.py?
        self.course_id = self.answer_fields.get('element')
        self.shortname = self.answer_fields.get('shortname')

    def get_score(self, student_answers):

        def make_cmap(status='incorrect', points=0, msg=''):
            return CorrectMap(self.answer_id, status, npoints=points, msg=msg)

        # Get stat for current user
        user = get_current_ssoid()
        ext_response = self.do_external_request(user, self.shortname)

        # If any error occurred -- we are done
        if isinstance(ext_response, dict) and 'error' in ext_response:
            return make_cmap(msg=ext_response['error'])

        # Find course we are checking
        for el in ext_response:
            # FIXME Pretty brave assumption, make it error-prone
            if int(self.course_id) == el['course_number']:
                points_earned = float(el['tasks_completed']) / el['tasks_total'] * self.get_max_score()
                # Ew, gross!
                points_earned = round(points_earned * 100) / float(100)
                return make_cmap(status='correct', points=points_earned)

        return make_cmap()

    def get_answers(self):
        return {}

    @classmethod
    def do_external_request(cls, ssoid=0, shortname=''):

        # FIXME Hardcoded url
        url = 'http://htmlacademy.ru/api/get_progress?course={shortname}&ifmo_user_id={user}'.format(user=ssoid, shortname=shortname)
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
