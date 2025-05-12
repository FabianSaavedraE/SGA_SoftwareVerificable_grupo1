from app.models import Course

MAX_NAME_LENGTH = 50
MAX_DESCRIPTION_LENGTH = 100
MAX_CODE_LENGTH = 10

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
    elif len(code) > MAX_CODE_LENGTH:
        errors['code'] = (f"El código no puede superar los {MAX_CODE_LENGTH} "
                          f"caracteres")
    else:
        existing_course = Course.query.filter_by(code=code).first()
        if existing_course and (course_id is None or existing_course.id != course_id):
            errors['code'] = "El código ya está en uso por otro curso."

    try:
        credits = int(credits)
        if credits < 0:
            errors['credits'] = "Los créditos no pueden ser negativos."
    except ValueError:
        errors['credits'] = "Los créditos deber ser un número entero."

    return errors
