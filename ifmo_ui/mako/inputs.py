from django.utils.html import escape
from ifmo_ui.mako.utils import *


def text_input(context, id=None, name=None, placeholder=None, value=None, **kwargs):

    params = {
        'id': format_or_empty(u'id="%s"', escape(id)),
        'name': format_or_empty(u'name="%s"', escape(name)),
        'placeholder': format_or_empty(u'placeholder="%s"', escape(placeholder)),
        'value': format_or_empty(u'value="%s"', escape(value)),
    }

    context.write(u"<input class='input' type='text' {id} {name} {placeholder} {value}/>".format(**params))
    return context


def text_area(context, id=None, name=None, placeholder=None, value=None, **kwargs):

    params = {
        'id': format_or_empty(u'id="%s"', escape(id)),
        'name': format_or_empty(u'name="%s"', escape(name)),
        'placeholder': format_or_empty(u'placeholder="%s"', escape(placeholder)),
        'value': format_or_empty(u'%s', escape(value)),
    }

    context.write(u"<textarea class='input' {id} {name} {placeholder} style='width:70%' rows='20'>{value}</textarea>".format(**params))
    return context