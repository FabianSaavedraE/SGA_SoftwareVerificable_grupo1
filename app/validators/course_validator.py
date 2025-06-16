from app.models import Course

COURSE_CODE_PREFIX = 'ICC'
CODE_LENGTH = 4
MAX_NAME_LENGTH = 50
MAX_DESCRIPTION_LENGTH = 100
MIN_CREDITS_VALUE = 1
MAX_CREDITS_VALUE = 4


def validate_course_data(data, course_id=None):
    errors = {}

    name = get_stripped_field(data, 'name')
    description = get_stripped_field(data, 'description')
    code = get_stripped_field(data, 'code')
    raw_credits = get_stripped_field(data, 'credits')

    validate_text_field('name', name, MAX_NAME_LENGTH, errors)
    validate_text_field(
        'description', description, MAX_DESCRIPTION_LENGTH, errors
    )
    validate_course_code(code, course_id, errors)
    validate_credits(raw_credits, errors)

    return errors


def get_stripped_field(data, field):
    return (str(data.get(field) or '')).strip()


def validate_text_field(field_name, value, max_length, errors):
    if not value:
        field_display = 'nombre' if field_name == 'name' else 'descripción'
        errors[field_name] = f'El atributo {field_display} es obligatorio.'

    elif len(value) > max_length:
        field_display = 'nombre' if field_name == 'name' else 'descripción'
        errors[field_name] = (
            f'El atributo {field_display} no puede superar los {max_length} '
            f'caracteres.'
        )


def validate_course_code(code, course_id, errors):
    if not code:
        errors['code'] = 'El código es obligatorio.'

    elif len(code) != CODE_LENGTH or not code.isdigit():
        errors['code'] = (
            f'El código debe ser un número de {CODE_LENGTH} dígitos.'
        )
    else:
        full_code = f'{COURSE_CODE_PREFIX}{code}'
        existing = Course.query.filter_by(code=full_code).first()
        if existing and (course_id is None or existing.id != course_id):
            errors['code'] = 'El código ya está en uso por otro curso.'


def validate_credits(credits, errors):
    try:
        value = int(credits)
        if not MIN_CREDITS_VALUE <= value <= MAX_CREDITS_VALUE:
            errors['credits'] = (
                f'El valor de los créditos debe ser entre '
                f'{MIN_CREDITS_VALUE} y {MAX_CREDITS_VALUE}.'
            )
    except ValueError:
        errors['credits'] = 'Los créditos deben ser un número entero.'
