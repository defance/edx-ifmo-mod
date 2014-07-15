from capa.inputtypes import InputTypeBase
from capa.correctmap import CorrectMap
from capa.responsetypes import LoncapaResponse

from ifmo_mod.utils import (get_current_ssoid, do_external_request, )


class AcademicNTInput(InputTypeBase):
    template = 'problems/academicnt.html.mako'
    tags = ['academicntinput']

    def setup(self):
        self.m_courseid = self.xml.get('courseid')
        self.m_unitid = self.xml.get('unitid')
        self.m_description = self.xml.findtext('./description')
        self.m_ssoid = get_current_ssoid()

    def _extra_context(self):
        return {
            'courseid': self.m_courseid,
            'unitid': self.m_unitid,
            'description': self.m_description,
            'ssoid': self.m_ssoid,
        }


class AcademicNTResponse(LoncapaResponse):

    tags = ['academicntresponse']
    allowed_inputfields = ['academicntinput']
    max_inputfields = 1

    def setup_response(self):
        self.answer_fields = self.inputfields[0]
        # FIXME Why must this be doubled here and in inputfields.py?
        self.course = self.answer_fields.get('courseid')
        self.unit = self.answer_fields.get('unitid')

    def get_answers(self):
        return {}

    def get_score(self, student_answers):

        def make_cmap(status='incorrect', points=0, msg=''):
            return CorrectMap(self.answer_id, status, npoints=points, msg=msg)

        url = "http://de.ifmo.ru/api/public/getMark?pid={0}&courseid={1}&unitid={2}"
        url = url.format(get_current_ssoid(), self.course, self.unit)
        score = do_external_request(url)

        status = 'correct' if (score != 0) else 'incorrect'

        points_earned = float(score) / 100 * self.get_max_score()
        points_earned = round(points_earned * 100) / float(100)
        result = make_cmap(status=status, points=points_earned)

        return result
