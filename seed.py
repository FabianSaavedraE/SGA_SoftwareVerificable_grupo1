# seed.py

from app import create_app, db
from app.models.student import Student
from app.models.course import Course
from app.models.course_section import CourseSection
from app.models.teacher import Teacher

app = create_app()

with app.app_context():
    # Reiniciar base de datos: eliminar y recrear todas las tablas
    db.drop_all()
    db.create_all()
    print("Base de datos reiniciada (tablas eliminadas y recreadas).")

    # Crear 5 estudiantes independientes
    nuevos_estudiantes = [
        Student(first_name="Sofía", last_name="Gómez", email="sofia.gomez@example.com"),
        Student(first_name="Ignacio", last_name="Pérez", email="ignacio.perez@example.com"),
        Student(first_name="Camila", last_name="Rojas", email="camila.rojas@example.com"),
        Student(first_name="Benjamín", last_name="Torres", email="benjamin.torres@example.com"),
        Student(first_name="Fernanda", last_name="Molina", email="fernanda.molina@example.com")
    ]
    db.session.add_all(nuevos_estudiantes)
    db.session.commit()
    print("5 estudiantes creados con éxito.")

    # Crear 5 cursos
    nuevos_cursos = [
        Course(name="Matemáticas I"),
        Course(name="Programación Avanzada"),
        Course(name="Física General"),
        Course(name="Bases de Datos"),
        Course(name="Inteligencia Artificial")
    ]
    db.session.add_all(nuevos_cursos)
    db.session.commit()
    print("5 cursos creados con éxito.")

    # Crear un profesor
    profesor = Teacher(first_name="Claudia", last_name="Valdés", email="claudia.valdes@example.com")
    db.session.add(profesor)
    db.session.commit()
    print("Profesor de ejemplo creado.")

    # Crear 5 secciones, una por cada curso
    cursos = Course.query.all()
    nuevas_secciones = []
    for i, curso in enumerate(cursos):
        seccion = CourseSection(
            nrc=f"NRC00{i+1}",
            semester="2025-1",
            course_id=curso.id,
            teacher_id=profesor.id
        )
        nuevas_secciones.append(seccion)

    db.session.add_all(nuevas_secciones)
    db.session.commit()
    print("5 secciones creadas con éxito.")
