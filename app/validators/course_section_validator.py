from app.models import CourseSection

NRC_LENGTH = 4


def validate_course_section(data, course_section_id=None):
    """Validate course section data and returns any errors."""
    errors = {}

    nrc = get_stripped_field(data, "nrc")

    validate_nrc(nrc, course_section_id, errors)

    return errors


def get_stripped_field(data, field):
    """Return a stripped string from form data."""
    return (str(data.get(field) or "")).strip()


def validate_nrc(nrc, course_section_id, errors):
    """Validate the NRC for a course section."""
    if not nrc:
        errors["nrc"] = "El NRC es obligatorio."
    elif len(nrc) != NRC_LENGTH:
        errors["nrc"] = f"El NRC debe ser un número de {NRC_LENGTH} dígitos."
    else:
        existing_section = CourseSection.query.filter_by(
            nrc=f"NRC{nrc}"
        ).first()

        if existing_section and (
            course_section_id is None
            or existing_section.id != course_section_id
        ):
            errors["nrc"] = f"El NRC ({nrc}) ya está en uso por otra sección."


def validate_evaluation_types_warning(course_section):
    """Check if overall evaluation type ponderations sum to 100%."""
    warning_evaluation_types = None
    if course_section.overall_ponderation_type == "Porcentaje":
        total_ponderation_of_evaluation_types = round(
            sum(
                evaluation_type.overall_ponderation
                for evaluation_type in course_section.evaluation_types
            ),
            2,
        )

        if total_ponderation_of_evaluation_types < 100:
            warning_evaluation_types = (
                f"Suma actual de ponderaciones de tipos: "
                f"{total_ponderation_of_evaluation_types}%. "
                f"Falta completar hasta 100%."
            )

    return warning_evaluation_types


def validate_evaluations_warning(course_section):
    """Check if evaluations within each type sum to 100%."""
    warning_evaluations = {}
    for evaluation_type in course_section.evaluation_types:
        if evaluation_type.ponderation_type == "Porcentaje":
            total_ponderation_of_evaluations = round(
                sum(
                    (evaluation.ponderation or 0)
                    for evaluation in evaluation_type.evaluations
                ),
                2,
            )

            if total_ponderation_of_evaluations < 100:
                warning_evaluations[evaluation_type.id] = (
                    f'Falta ponderar instancias de "{evaluation_type.topic}": '
                    f"{total_ponderation_of_evaluations}% (meta 100%)."
                )

    return warning_evaluations
