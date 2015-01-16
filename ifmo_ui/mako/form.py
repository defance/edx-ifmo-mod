def text_input(context, id=None, name=None, placeholder=None, value=None, **kwargs):

    _ = lambda s, v: s % v if v is not None else u''

    params = {
        'id': _(u'id="%s"', id),
        'name': _(u'name="%s"', name),
        'placeholder': _(u'placeholder="%s"', placeholder),
        'value': _(u'value="%s"', value),
    }

    context.write(u"<input class='input' type='text' {id} {name} {placeholder} {value}/>".format(**params))
    return context


def li_text_input(context, id=None, name=None, value=None, placeholder=None, caption=None, help=None):

    context.write(u"<li class=''>")

    context.write(u"<label class=''>{caption}</label>".format(caption=caption))
    text_input(**locals())

    if help is not None:
        context.write(u"<span class='help'>{help}</span>".format(help=help))

    context.write(u"</li>")

    return context