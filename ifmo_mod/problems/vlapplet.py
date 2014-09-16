import json
import hashlib

from capa.inputtypes import InputTypeBase, Attribute
from capa.correctmap import CorrectMap
from capa.responsetypes import LoncapaResponse


class AppletSecuredStateException(Exception):
    pass


class AppletSecuredState:

    def __init__(self, data, secret=''):

        self._reset()

        if '' == data:
            return

        try:
            input_dict = json.loads(data)
            self.user_state = input_dict['userstate']
            self.variant = input_dict['variant']
            self.attempted = input_dict['attempted']
            if "true" == self.attempted:
                self.score = input_dict['score']
                self.display_message = input_dict['display_message']
                self.system_message = input_dict['system_message']
            self.hash = input_dict['hash']
            self.secret = secret

            if not self._hash_is_valid():
                self._reset()
                raise AppletSecuredStateException("Hash is not valid")

        except ValueError as error:
            self._reset()
            raise AppletSecuredStateException("Bad secured data: %s" % (error,))

    def _reset(self):
        self.user_state = ''
        self.variant = ''
        self.score = ''
        self.display_message = ''
        self.system_message = ''
        self.attempted = ''
        self.hash = ''
        self.secret = ''

    def _hash_is_valid(self):
        string = "".join([self.user_state, self.variant])
        if "true" == self.attempted:
            string = "".join([string, self.score, self.display_message, self.system_message])
        string = "".join([string, self.attempted, self.secret])
        hashed_string = hashlib.sha1(string).hexdigest()
        return hashed_string == self.hash


class VLAppletInput(InputTypeBase):
    template = 'problems/vlapplet.html.mako'
    tags = ['javaapplet']

    @classmethod
    def get_attributes(cls):
        """
        Register the attributes.
        """
        return [
            Attribute('width', 0),
            Attribute('height', 0),
            Attribute('archive', None),
            Attribute('code', None),
            Attribute('secret', render=False),
            Attribute('meta', ''),
        ]

    def setup(self):
        self.state = AppletSecuredState(self.value, secret=self.loaded_attributes['secret'])

    def _extra_context(self):
        return {
            'variant': self.state.variant,
            'user_state': self.state.user_state,
            'attempted': self.state.attempted,
            'hash': self._hash(),
        }

    def _hash(self):
        string = "".join([self.state.user_state, self.state.variant, self.state.attempted])
        if "debug" in self.loaded_attributes['meta']:
            string += "true"
        else:
            string += "false"
        string = "".join([string, self.loaded_attributes['meta'], self.state.secret])
        print string
        return hashlib.sha1(string).hexdigest()


class VLAppletResponse(LoncapaResponse):
    """
    Java applet.

    It must have getScore() method returning value between 0.0 and 1.0.
    Applet is to be uploaded via Content -> Files in edX Studio.

    Mark-up template:

    <problem>
        <javaappletresponse>
            <javaapplet height="100" width="100" archive="program.jar" code="my.class" secret="secret-string"/>
        </javaappletresponse>
    </problem>
    """

    tags = ['javaappletresponse']
    allowed_inputfields = ['javaapplet']
    max_inputfields = 1

    def setup_response(self):
        pass

    def get_score(self, student_answers):

        input_field = self.inputfields[0]
        state = AppletSecuredState(student_answers[self.answer_id], input_field.get('secret', ''))
        score = float(state.score)

        if score == 0:
            status = 'incorrect'
            message = 'You answer is incorrect.'
        elif score == 1:
            status = 'correct'
            message = 'Your answer is correct. Your total score: %.2f' % (score,)
        else:
            status = 'partial'
            message = 'Your answer is partially correct. Your total score: %.2f' % (score,)

        result = CorrectMap(self.answer_id, status, npoints=score, msg=message)

        return result

    def get_answers(self):
        return {}
