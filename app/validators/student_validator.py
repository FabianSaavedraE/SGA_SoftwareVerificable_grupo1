from app.models import Student

MAX_LENGTH_FIRST_NAME = 50
MAX_LENGTH_LAST_NAME = 50
MAX_EMAIL_LENGTH = 50
MIN_ENTRY_YEAR = 1980
MAX_ENTRY_YEAR = 2025

def validate_student_data(data, student_id=None):
    errors = {}

    first_name = (data.get('first_name') or '').strip()
    last_name = (data.get('last_name') or '').strip()
    email = (data.get('email') or '').strip()
    entry_year = (data.get('entry_year') or '').strip()

    if not first_name:
        errors['first_name'] = "El nombre es obligatorio."
    elif len(first_name) > MAX_LENGTH_FIRST_NAME:
        errors['first_name'] = (f"El nombre no puede superar los "
                                f"{MAX_LENGTH_FIRST_NAME} caracteres.")

    if not last_name:
        errors['last_name'] = "El apellido es obligatorio."  
    elif len(last_name) > MAX_LENGTH_LAST_NAME:
        errors['last_name'] = (f"El apellido no puede superar los "
                               f"{MAX_LENGTH_LAST_NAME} caracteres.") 

    if not email:
        errors['email'] = "El email es obligatorio."
    elif len(email) > MAX_EMAIL_LENGTH:
        errors['email'] = (f"El email no puede superar los {MAX_EMAIL_LENGTH} "
                           f"caracteres.")
    else:
        existing_student = Student.query.filter_by(email=email).first()
        if existing_student and (
            student_id is None or existing_student.id != student_id
        ):
            errors['email'] = "El email ya está en uso por otro estudiante."

    if entry_year:
        if not entry_year.isdigit():
            errors['entry_year'] = "El año de ingreso debe ser un número."
        else:
            year = int(entry_year)
            if year < MIN_ENTRY_YEAR or year > MAX_ENTRY_YEAR:
                errors['entry_year'] = (
                    f"El año de ingreso debe ser entre {MIN_ENTRY_YEAR} y "
                    f"{MAX_ENTRY_YEAR}.")

    return errors
