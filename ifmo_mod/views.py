from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views.decorators.http import require_POST
from edxmako.shortcuts import render_to_response
from instructor.views.api import require_level
from student import views as student_views
from student.models import CourseEnrollment
from opaque_keys.edx.keys import CourseKey
from xmodule.modulestore.django import modulestore

from datetime import datetime
import json
import logging
log = logging.getLogger(__name__)

from .models import CourseEnrollmentExtension
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


def summary(request):
    """
    Get course summary, as: course_id, display_name, start_date and enrolled_users.
    :param request:
    :return:
    """
    if not request.user.is_superuser:
        return HttpResponseNotFound()

    return render_to_response('summary.html')


@require_level('staff')
def summary_handler(request):

    courses = modulestore().get_courses()
    courses = sorted(courses, key=lambda x: x.start, reverse=True)
    courses = [{
        'id': unicode(i.id),
        'display_name': "%s %s" % (i.id.course, i.display_name),
        'start': i.start.strftime('%d/%m/%Y'),
        'enrollments': [
            {
                'date': date,
                'data': CourseEnrollmentExtension.enrollment_counts(i.id, datetime.strptime(date, "%d/%m/%Y"))
            } for date in request.GET.getlist('dates[]')
        ]
    } for i in courses]

    return HttpResponse(json.dumps({
        'dates': request.GET.getlist('dates[]'),
        'courses': courses
    }))


@require_level('staff')
def date_check(request, course_id):

    row = '<tr><td>%s</td>%s%s</tr>'
    date_cell = '<td class="%(status)s">%(date)s</td>'

    def get_date(date):
        return date.strftime('%d/%m/%Y %H:%M') if date is not None else 'N/A'

    def date_correct_start(date):
        status = 'date-error'
        if date is None:
            status = 'date-na'
        elif all([date.isoweekday() == 7, date.hour == 21, date.minute == 0, date.second == 0]):
            status = 'date-ok'
        return {
            'date': get_date(date),
            'status': status
        }

    def date_correct_due(date):
        status = 'date-error'
        if date is None:
            status = 'date-na'
        elif all([date.isoweekday() == 7, date.hour == 21, date.minute == 0, date.second == 0]):
            status = 'date-ok'
        return {
            'date': get_date(date),
            'status': status
        }

    def build_children(children, res, depth=0):

        for i in children:

            i = modulestore().get_item(i)
            res.append(row % ('<span class="tab"></span>' * depth + i.display_name_with_default,
                              date_cell % date_correct_start(i.start),
                              date_cell % date_correct_due(i.due)))

            if i.has_children and i.children is not None and len(i.children):
                build_children(i.children, res, depth + 1)

    course_key = CourseKey.from_string(course_id)
    course = modulestore().get_course(course_key)

    rows = []
    build_children(course.children, rows)

    return render_to_response('date_check.mako', {
        'course_id': course_id,
        'course_name': course.display_name_with_default,
        'content': '<table>%s</table>' % "".join(rows),
    })