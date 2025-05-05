from app import db
from app.models.teacher import Teacher

MAX_LENGTH_FIRST_NAME = 50
MAX_LENGTH_LAST_NAME = 50
MAX_LENGTH_EMAIL = 50

def get_all_teachers():
    teachers = Teacher.query.all()
    return teachers

def get_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    return teacher

def create_teacher(data):
    errors = validate_teacher_data(data)
    if errors:
        return None, errors
    
    new_teacher = Teacher(
        first_name = data.get('first_name'),
        last_name = data.get('last_name'),
        email = data.get('email')
    )
    db.session.add(new_teacher)
    db.session.commit()

    return new_teacher, None

def update_teacher(teacher, data):
    if not teacher:
        return None

    teacher.first_name = data.get('first_name', teacher.first_name)
    teacher.last_name = data.get('last_name', teacher.last_name)
    teacher.email = data.get('email', teacher.email)

    db.session.commit()
    return teacher

def delete_teacher(teacher):
    if not teacher:
        return False

    db.session.delete(teacher)
    db.session.commit()
    return True

def validate_teacher_data(data):
    errors = []

    first_name = data.get('first_name', '').strip()
    if len(first_name) > MAX_LENGTH_FIRST_NAME:
        errors.append(
            f"El nombre es demasiado largo (máx. "
            f"{MAX_LENGTH_FIRST_NAME} caracteres)."
        )

    last_name = data.get('last_name', '').strip()
    if len(last_name) > MAX_LENGTH_LAST_NAME:
        errors.append(
            f"El apellido es demasiado largo (máx. "
            f"{MAX_LENGTH_LAST_NAME} caracteres)."
        )    

    email = data.get('email', '').strip()
    if len(email) > MAX_LENGTH_EMAIL:
        errors.append(
            f"El email es demasiado largo (máx. {MAX_LENGTH_EMAIL} caracteres)"
        )

    return errors
