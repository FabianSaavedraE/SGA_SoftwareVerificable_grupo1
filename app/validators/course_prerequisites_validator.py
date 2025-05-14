from app.models import CoursePrerequisite
from app.controllers.course_prerequisites_controllers import (
    get_course_prerequisite
)

def validate_prerequisites(course_id, prerequisite_ids):
    errors = {}

    if not course_id:
        errors['course_id'] = 'Debe seleccionar un curso.'

    if not prerequisite_ids:
        errors['prerequisite_ids'] = (
            f'Debe seleccionar al menos un prerequisito.'
        )

    else:
        for prereq_id in prerequisite_ids:
            if is_self_reference(str(course_id), str(prereq_id)):
                errors['self_reference'] = (
                    f'Un curso no puede ser prerequisito de sí mismo.'
                )
                break

            elif is_direct_cycle(int(course_id), int(prereq_id)):
                errors['cycle'] = (
                    f'No se puede agregar este curso como prerequisito porque '
                    f'genera un ciclo directo.'
                )
                break

            elif get_course_prerequisite(course_id, prereq_id):
                errors['duplicate'] = (
                    f'La relación entre estos cursos ya existe.'
                )
                break

    return errors

def is_direct_cycle(course_id, prerequisite_id):
    reversed_pair = CoursePrerequisite.query.filter_by(
        course_id=prerequisite_id,
        prerequisite_id=course_id
    ).first()

    return reversed_pair is not None

def is_self_reference(course_id, prerequisite_id):
    return course_id == prerequisite_id
