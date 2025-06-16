"""
This .py file it's used to run queries. Similar to the Rails Console -using
this analogy since it's the only web development framework we studied
officially at UANDES- it will run the queries here written when called from
console. To do this, it needs to access the specific tables and structure.
"""

from app import create_app
from app.models.course import Course
from app.models.course_prerequisite import CoursePrerequisite
from app.models.course_section import CourseSection
from app.models.student import Student
from app.models.teacher import Teacher

# The app needs to be created for consultations
app = create_app()

with app.app_context():
    # Query for all existing courses.

    print('Cursos existentes:')
    cursos = Course.query.all()
    for curso in cursos:
        print(f'- {curso.id}: {curso.name}')

    print('Profesores existentes:')
    profesores = Teacher.query.all()
    for profesor in profesores:
        print(f'- {profesor.id}: {profesor.first_name} {profesor.last_name}')

    # Query for all existing students:

    print('\nEstudiantes existentes:')
    estudiantes = Student.query.all()
    for est in estudiantes:
        print(est)

    print('\nPares de prerrequisitos:')
    prerequisites = CoursePrerequisite.query.all()
    for prerequisite in prerequisites:
        print(
            f'{prerequisite.course.name} requires '
            f'{prerequisite.prerequisite.name}'
        )

    print('\nSecciones existentes:')
    secciones = CourseSection.query.all()
    for seccion in secciones:
        teacher = Teacher.query.get(seccion.teacher_id)
        teacher_name = (
            f'{teacher.first_name} {teacher.last_name}'
            if teacher
            else 'Sin profesor asignado'
        )
        print(
            f'- ID: {seccion.id}, NRC: {seccion.nrc}, Tipo de ponderación: '
            f'{seccion.overall_ponderation_type}, '
            f'Estado: {seccion.state}, ID instancia curso: '
            f'{seccion.course_instance_id}, Profesor: {teacher_name}'
        )
