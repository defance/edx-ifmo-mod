from capa.inputtypes import InputTypeBase
from capa.correctmap import CorrectMap
from capa.responsetypes import LoncapaResponse

import requests

from ifmo_mod.utils import (get_current_ssoid, get_current_request, get_current_uri,)


class HTMLAcademy2Input(InputTypeBase):
    template = 'problems/htmlacademy/input_v2.html.mako'
    tags = ['htmlacademy2input']

    def setup(self):
        # FIXME Error handling if some fields missing
        self.description = self.xml.findtext('./description')
        self.course_name = self.xml.get('name')
        self.course_shortname = self.xml.get('shortname')
        self.course_element = self.xml.get('element')
        self.userid = get_current_ssoid()

    def _extra_context(self):
        return {
            'description': self.description,
            'course_name': self.course_name,
            'course_shortname': self.course_shortname,
            'course_element': self.course_element,
            'userid': self.userid,
        }


class HTMLAcademy2Response(LoncapaResponse):

    tags = ['htmlacademy2response']
    allowed_inputfields = ['htmlacademy2input']
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
        ext_responce = self.do_external_request(user, self.shortname)

        # If any error occurred -- we are done
        if isinstance(ext_responce, dict) and ext_responce.error is not None:
            return make_cmap(msg=ext_responce.error)

        # Find course we are checking
        for el in ext_responce:
            # FIXME Pretty brave assumption, make it error-prone
            if int(self.course_id) == el['course_number']:
                points_earned = float(el['tasks_completed']) / el['tasks_total'] * self.get_max_score()
                # Ew, gross!
                points_earned = round(points_earned * 100) / float(100)
                return make_cmap(status = 'correct', points=points_earned)

        return make_cmap()

    def get_answers(self):
        return {}

    @classmethod
    def do_external_request(cls, ssoid=0, shortname=''):

        # FIXME Hardcoded url
        url = 'http://htmlacademy.ru/api/get_progress?course={shortname}&ifmo_user_id={user}'.format(user=ssoid, shortname=shortname)

        try:
            req = requests.post(url)
        except Exception as err:
            msg = 'Cannot connect to HTMLAcademy: %s' % err
            log.error(msg)
            return json.loads('{\'error\': \'%s\'}' % msg)

        #if self.system.DEBUG:
        log.info('response = %s', req.text)

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
