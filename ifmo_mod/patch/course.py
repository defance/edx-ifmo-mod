from xblock.fields import Scope, Field
from xmodule.course_module import CourseFields, CourseDescriptor


class AuthorField(Field):
    """
    Author field can contain string either in two forms:
     1. JSON array of strings
     2. anything other

    If string is in first form and valid -- this array is returned when obtaining value. Otherwise
    array [value] is returned.
    """
    def from_json(self, value):

        def is_list_of_basestring(data):
            if not isinstance(data, list):
                return False
            for i in data:
                if not isinstance(i, basestring):
                    return False
            return True

        if isinstance(value, basestring):
            return [value]

        elif is_list_of_basestring(value):
            return value

        else:
            raise TypeError('Author field can be String of List<String>, found %s' % type(value))

    enforce_type = from_json


def _property_author(self):
    return self.course_author


def patch():
    """
    Add field "course_author" to course information to be displayed on course index page.
    """
    CourseFields.course_author = AuthorField(
        display_name="Course Author",
        help="Original author of the course. Can be string or array of strings.",
        scope=Scope.settings,
        default=""
    )
    CourseDescriptor.author = property(_property_author)
