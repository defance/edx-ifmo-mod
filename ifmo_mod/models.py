from collections import defaultdict
from django.db.models import Count
from student.models import CourseEnrollment
from util.query import use_read_replica_if_available


class CourseEnrollmentExtension(object):

    @classmethod
    def enrollment_counts(cls, course_id, date):

        query = use_read_replica_if_available(CourseEnrollment.objects.filter(
            course_id=course_id,
            is_active=True,
            created__lte=date,
        ).values('mode').order_by().annotate(Count('mode')))
        total = 0
        enroll_dict = defaultdict(int)
        for item in query:
            enroll_dict[item['mode']] = item['mode__count']
            total += item['mode__count']
        enroll_dict['total'] = total
        return enroll_dict
