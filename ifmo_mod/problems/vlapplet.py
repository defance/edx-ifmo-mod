from capa.inputtypes import InputTypeBase
from capa.correctmap import CorrectMap
from capa.responsetypes import LoncapaResponse


class VLAppletInput(InputTypeBase):
    template = 'problems/vlapplet.html.mako'
    tags = ['vlapplet']

    height = 0
    width = 0
    archive = None
    code = None
    description = None

    def setup(self):

        import logging
        log = logging.getLogger(__name__)
        log.error("setup vlapplet")

        self.description = self.xml.findtext('./description')
        self.height = self.xml.findtext('./height')
        self.width = self.xml.findtext('./width')
        self.archive = self.xml.findtext('./archive')
        self.code = self.xml.findtext('./code')

        if self.archive is None or self.code is None:
            raise ValueError(
                'Error while reading attributes "archive" and/or "code" for <applet/>'
            )

    def _extra_context(self):
        return {
            'height': self.height,
            'width': self.width,
            'archive': self.archive,
            'code': self.code,
            'description': self.description
        }


class VLAppletResponse(LoncapaResponse):
    """
    Java applet.

    It must have getScore() method returning value between 0.0 and 1.0.
    Applet is to be uploaded via Content -> Files in edX Studio.

    Mark-up template:

    <problem>
        <vlappletresponse>
            <vlapplet>
                <title>Test applet</title>
                <description>This is test applet.</description>
                <width>540</width>
                <height>320</height>
                <archive>/static/usolcev-test.jar</archive>
                <code>Test.class</code>
            </vlapplet>
        </vlappletresponse>
    </problem>
    """

    tags = ['vlappletresponse']
    allowed_inputfields = ['vlapplet']
    max_inputfields = 1

    def setup_response(self):
        self.answer_fields = self.inputfields[0]

    def get_score(self, student_answers):

        def make_cmap(status='incorrect', points=0, msg=''):
            return CorrectMap(self.answer_id, status, npoints=points, msg=msg)

        result = make_cmap()

        try:
            result.set_property(self.answer_id, 'npoints', float(student_answers[self.answer_id+'_score']))
            result.set_property(self.answer_id, 'correctness', 'correct')
        except ValueError:
            result.msg = 'Error in result handling.'

        return result

    def get_answers(self):
        return {}
