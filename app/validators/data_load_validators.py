import json

from flask import flash

from app.validators.classroom_validator import (
    validate_classroom_data_and_return_errors,
)
from app.validators.course_instance_validator import (
    validate_course_instance_and_return_errors,
)
from app.validators.course_validator import (
    validate_course_data_and_return_errors,
)
from app.validators.student_course_validator import (
    validate_student_course_and_return_errors,
)
from app.validators.student_validator import (
    validate_student_data_and_return_errors,
)
from app.validators.teacher_validator import (
    validate_teacher_data_and_return_errors,
)

VALIDATORS = {
    "student": validate_student_data_and_return_errors,
    "teacher": validate_teacher_data_and_return_errors,
    "classroom": validate_classroom_data_and_return_errors,
    "course": validate_course_data_and_return_errors,
    "instance": validate_course_instance_and_return_errors,
    "student_course": validate_student_course_and_return_errors,
}

# Functions that validate the data loading process ----------------------------


def validate_json_file_and_return_processed_file(file):
    try:
        data = json.load(file)
        return data
    except json.JSONDecodeError:
        flash("Error: Archivo no sigue un formato JSON válido", "error")
        return None
    except Exception:
        flash("Error procesando archivo", "error")
        return None


def validate_json_has_required_key(json_data, key):
    if key in json_data:
        return True
    else:
        flash(f'ERROR: Entrada "{key}" no encontrada en el JSON', "error")
        return False


def validate_entry_has_required_keys(entry, keys: list):  # Keys list should be
    # aggregated when one calls the function like this: [arg1, arg2, arg3...]
    has_all_keys = True
    for key in keys:
        has_all_keys = has_all_keys and validate_json_has_required_key(
            entry, key
        )
    if not has_all_keys:
        flash(
            "ERROR al crear JSON, faltan argumentos para inicializar "
            "una instancia correctamente en la linea  "
            f"{entry}",
            "error",
        )
        # Generalized flash message to understand WHERE the lacking attribute
        # is
    return has_all_keys


def validate_entry_can_be_loaded(entry, type: str):
    validator = VALIDATORS.get(type)
    if validator:
        errors = validator(entry)
        if errors:
            for key in errors.keys():
                flash(
                    f"ERROR para linea {entry}: En {key}: {errors[key]}",
                    "error",
                )
            return False
    return True


def flash_custom_error(error):
    flash(f"ERROR {error}", error)
