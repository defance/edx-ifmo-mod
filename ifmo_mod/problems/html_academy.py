from capa.inputtypes import InputTypeBase
from capa.correctmap import CorrectMap
from capa.responsetypes import LoncapaResponse

import requests

from ifmo_mod.utils import (get_current_ssoid, get_current_request, get_current_uri,)


class HTMLAcademyInput(InputTypeBase):
    template = 'problems/htmlacademy/input.html.mako'
    tags = ['htmlacademy']

    def setup(self):
        # FIXME Error handling if some fields missing
        self.m_title = self.xml.findtext('./title')
        self.m_description = self.xml.findtext('./description')
        self.m_course = self.xml.findtext('./course')
        self.m_userid = get_current_ssoid()
        self.m_htmlac_url = self.build_htmlacademy_url()

    @staticmethod
    def build_htmlacademy_url(course=0):
        base_url = 'http://htmlacademy.ru/basic_html_css/{0}'.format(course)
        result_url = base_url
        return result_url

    def _extra_context(self):
        return {
            'title': self.m_title,
            'description': self.m_description,
            'course': self.m_course,
            'userid': self.m_userid,
            'htmlacademy_url': self.m_htmlac_url
        }


class HTMLAcademyResponse(LoncapaResponse):

    tags = ['htmlacademyresponse']
    allowed_inputfields = ['htmlacademy']
    max_inputfields = 1

    def setup_response(self):
        self.answer_fields = self.inputfields[0]
        # FIXME Why must this be doubled here and in inputfields.py?
        self.course = self.answer_fields.xpath('//course')[0]

    def get_score(self, student_answers):

        def make_cmap(status='incorrect', points=0, msg=''):
            return CorrectMap(self.answer_id, status, npoints=points, msg=msg)

        # Get stat for current user
        user = get_current_ssoid()
        ext_response = self.do_external_request(user)

        # If any error occurred -- we are done
        if isinstance(ext_response, dict) and 'error' in ext_response:
            return make_cmap(msg=ext_response['error'])

        # Find course we are checking
        for el in ext_response:
            # FIXME Pretty brave assumption, make it error-prone
            if int(self.course.text) == el['course_number']:
                points_earned = float(el['tasks_completed']) / el['tasks_total'] * self.get_max_score()
                # Ew, gross!
                points_earned = round(points_earned * 100) / float(100)
                return make_cmap(status='correct', points=points_earned)

        return make_cmap()


    def get_answers(self):
        return {}

    @classmethod
    def do_external_request(cls, ssoid):

        # FIXME Hardcoded url
        url = 'http://htmlacademy.ru/api/get_progress?course=basic&ifmo_user_id={0}'.format(ssoid)

        try:
            req = requests.post(url)
        except Exception as err:
            msg = 'Cannot connect to HTMLAcademy: %s' % err
            log.error(msg)
            return json.loads('{\'error\': \'%s\'}' % msg)

        if (not req.text) or (not req.text.strip()):
            msg = 'Empty answer from HTMLAcademy.'
            log.error(msg)
            return json.loads('{\'error\': \'%s\'}' % msg)

        try:
            # response is JSON; parse it
            rjson = json.loads(req.text)
        except Exception as err:
            msg = 'Cannot parse response from HTMLAcademy.'
            msg_detailed = '{0}. Details:\n    error: {1},\n    data: {2}'.format(msg, err, req.text)
            log.error(msg_detailed)
            return json.loads('{\'error\': \'%s\'}' % msg)

        return rjson
