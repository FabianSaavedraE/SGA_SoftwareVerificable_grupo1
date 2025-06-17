from datetime import datetime

from app.models import CourseInstance
from app.models import Course
from app.validators.constants import(
    KEY_YEAR_ENTRY,  KEY_INSTANCE_COURSE_ID_JSON, KEY_SEMESTER_ENTRY,
    KEY_ID_ENTRY, MUST_BE_INT, MUST_BE_STRING, MUST_BE_STRING_OR_INT,
    MIN_VALID_ENTRY_YEAR, MUST_BE, OVERFLOWS, KEY_YEAR_JSON, DOESNT_EXIST,
    KEY_COURSE_ID_ENTRY, KEY_INSTANCE_ID_ENTRY
)

def validate_course_instance_and_return_errors(data, course_instance_id=None):
    typing_errors = return_instance_typing_errors(
        data
    )

    #Since typing errors are exclusive to JSON load, should return inmediatly.
    if typing_errors:
        return typing_errors

    attribute_errors = return_instance_attributes_errors(data)
    return attribute_errors

def return_instance_typing_errors(instance):
    errors = {}
    year = instance.get(KEY_YEAR_ENTRY) or ''
    semester = instance.get(KEY_SEMESTER_ENTRY) or ''
    course_id = instance.get(KEY_INSTANCE_COURSE_ID_JSON) or ''
    instance_id = instance.get(KEY_ID_ENTRY) or ''

    if not(isinstance(year,str) or isinstance(year,int)):
        errors[KEY_YEAR_ENTRY] = (
        f'{KEY_YEAR_ENTRY} {MUST_BE_STRING_OR_INT}'
        )

    if not(isinstance(semester,str) or isinstance(semester,int)):
        errors[KEY_SEMESTER_ENTRY] = (
        f'{KEY_SEMESTER_ENTRY} {MUST_BE_STRING_OR_INT}'
        )
    
    if not(
        isinstance(course_id,int) 
        or course_id == ""
        or isinstance(course_id,str)
        ):

        errors[KEY_INSTANCE_COURSE_ID_JSON] = (
            f'{KEY_INSTANCE_COURSE_ID_JSON} {MUST_BE_STRING_OR_INT}'
        )

    if not(isinstance(instance_id,int) or instance_id == ""):
        errors [KEY_ID_ENTRY] = (
            f'{KEY_ID_ENTRY} {MUST_BE_INT}'
        )

    return errors

def return_instance_attributes_errors(instance):
    errors = {}

    year = instance.get(KEY_YEAR_ENTRY) or ''
    semester = instance.get(KEY_SEMESTER_ENTRY) or ''
    course_id = instance.get(KEY_COURSE_ID_ENTRY) or ''
    instance_id = instance.get(KEY_INSTANCE_ID_ENTRY) or ''

    year_errors = return_instance_year_errors(year)
    semester_errors = return_instance_semester_errors(semester)
    course_id_errors = return_instance_course_id_errors(course_id)

    errors.update(year_errors)
    errors.update(semester_errors)
    errors.update(course_id_errors)
    
    return errors

def return_instance_year_errors(year):
    errors = {}

    if not year:
        errors[KEY_YEAR_ENTRY] = f'{KEY_YEAR_ENTRY} {MUST_BE}'
        return errors

    if isinstance(year,str):
        try:
            year = int(year)
        except:
            errors[KEY_YEAR_ENTRY]= f'{KEY_YEAR_ENTRY} {MUST_BE_INT}'
            return errors

    if not (MIN_VALID_ENTRY_YEAR <= year <= int(datetime.now().year)):
        errors[KEY_YEAR_ENTRY] = (
            f'{KEY_YEAR_ENTRY} {OVERFLOWS}'
            f' {MIN_VALID_ENTRY_YEAR} - {datetime.now().year} {KEY_YEAR_JSON}s'
        )

    return errors

def return_instance_semester_errors(semester):
    errors = {}
    
    if not semester:
        errors[KEY_SEMESTER_ENTRY] = f'{KEY_SEMESTER_ENTRY} {MUST_BE}'
        return errors

    if isinstance(semester,str):
        try:
            semester = int(semester)
        except:
            errors[KEY_SEMESTER_ENTRY] = f'{KEY_SEMESTER_ENTRY} {MUST_BE_INT}'
            return errors

    if semester not in [1,2]:
        errors[KEY_SEMESTER_ENTRY] = f'{KEY_SEMESTER_ENTRY} {OVERFLOWS} 1-2'

    return errors

def return_instance_course_id_errors(course_id):
    errors = {}
    if not course_id:
        errors[KEY_INSTANCE_COURSE_ID_JSON] = (
            f'{KEY_INSTANCE_COURSE_ID_JSON} {MUST_BE}'
        )
        return errors
    if isinstance(course_id, str):
        try:
            course_id = int(course_id)
        except:
            errors[KEY_INSTANCE_COURSE_ID_JSON] = (
                f'{KEY_INSTANCE_COURSE_ID_JSON} {MUST_BE_INT}'
            )
            return errors
    
    if not Course.query.get(course_id):
        errors[KEY_INSTANCE_COURSE_ID_JSON] = (
            f'{KEY_INSTANCE_COURSE_ID_JSON} {course_id} {DOESNT_EXIST}'
        )
    
        
    return errors

def return_instance_id_errors(instance_id):
    errors = {}
    
    if not instance_id:
        errors[KEY_ID_ENTRY] = (
            f'{KEY_ID_ENTRY} {MUST_BE}'
        )
        return errors
    
    if isinstance(instance_id, str):
        try:
            instance_id = int(instance_id)
        except:
            errors[KEY_ID_ENTRY] = (
                f'{KEY_ID_ENTRY} {MUST_BE_INT}'
            )
    
    return errors

'''
Chiara don't know what this does, please fix!
def validate_course_instance_uniqueness_and_return_errors(
    year, semester, course_instance_id, course_id, errors
):
    if not course_id and course_instance_id:
        course_instance = CourseInstance.query.get(course_instance_id)
        if course_instance:
            course_id = course_instance.course_id

    if not errors.get('year') and not errors.get('semester') and course_id:
        existing_instance = CourseInstance.query.filter_by(
            course_id=course_id,
            year=year,
            semester=semester
        ).filter(CourseInstance.id != course_instance_id).first()

        if existing_instance:
            errors['exists'] = (
                f'Ya existe una instancia de este curso para {year}-{semester}.'
            )
'''

def get_stripped_field(data, field):
    return (str(data.get(field) or '')).strip()
