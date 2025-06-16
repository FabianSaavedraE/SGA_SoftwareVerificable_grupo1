import json
from flask import (
    redirect, flash, url_for
)
from app.validators.student_validator import validate_student_data
from app.validators.teacher_validator import validate_teacher_data
from app.validators.classroom_validator import (
    validate_classroom_data_and_return_errors
)


VALIDATORS = {
    'student': validate_student_data,
    'teacher': validate_teacher_data,
    'classroom': validate_classroom_data_and_return_errors
}
  
#Functions that validate the data loading process -----------------------------

def validate_json_file_and_return_processed_file(file):
    try:
        data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        flash('Error: Archivo no sigue un formato JSON válido', 'error')
        return None
    except Exception as e:
        flash('Error procesando archivo', 'error')
        return None
    
def validate_json_has_required_key(json_data, key):
    if key in json_data:
        return True
    else:
        flash(f'ERROR: Entrada "{key}" no encontrada en el JSON', 'error')
        return False
    
def validate_entry_has_required_keys(entry, keys :list): #Keys list should be
    #aggregated when one calls the funcion like this: [arg1, arg2, arg3...]
    has_all_keys = True
    for key in keys:
        has_all_keys = (
            has_all_keys and validate_json_has_required_key(entry,key)
        )
    if has_all_keys == False:
         flash('ERROR al crear JSON, faltan argumentos para inicializar '
                      'una instancia correctamente en la linea  '
                      f'{entry}', 'error')
         #Generalized flash message to understand WHERE the lacking atribute is
    return has_all_keys

def validate_entry_can_be_loaded(entry, type :str):
    validator = VALIDATORS.get(type)
    if validator:
        errors = validator(entry)
        if errors:
            for key in errors.keys():
                flash(f'ERROR para linea {entry}: En {key}: {errors[key]}',
                      'error')
            return False
    return True
