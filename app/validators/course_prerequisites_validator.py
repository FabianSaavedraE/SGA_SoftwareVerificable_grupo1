from app.controllers.course_prerequisites_controllers import (
    get_course_prerequisite,
)
from app.models import CoursePrerequisite


def validate_prerequisites(course_id, prerequisite_ids):
    """Validate course prerequisites and returns any errors."""
    errors = {}

    if not course_id:
        errors["course_id"] = "Debe seleccionar un curso."

    if not prerequisite_ids:
        errors["prerequisite_ids"] = (
            "Debe seleccionar al menos un prerrequisito."
        )

    else:
        for prerequisite_id in prerequisite_ids:
            if is_self_reference(str(course_id), str(prerequisite_id)):
                errors["self_reference"] = (
                    "Un curso no puede ser prerrequisito de sí mismo."
                )
                break

            elif is_direct_cycle(int(course_id), int(prerequisite_id)):
                errors["cycle"] = (
                    "No se puede agregar este curso como prerrequisito porque "
                    "genera un ciclo directo."
                )
                break

            elif get_course_prerequisite(course_id, prerequisite_id):
                errors["duplicate"] = (
                    "La relación entre estos cursos ya existe."
                )
                break

    return errors


def is_direct_cycle(course_id, prerequisite_id):
    """Check if adding a prerequisite creates a direct cycle."""
    reversed_pair = CoursePrerequisite.query.filter_by(
        course_id=prerequisite_id, prerequisite_id=course_id
    ).first()

    return reversed_pair is not None


def is_self_reference(course_id, prerequisite_id):
    """Check if a course is set as its own prerequisite."""
    return course_id == prerequisite_id
