from django.utils.html import escape
from .inputs import *


def li_text_input(context, id=None, name=None, value=None, placeholder=None, caption=None, help=None):

    context.write(u"<li class=''>")

    context.write(u"<label class=''>{caption}</label>".format(caption=escape(caption)))
    text_input(**locals())

    if help is not None:
        context.write(u"<span class='help'>{help}</span>".format(help=help))

    context.write(u"</li>")

    return context


def li_text_area(context, id=None, name=None, value=None, placeholder=None, caption=None, help=None):

    context.write(u"<li class=''>")

    context.write(u"<label class=''>{caption}</label>".format(caption=caption))
    text_area(**locals())

    if help is not None:
        context.write(u"<span class='help'>{help}</span>".format(help=help))

    context.write(u"</li>")

    return context