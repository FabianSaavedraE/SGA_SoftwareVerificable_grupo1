from unittest.mock import patch, MagicMock

from app.controllers import student_controller as controller

class MockStudent:
    def __init__(self, id):
        self.id = id
        self.student_courses = []

class MockEnrollment:
    def __init__(self, course_section, final_grade=5, state='Closed'):
        self.course_section = course_section
        self.final_grade = final_grade
        self.state = state

class MockCourse:
    def __init__(self, name):
        self.name = name

class MockCourseInstance:
    def __init__(self, year, semester, course):
        self.year = year
        self.semester = semester
        self.course = course

class MockSection:
    def __init__(self, nrc, state, course_instance):
        self.nrc = nrc
        self.state = state
        self.course_instance = course_instance

def test_are_students_available_for_timeslot_no_students():
    section = {'section': MagicMock(students=[])}
    block = [MagicMock(id=1)]
    assert (
        controller.are_students_available_for_timeslot(section, block) is True
    )

@patch('app.controllers.student_controller.get_conflicting_schedules')
def test_are_students_available_for_timeslot_conflict(mock_conflicts):
    section_obj = MagicMock()
    section_obj.students = [MagicMock(id=1), MagicMock(id=2)]
    section = {'section': section_obj}
    block = [MagicMock(id=1), MagicMock(id=2)]

    mock_conflicts.return_value = [MagicMock()]

    result = controller.are_students_available_for_timeslot(section, block)
    assert result is False
    mock_conflicts.assert_called_once()

@patch('app.controllers.student_controller.get_conflicting_schedules')
def test_are_students_available_for_timeslot_no_conflict(mock_conflicts):
    section_obj = MagicMock()
    section_obj.students = [MagicMock(id=1)]
    section = {'section': section_obj}
    block = [MagicMock(id=1)]

    mock_conflicts.return_value = []

    result = controller.are_students_available_for_timeslot(section, block)
    assert result is True

def test_generate_closed_course_records_and_sort():
    course = MockCourse('Diseño de Software Verificable')
    instance = MockCourseInstance(2023, 1, course)
    section_closed = MockSection('A', 'Closed', instance)
    section_open = MockSection('B', 'Open', instance)

    enrollment1 = MockEnrollment(section_closed, 6, 'Closed')
    enrollment2 = MockEnrollment(section_open, 7, 'Open')

    student = MockStudent(1)
    student.student_courses = [enrollment2, enrollment1]

    records = controller.generate_closed_course_records(student)
    assert len(records) == 1
    assert records[0]['Curso'] == 'Diseño de Software Verificable'
    assert records[0]['Año'] == 2023

def test_convert_records_to_excel_none():
    result = controller.convert_records_to_excel([])
    assert result is None
