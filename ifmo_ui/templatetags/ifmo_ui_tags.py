from django import template
from ifmo_ui import mako

register = template.Library()


@register.simple_tag(name="ifmo_ui_text_input")
def text_input_tag(*args, **kwargs):
    return mako.form.text_input(MockContext(), **kwargs).get_data()


@register.simple_tag(name="ifmo_ui_form_li_text_input")
def ifmo_ui_form_li_text_input(*args, **kwargs):
    return mako.form.li_text_input(MockContext(), **kwargs).get_data()


class MockContext():

    def __init__(self):
        self._data = u''

    def write(self, data):
        self._data += data

    def get_data(self):
        return self._data