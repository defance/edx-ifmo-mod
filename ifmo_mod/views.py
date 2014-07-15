from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from student import views as student_views
from edxmako.shortcuts import render_to_response

import logging
log = logging.getLogger(__name__)

from .utils import do_external_request


def partners(request):
    return render_to_response('partners.html')


def ant_external(request, course, unit, ssoid=None):
    """
    Register user for the ANT-course via api-request if ssoid is set. Then
    redirect user to the course page.
    """
    url = ''
    if ssoid is not None:
        try:
            url = "http://de.ifmo.ru/api/public/getCourseAccess?pid={0}&courseid={1}"
            url = url.format(ssoid, course)
            result = do_external_request(url)
            log.debug("User {0} registered for course {1} via ANT-api with responce: {2}".format(ssoid, course, result))

            test_url = ('http://de.ifmo.ru/IfmoSSO?redirect='
                        'http://de.ifmo.ru/servlet/%3FRule=EXTERNALLOGON%26COMMANDNAME=getCourseUnit%26'
                        'DATA=UNIT_ID={1}|COURSE_ID={0}').format(course, unit)
            log.debug(test_url)

            return HttpResponseRedirect(test_url)

        except Exception as e:
            log.error(ssoid)
            log.error(course)
            log.error("Failed to register user {0} for course {1} via ANT-api: {2}".format(ssoid, course, e))
    return HttpResponse('Failed to open ANT frame.')

@require_POST
def change_enrollment(request):
    """
    This change_enrollment overloads default one. When 'enroll' action is
    specified it tries to lookup in configuration whether some url for the
    enrolling course is set. If it is so, client is redirected to this url,
    otherwise standard action is executed and nothing changes.
    """
    # Execute original handler
    response = student_views.change_enrollment(request)

    action = request.POST.get("enrollment_action")
    course_id = request.POST.get("course_id")
    callback_url = None

    # Try to lookup redirect url for course if we are enrolling
    if action is not None and action == 'enroll':
        if course_id is not None:
            try:
                callback_url = settings.ENROLL_URL_CALLBACK[course_id]
            except Exception:
                log.debug('No url for course {0} is specified in configuration.'.format(course_id))

    # If url IS specified -- redirect there
    if callback_url is not None:
        return HttpResponse(callback_url)

    # Return original response
    return response
