from app.models import Course

from app.validators.constants import(
    COURSE_CODE_PREFIX, CODE_LENGTH, MAX_DESCRIPTION_LENGTH,
    MIN_CREDITS_VALUE, MAX_CREDITS_VALUE, KEY_NAME_ENTRY, OVERFLOWS,
    KEY_DESCRIPTION_ENTRY, KEY_CODE_ENTRY, KEY_CREDITS_ENTRY, CHARACTERS,
    KEY_COURSE_ID_ENTRY, MUST_BE, MUST_BE_INT, MUST_BE_STRING, MUST_BE_STRING_OR_INT,
    ALREADY_EXISTS
)

def validate_course_data_and_return_errors(data, course_id=None):
    #Since typing errors are exclusive to JSON load, should return inmediatly.
    typing_errors = return_course_typing_errors(data)
    if typing_errors:
        return typing_errors

    attributes_errors = return_course_attributes_errors(data, course_id)
    return attributes_errors

def return_course_typing_errors(data):
    errors = {}
    name = data.get(KEY_NAME_ENTRY) or ''
    description = data.get(KEY_DESCRIPTION_ENTRY) or ''
    code = data.get(KEY_CODE_ENTRY) or ''
    raw_credits = data.get(KEY_CREDITS_ENTRY) or ''
    id = data.get(KEY_COURSE_ID_ENTRY) or ''

    if not (isinstance(id, int) or (id == '')):
        errors[KEY_COURSE_ID_ENTRY] = f'{KEY_COURSE_ID_ENTRY} {MUST_BE_INT}'
        
    if not isinstance(name, str):
        errors[KEY_NAME_ENTRY] = f'{KEY_NAME_ENTRY} {MUST_BE_STRING}'

    if not isinstance(description, str):
        errors[KEY_DESCRIPTION_ENTRY] = (
            f'{KEY_DESCRIPTION_ENTRY} {MUST_BE_STRING}'
            )
    if not (isinstance(code, str) or isinstance(code,int)):
        errors[KEY_CODE_ENTRY] = f'{KEY_CODE_ENTRY} {MUST_BE_STRING_OR_INT}'

    if not (isinstance(raw_credits, int) or (isinstance (raw_credits, str))):
        errors[KEY_CREDITS_ENTRY] = (
            f'{KEY_CREDITS_ENTRY} {MUST_BE_STRING_OR_INT}'
        )
    
    return errors

def return_course_attributes_errors(data, course_id):
    errors = {}

    name = data.get(KEY_NAME_ENTRY) or ''
    description = data.get(KEY_DESCRIPTION_ENTRY) or ''
    code = data.get(KEY_CODE_ENTRY) or ''
    raw_credits = data.get(KEY_CREDITS_ENTRY) or ''

    text_errors = return_text_field_errors(
        KEY_NAME_ENTRY, name
        )
    description_errors = return_text_field_errors(
        KEY_DESCRIPTION_ENTRY, description
        )
    code_errors = return_course_code_errors(
        code, course_id
    )
    credit_errors = return_credits_errors(
        raw_credits
    )

    errors.update(text_errors)
    errors.update(description_errors)
    errors.update(code_errors)
    errors.update(credit_errors)

    return errors

def return_text_field_errors(key, text):
    errors = {}

    if not text or text == "" or text == '':
        errors[key] = f'{key} {MUST_BE}'

    elif len(text) > MAX_DESCRIPTION_LENGTH:
        errors[key] = (
            f'{key} {OVERFLOWS} 1 - {MAX_DESCRIPTION_LENGTH} {CHARACTERS}.'
        )

    return errors

def return_course_code_errors(code, course_id):
    errors = {}

    if not code or code == "" or code == "":
        errors[KEY_CODE_ENTRY] = f'{KEY_CODE_ENTRY} {MUST_BE}'
        return errors

    if isinstance(code, str):
        if code.startswith("ICC"):
            #Remove for case JSON has ICC preloaded in the code
            code = code[3:]
        if len(code) != CODE_LENGTH or not code.isdigit():
            errors[KEY_CODE_ENTRY] = (
            f'{KEY_CODE_ENTRY} {OVERFLOWS} {CODE_LENGTH} {CHARACTERS}'
            )
            return errors
        
    full_code = f'{COURSE_CODE_PREFIX}{code}'
    existing = Course.query.filter_by(code=full_code).first()

    if existing and (course_id is None or existing.id != course_id):
        errors[KEY_CODE_ENTRY] = f'{KEY_CODE_ENTRY} {ALREADY_EXISTS}'
    
    return errors

def return_credits_errors(credits):
    errors = {}
    if isinstance(credits,str):
        try:
            credits = int(credits)
        except:
            errors[KEY_CREDITS_ENTRY] = f'{KEY_CREDITS_ENTRY} {MUST_BE_STRING}'
            return errors
    if not (MIN_CREDITS_VALUE <= credits <= MAX_CREDITS_VALUE):
                errors[KEY_CREDITS_ENTRY] = (
                    f'{KEY_CREDITS_ENTRY} {OVERFLOWS} '
                    f' {MIN_CREDITS_VALUE} - {MAX_CREDITS_VALUE}.'
                )

    return errors

def validate_and_return_prerequisite_if_course_exists(prerequisite):
    course = Course.query.filter_by(code = prerequisite).first()
    if course:
        return course
    return False
    


    