def format_or_empty(format_str, param):
    return format_str % param if param is not None else u''
