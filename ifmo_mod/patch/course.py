from xblock.fields import Scope, String
from xmodule.course_module import CourseFields, CourseDescriptor


def _property_author(self):
    return self.course_author


def patch():
    """
    Add field "course_author" to course information to be displayed on course index page.
    """
    CourseFields.course_author = String(
        display_name="Course Author",
        help="Original author of the course. This is provided bydd ifmo_mod.",
        scope=Scope.settings,
        default="",
    )
    CourseDescriptor.author = property(_property_author)
