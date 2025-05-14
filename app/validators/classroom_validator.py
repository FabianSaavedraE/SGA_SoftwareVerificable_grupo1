from app.models import Classroom

MAX_NAME_LENGTH = 20
MIN_CAPACITY = 1
MAX_CAPACITY = 400

def validate_classroom_data(data, classroom_id=None):
    errors = {}

    name = (data.get('name') or '').strip()
    capacity = (data.get('capacity') or '').strip()

    if not name:
        errors['name'] = 'El nombre es obligatorio.'
    elif len(name) > MAX_NAME_LENGTH:
        errors['name'] = (
            f'El nombre no puede superar los {MAX_NAME_LENGTH} caracteres.'
        )
    else:
        existing_classroom = Classroom.query.filter_by(
            name=name
        ).first()

        if existing_classroom and (
            classroom_id is None or existing_classroom.id != classroom_id
        ):
            errors['name'] = f'Esta sala ya existe ({name}).'

    if not capacity:
        errors['capacity'] = 'La capacidad es obligatoria.'
    elif capacity:
        try:
            capacity = int(capacity)
            if capacity < MIN_CAPACITY or capacity > MAX_CAPACITY:
                errors['capacity'] = (
                    f'La capacidad debe ser un valor entre '
                    f'{MIN_CAPACITY} y {MAX_CAPACITY}.'
                )
        except ValueError:
            errors['capacity'] = 'La capacidad debe ser un número entero.'

    return errors
