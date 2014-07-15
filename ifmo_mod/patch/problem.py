import capa.inputtypes as capa_input_types
import capa.responsetypes as capa_response_types


def _register_loncapa_problem_type(response_type=None, input_type=None):
    if response_type is not None:
        capa_response_types.registry.register(response_type)
    if input_type is not None:
        capa_input_types.registry.register(input_type)


def _register_loncapa_input_types():
    from ..problems import (
        html_academy, html_academy_v2, vlapplet, academicnt
    )
    new_problem_types = (
        (html_academy.HTMLAcademyResponse, html_academy.HTMLAcademyInput),
        (html_academy_v2.HTMLAcademy2Response, html_academy_v2.HTMLAcademy2Input),
        (vlapplet.VLAppletResponse, vlapplet.VLAppletInput),
        (academicnt.AcademicNTResponse, academicnt.AcademicNTInput),
    )
    for (problem_response, problem_input) in new_problem_types:
        _register_loncapa_problem_type(problem_response, problem_input)


def patch():
    _register_loncapa_input_types()
