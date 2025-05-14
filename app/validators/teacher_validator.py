from app.models import Teacher

MAX_LENGTH_FIRST_NAME = 50
MAX_LENGTH_LAST_NAME = 50
MAX_LENGTH_EMAIL = 50

def validate_teacher_data(data, teacher_id=None):
    errors = {}

    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    email = data.get('email', '').strip()

    if not first_name:
        errors['first_name'] = 'El nombre es obligatorio.'
    elif len(first_name) > MAX_LENGTH_FIRST_NAME:
        errors['first_name'] = (
            f'El nombre no puede superar los {MAX_LENGTH_FIRST_NAME} '
            f'caracteres.'
        )
        
    if not last_name:
        errors['last_name'] = 'El apellido es obligatorio.'  
    elif len(last_name) > MAX_LENGTH_LAST_NAME:
        errors['last_name'] = (
            f'El apellido no puede superar los {MAX_LENGTH_LAST_NAME} '
            f'caracteres.'
        ) 

    if not email:
        errors['email'] = 'El email es obligatorio.'
    elif len(email) > MAX_LENGTH_EMAIL:
        errors['email'] = (
            f'El email no puede superar los {MAX_LENGTH_EMAIL} caracteres.'
        )
    else:
        existing_teacher = Teacher.query.filter_by(email=email).first()
        if existing_teacher and (
            teacher_id is None or existing_teacher.id != teacher_id
        ):
            errors['email'] = 'El email ya está en uso por otro profesor.'

    return errors
