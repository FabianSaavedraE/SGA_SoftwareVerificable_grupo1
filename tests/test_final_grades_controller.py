from app.controllers.final_grades_controller import (
    compute_student_final_grade, compute_type_average, get_student_grade
)

class MockStudent:
    def __init__(self, id):
        self.id = id

class MockEvaluation:
    def __init__(self, ponderation, optional=False, student_evaluations=None):
        self.ponderation = ponderation
        self.optional = optional
        self.student_evaluations = student_evaluations

class MockStudentEvaluation:
    def __init__(self, student_id, grade):
        self.student_id = student_id
        self.grade = grade

class MockEvaluationType:
    def __init__(
            self, overall_ponderation, ponderation_type, evaluations=None
        ):
        self.overall_ponderation = overall_ponderation
        self.ponderation_type = ponderation_type
        self.evaluations = evaluations or []

class MockCourseSection:
    def __init__(self, evaluation_types, overall_ponderation_type):
        self.evaluation_types = evaluation_types
        self.overall_ponderation_type = overall_ponderation_type

def test_get_student_grade_returns_correct_grade():
    student = MockStudent(1)
    evaluations = [
        MockStudentEvaluation(1, 6.0),
        MockStudentEvaluation(2, 5.0)
    ]
    evaluation = MockEvaluation(
        ponderation=30, student_evaluations=evaluations
    )

    grade = get_student_grade(evaluation, student)
    assert grade == 6.0

def test_get_student_grade_returns_none_if_not_found():
    student = MockStudent(3)
    evaluations = [
        MockStudentEvaluation(1, 6.0),
        MockStudentEvaluation(2, 5.0)
    ]
    evaluation = MockEvaluation(
        ponderation=30, student_evaluations=evaluations
    )

    grade = get_student_grade(evaluation, student)
    assert grade is None

def test_compute_type_average_with_percentages():
    student = MockStudent(1)
    evaluations = [
        MockEvaluation(ponderation=50, student_evaluations=[
            MockStudentEvaluation(1, 5.0)
        ]),
        MockEvaluation(ponderation=50, student_evaluations=[
            MockStudentEvaluation(1, 7.0)
        ])
    ]
    evaluation_type = MockEvaluationType(
        overall_ponderation=100,
        ponderation_type='Porcentaje',
        evaluations=evaluations
    )

    result = compute_type_average(student, evaluation_type)
    assert result == 6.0

def test_compute_type_average_skips_optional_with_no_grade():
    student = MockStudent(1)
    evaluations = [
        MockEvaluation(ponderation=100, optional=True, student_evaluations=[])
    ]
    evaluation_type = MockEvaluationType(
        overall_ponderation=100,
        ponderation_type='Porcentaje',
        evaluations=evaluations
    )

    result = compute_type_average(student, evaluation_type)
    assert result == 0

def test_compute_type_average_uses_min_grade_when_required_missing():
    student = MockStudent(1)
    evaluations = [
        MockEvaluation(ponderation=100, optional=False, student_evaluations=[])
    ]
    evaluation_type = MockEvaluationType(
        overall_ponderation=100,
        ponderation_type='Porcentaje',
        evaluations=evaluations
    )

    result = compute_type_average(student, evaluation_type)
    assert result == 1.0

def test_compute_student_final_grade_with_percentages():
    student = MockStudent(1)
    evaluation_type_1 = MockEvaluationType(
        overall_ponderation=40,
        ponderation_type='Porcentaje',
        evaluations=[
            MockEvaluation(ponderation=100, student_evaluations=[
                MockStudentEvaluation(1, 6.0)
            ])
        ]
    )

    evaluation_type_2 = MockEvaluationType(
        overall_ponderation=60,
        ponderation_type='Porcentaje',
        evaluations=[
            MockEvaluation(ponderation=100, student_evaluations=[
                MockStudentEvaluation(1, 4.0)
            ])
        ]
    )

    course_section = MockCourseSection(
        evaluation_types=[evaluation_type_1, evaluation_type_2],
        overall_ponderation_type='Porcentaje'
    )

    result = compute_student_final_grade(
        student, course_section, is_percentage=True
    )

    assert result == 4.8

def test_compute_student_final_grade_without_percentages():
    student = MockStudent(1)
    evaluation_type_1 = MockEvaluationType(
        overall_ponderation=2,
        ponderation_type='Peso',
        evaluations=[
            MockEvaluation(ponderation=1, student_evaluations=[
                MockStudentEvaluation(1, 5.0)
            ])
        ]
    )

    evaluation_type_2 = MockEvaluationType(
        overall_ponderation=1,
        ponderation_type='Peso',
        evaluations=[
            MockEvaluation(ponderation=1, student_evaluations=[
                MockStudentEvaluation(1, 3.0)
            ])
        ]
    )

    course_section = MockCourseSection(
        evaluation_types=[evaluation_type_1, evaluation_type_2],
        overall_ponderation_type='Peso'
    )

    result = compute_student_final_grade(
        student, course_section, is_percentage=False
    )

    assert result == 4.3