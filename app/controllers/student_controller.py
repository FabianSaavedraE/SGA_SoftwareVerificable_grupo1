from io import BytesIO
from sqlalchemy import func

import pandas as pd

from app import db
from app.models import CourseSection, Schedule, Student, StudentCourses
from app.validators.data_load_validators import (
    validate_entry_can_be_loaded,
    validate_entry_has_required_keys,
    validate_json_has_required_key,
)

STUDENT_JSON_KEY = "alumnos"
CLOSED_STATE = "Closed"
REPORT_COLUMNS = [
    "Curso",
    "Año",
    "Semestre",
    "Sección",
    "Nota Final",
    "Estado",
]

KEY_ID_ENTRY = "id"
KEY_NAME_ENTRY = "nombre"
KEY_MAIL_ENTRY = "correo"
KEY_YEAR_ENTRY = "anio_ingreso"
KEYS_NEEDED_FOR_STUDENT_JSON = [
    KEY_ID_ENTRY,
    KEY_MAIL_ENTRY,
    KEY_NAME_ENTRY,
    KEY_YEAR_ENTRY,
]


def get_all_students():
    students = Student.query.all()
    return students


def get_student(student_id):
    student = Student.query.get(student_id)
    return student


def create_student(data):
    student_id = data.get('student_id')
    
    new_student = Student(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
        entry_year=data.get("entry_year"),
    )
    
    if student_id is not None:
        new_student.id = student_id

    db.session.add(new_student)
    db.session.commit()

    return new_student


def update_student(student, data):
    if not student:
        return None

    student.first_name = data.get("first_name", student.first_name)
    student.last_name = data.get("last_name", student.last_name)
    student.email = data.get("email", student.email)
    student.entry_year = data.get("entry_year", student.entry_year)

    db.session.commit()
    return student


def delete_student(student):
    if not student:
        return False

    db.session.delete(student)
    db.session.commit()
    return True


def are_students_available_for_timeslot(section, block):
    timeslot_ids = [timeslot.id for timeslot in block]
    students = section["section"].students

    if not students:
        return True

    student_ids = [student.id for student in students]
    current_section_id = section["section"].id

    conflicts = get_conflicting_schedules(timeslot_ids, student_ids, current_section_id)

    return len(conflicts) == 0


def get_conflicting_schedules(timeslots_id, students_id, current_section_id):
    return (
        Schedule.query.join(CourseSection)
        .join(CourseSection.student_courses)
        .filter(
            Schedule.time_slot_id.in_(timeslots_id),
            StudentCourses.student_id.in_(students_id),
            CourseSection.id != current_section_id,
        )
        .all()
    )


def create_students_from_json(data):
    if not validate_json_has_required_key(data, STUDENT_JSON_KEY):
        return None

    students = data.get("alumnos", [])

    # Validation cicle  (Will break if an entry it's not valid ----------------
    for student in students:
        if not validate_entry_has_required_keys(student, KEYS_NEEDED_FOR_STUDENT_JSON):
            return None

        if not validate_entry_can_be_loaded(
            transform_json_entry_into_processable_student_format(student),
            "student",
        ):
            return None

    # Creation cicle (Will only execute if ALL validations pass) -----------
    # (Thus, two for cicles are needed) ------------------------------------
    for student in students:
        id = student.get('id')
        student_data = transform_json_entry_into_processable_student_format(student)
        
        if check_if_student_with_id_exists(id):
            handle_student_with_existing_id(id)
        
        if student_data:
            create_student(student_data)
        else:
            break


def transform_json_entry_into_processable_student_format(student):
    name = student.get("nombre", "")
    data = {
        "first_name": name.split()[0] if isinstance(name, str) else name,
        "last_name": (
            " ".join(name.split()[1:])
            if (isinstance(name, str) and len(name.split()) > 1)
            else ("")
        ),
        "email": student.get("correo"),
        "entry_year": int(student.get("anio_ingreso")),
        "student_id":student.get("id")
    }
    return data


def check_if_student_with_id_exists(id):
    student = Student.query.filter_by(id=id).first()
    if student:
        return True
    else:
        return False


def handle_student_with_existing_id(id):
    student = Student.query.filter_by(id=id).first()
    max_id = db.session.query(func.max(Student.id)).scalar() or 0
    new_id = max_id + 1

    student.id = new_id
    db.session.commit()


def export_student_report_to_excel(student):
    records = generate_closed_course_records(student)
    excel_buffer = convert_records_to_excel(records)

    if excel_buffer is None:
        return None

    filename = f"{student.first_name}_{student.last_name}_reporte_notas.xlsx"
    return excel_buffer, filename


def generate_closed_course_records(student):
    closed_courses = []

    for enrollment in student.student_courses:
        section = enrollment.course_section

        if section is None or section.state != CLOSED_STATE:
            continue

        instance = section.course_instance
        course = instance.course

        closed_courses.append(
            {
                "Curso": course.name,
                "Año": instance.year,
                "Semestre": instance.semester,
                "Sección": section.nrc,
                "Nota Final": enrollment.final_grade,
                "Estado": enrollment.state,
            }
        )

    return sorted(closed_courses, key=lambda r: (r["Año"], r["Semestre"]))


def convert_records_to_excel(records):
    if not records:
        return None

    dataframe = pd.DataFrame(records, columns=REPORT_COLUMNS)
    excel_buffer = BytesIO()
    dataframe.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    return excel_buffer
