from django import template

import ifmo_ui.mako.form as ifmo_form
import ifmo_ui.mako.inputs as ifmo_inputs

register = template.Library()


@register.simple_tag(name="ifmo_ui_text_input")
def text_input_tag(*args, **kwargs):
    return ifmo_inputs.text_input(MockContext(), **kwargs).get_data()


@register.simple_tag(name="ifmo_ui_form_li_text_input")
def ifmo_ui_form_li_text_input(*args, **kwargs):
    return ifmo_form.li_text_input(MockContext(), **kwargs).get_data()


@register.simple_tag(name="ifmo_ui_text_area")
def ifmo_ui_text_area(*args, **kwargs):
    return ifmo_inputs.text_area(MockContext(), **kwargs).get_data()


@register.simple_tag(name="ifmo_ui_form_li_text_area")
def ifmo_ui_form_li_text_area(*args, **kwargs):
    return ifmo_form.li_text_area(MockContext(), **kwargs).get_data()


class MockContext():

    def __init__(self):
        self._data = u''

    def write(self, data):
        self._data += data

    def get_data(self):
        return self._data