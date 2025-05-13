from app.models import Course

MAX_NAME_LENGTH = 50
MAX_DESCRIPTION_LENGTH = 100
CODE_LENGTH = 4
MAX_CREDITS_VALUE = 30

def validate_course_data(data, course_id=None):
    errors = {}

    name = (data.get('name') or '').strip()
    description = (data.get('description') or '').strip()
    code = (data.get('code') or '').strip()
    credits = (data.get('credits') or '').strip()

    if not name:
        errors['name'] = "El nombre es obligatorio."
    elif len(name) > MAX_NAME_LENGTH:
        errors['name'] = (f"El nombre no puede superar los {MAX_NAME_LENGTH} "
                          f"caracteres")

    if not description:
        errors['description'] = "La descripción es obligatoria."
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        errors['description'] = (f"La descripción no puede superar los "
                                 f"{MAX_DESCRIPTION_LENGTH} caracteres")

    if not code:
        errors['code'] = "El código es obligatorio."
    elif len(code) != CODE_LENGTH:
        errors['code'] = (f"El código debe ser un número de {CODE_LENGTH} "
                          f"dígitos")
    else:
        existing_course = Course.query.filter_by(
            code=f"ICC-{code}"
        ).first()
        if existing_course and (
            course_id is None or existing_course.id != course_id
        ):
            errors['code'] = "El código ya está en uso por otro curso."

    try:
        credits = int(credits)
        print("CREDITS:", credits)
        if credits < 0 or credits > MAX_CREDITS_VALUE:
            errors['credits'] = (f"El valor de los créditos debe ser entre "
                                 f"0-{MAX_CREDITS_VALUE}")
    except ValueError:
        errors['credits'] = "Los créditos deber ser un número entero."

    return errors
