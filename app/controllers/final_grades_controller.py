from app.controllers.student_course_controller import (
    apply_final_grade,
    get_student_course,
)

PERCENTAGE = 'Porcentaje'
MINIMUM_GRADE = 1.0


def calculate_final_grades(course_section):
    if course_section is None:
        return

    is_percentage = course_section.overall_ponderation_type == PERCENTAGE

    for student in course_section.students:
        final_grade = compute_student_final_grade(
            student, course_section, is_percentage
        )

        update_student_final_grade(student.id, course_section.id, final_grade)


def compute_student_final_grade(student, course_section, is_percentage):
    total_weighted_scores = 0
    total_weights = 0

    for eval_type in course_section.evaluation_types:
        weighted_average = compute_type_average(student, eval_type)
        weight = eval_type.overall_ponderation or 0

        factor = (weight / 100) if is_percentage else weight
        total_weighted_scores += weighted_average * factor
        total_weights += factor

    if total_weights == 0:
        return 0

    final_grade = round(total_weighted_scores / total_weights, 1)
    return final_grade


def compute_type_average(student, evaluation_type):
    total_weighted_scores = 0
    total_weights = 0

    for evaluation in evaluation_type.evaluations:
        grade = get_student_grade(evaluation, student)
        if grade is None:
            if evaluation.optional:
                continue

            grade = MINIMUM_GRADE

        weight = evaluation.ponderation or 0

        is_percentage = evaluation_type.ponderation_type == PERCENTAGE
        factor = (weight / 100) if is_percentage else weight
        total_weighted_scores += grade * factor
        total_weights += factor

    if total_weights == 0:
        return 0

    average = total_weighted_scores / total_weights
    return round(average, 1)


def get_student_grade(evaluation, student):
    for student_eval in evaluation.student_evaluations:
        if student_eval.student_id == student.id:
            return student_eval.grade

    return None


def update_student_final_grade(student_id, course_section_id, final_grade):
    student_course = get_student_course(student_id, course_section_id)
    if student_course:
        apply_final_grade(student_course, final_grade)
