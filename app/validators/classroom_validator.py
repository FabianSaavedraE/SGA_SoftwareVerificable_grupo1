from app.models import Classroom
MAX_NAME_LENGTH = 20
MIN_CAPACITY = 1
MAX_CAPACITY = 400
KEY_NAME_ENTRY = 'name'
KEY_CAPACITY_ENTRY = 'capacity'
KEY_ID_ENTRY = 'id'

def validate_classroom_data_and_return_errors(data, classroom_id=None):
    typing_errors = return_classroom_typing_errors(data)

    #Since typing errors are exclusive to JSON load, should return inmediatly.
    if typing_errors:
        return(typing_errors)
    
    attribute_errors = return_classroom_attribute_errors(data, classroom_id)

    return attribute_errors

def return_classroom_typing_errors(data):
    errors = {}
    name = data.get(KEY_NAME_ENTRY) or ''
    capacity = data.get(KEY_CAPACITY_ENTRY) or ''
    id = data.get(KEY_ID_ENTRY) or ''

    if not (isinstance(id, int) or (id == '')):
        errors[KEY_ID_ENTRY] = 'El id debe ser un int'
        
    if not isinstance(name, str):
        errors[KEY_NAME_ENTRY] = 'El nombre debe ser un string'

    if not (isinstance(capacity, str) or isinstance(capacity, int)):
        errors[KEY_CAPACITY_ENTRY] = 'La capacidad debe ser un int o un string'

    return errors

def return_classroom_attribute_errors(data, classroom_id):
    name = (data.get(KEY_NAME_ENTRY) or '').strip()
    capacity = data.get(KEY_CAPACITY_ENTRY) or ''
    if isinstance(capacity, str):
        capacity = capacity.strip()

    name_errors = return_classroom_name_errors(name, classroom_id)
    capacity_errors = return_classroom_capacity_errors(capacity)

    errors = {}
    errors.update(name_errors)
    errors.update(capacity_errors)
    return errors

def return_classroom_name_errors(name, classroom_id):
    errors = {}
    if not name:
        errors[KEY_NAME_ENTRY] = 'El nombre es obligatorio.'
    elif len(name) > MAX_NAME_LENGTH:
        errors[KEY_NAME_ENTRY] = (
            f'El nombre no puede superar los {MAX_NAME_LENGTH} caracteres.'
        )
    else:
        existing_classroom = Classroom.query.filter_by(
            name=name
        ).first()

        if existing_classroom and (
            classroom_id is None or existing_classroom.id != classroom_id
        ):
            errors[KEY_NAME_ENTRY] = f'Esta sala ya existe ({name}).'

    return errors

def return_classroom_capacity_errors(capacity):
    errors = {}
    if not capacity:
        errors[KEY_CAPACITY_ENTRY] = 'La capacidad es obligatoria.'
    else:
        try:
            capacity = int(capacity)
            if capacity < MIN_CAPACITY or capacity > MAX_CAPACITY:
                errors[KEY_CAPACITY_ENTRY] = (
                    f'La capacidad debe ser un valor entre '
                    f'{MIN_CAPACITY} y {MAX_CAPACITY}.'
                )
        except ValueError:
            errors[KEY_CAPACITY_ENTRY] = 'La capacidad debe ser un número entero.'
    return errors