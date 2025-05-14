from datetime import date

from app.models import Student

MAX_STRING_LENGTH = 50
MIN_VALID_ENTRY_YEAR = 1980
MAX_VALID_ENTRY_YEAR = 2025

FIELD_LABELS = {
    'first_name': 'nombre',
    'last_name': 'apellido'
}

def validate_student_data(data, student_id=None):
    errors = {}

    first_name = get_stripped_field(data, 'first_name')
    last_name = get_stripped_field(data, 'last_name')
    email = get_stripped_field(data, 'email')
    entry_year = get_stripped_field(data, 'entry_year')

    validate_name('first_name', first_name, errors)
    validate_name('last_name', last_name, errors)
    validate_email(email, student_id, errors)
    validate_entry_year(entry_year, errors)

    return errors

def get_stripped_field(data, field_name):
    return (str(data.get(field_name) or '')).strip()

def validate_name(field_name, value, errors):
    label = FIELD_LABELS.get(field_name, field_name)

    if not value:
        errors[field_name] = f'El {label} es obligatorio.'

    elif len(value) > MAX_STRING_LENGTH:
        errors[field_name] = (
            f'El {label} no puede superar los {MAX_STRING_LENGTH} caracteres.'
        )

def validate_email(email, student_id, errors):
    if not email:
        errors['email'] = 'El email es obligatorio.'

    elif len(email) > MAX_STRING_LENGTH:
        errors['email'] = (
            f'El email no puede superar los {MAX_STRING_LENGTH} caracteres.'
        )

    else:
        existing = Student.query.filter_by(email=email).first()

        if existing and (student_id is None or existing.id != student_id):
            errors['email'] = 'El email ya está en uso por otro estudiante.'

def validate_entry_year(entry_year, errors):
    if not entry_year:
        return
    
    if not entry_year.isdigit():
        errors['entry_year'] = 'El año de ingreso debe ser un número.'
        return

    year = int(entry_year)
    if year < MIN_VALID_ENTRY_YEAR or year > MAX_VALID_ENTRY_YEAR:
        errors['entry_year'] = (
            f'El año de ingreso debe estar entre {MIN_VALID_ENTRY_YEAR} y '
            f'{MAX_VALID_ENTRY_YEAR}.'
        )

def normalize_entry_year(year):
    try:
        year = int(year)
    except (ValueError, TypeError):
        year = date.today().year

    return max(MIN_VALID_ENTRY_YEAR, min(MAX_VALID_ENTRY_YEAR, year))
