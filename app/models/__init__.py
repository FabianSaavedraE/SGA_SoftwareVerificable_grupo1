"""Models package: imports all database models for easy access."""

from .classroom import Classroom as Classroom
from .course import Course as Course
from .course_instance import CourseInstance as CourseInstance
from .course_prerequisite import CoursePrerequisite as CoursePrerequisite
from .course_section import CourseSection as CourseSection
from .evaluation import Evaluation as Evaluation
from .evaluation_type import EvaluationType as EvaluationType
from .schedule import Schedule as Schedule
from .student import Student as Student
from .student_course import StudentCourses as StudentCourses
from .student_evaluation import StudentEvaluations as StudentEvaluations
from .teacher import Teacher as Teacher
from .timeslot import TimeSlot as TimeSlot

__all__ = [
    "Classroom",
    "Course",
    "CourseInstance",
    "CoursePrerequisite",
    "CourseSection",
    "Evaluation",
    "EvaluationType",
    "Schedule",
    "Student",
    "StudentCourses",
    "StudentEvaluations",
    "Teacher",
    "TimeSlot",
]
