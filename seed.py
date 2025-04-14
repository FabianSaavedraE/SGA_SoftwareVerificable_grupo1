import random
from app import create_app, db
from app.models.student import Student
from app.models.course import Course
from app.models.course_instance import CourseInstance
from app.models.course_section import CourseSection
from app.models.teacher import Teacher
from app.models.course_prerequisite import CoursePrerequisite

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database reset (tables dropped and recreated).")

    # ---------- Estudiantes ----------
    nombres = ["Sofía", "Ignacio", "Camila", "Benjamín", "Fernanda", "Joaquín", "Martina", "Matías", "Antonia", "Diego", "Chiara", "Fabián", "Vicente"]
    apellidos = ["Gómez", "Pérez", "Rojas", "Torres", "Molina", "Navarro", "Ramírez", "Silva", "Morales", "Castillo", "Romanini", "Acevedo", "Saavedra"]

    estudiantes = []
    used_emails = set()

    while len(estudiantes) < 30:
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        email_base = f"{nombre.lower()}.{apellido.lower()}@miuandes.cl"
        email = email_base
        count = 1
        while email in used_emails:
            email = f"{nombre.lower()}.{apellido.lower()}{count}@miuandes.cl"
            count += 1
        used_emails.add(email)

        estudiante = Student(first_name=nombre, last_name=apellido, email=email)
        estudiantes.append(estudiante)

    db.session.add_all(estudiantes)
    db.session.commit()
    print("30 estudiantes creados.")

    # ---------- Profesores ----------
    profesores_data = [
        ("Matías", "Recabarren", "matias.recabarren@miuandes.cl"),
        ("Jorge", "Gómez", "jorge.gomez@miuandes.cl"),
        ("Claudio", "Álvarez", "claudio.alvarez@miuandes.cl"),
        ("Eduardo", "Peters", "eduardo.peters@miuandes.cl"),
        ("Miguel", "Canales", "miguel.canales@miuandes.cl"),
    ]

    profesores = [Teacher(first_name=fn, last_name=ln, email=mail) for fn, ln, mail in profesores_data]
    db.session.add_all(profesores)
    db.session.commit()
    print("5 profesores creados.")

    # ---------- Cursos ----------
    cursos_nombres = [
        "Matemáticas I", "Matemáticas II", "Programación", "Estructuras de Datos", "Bases de Datos",
        "Sistemas Operativos", "Algoritmos", "Redes de Computadores", "Inteligencia Artificial",
        "Machine Learning", "Cálculo Numérico", "Probabilidades", "Física", "Compiladores",
        "Ingeniería de Software", "Desarrollo Web", "Sistemas Distribuidos", "Arquitectura de Computadores",
        "Criptografía", "Robótica"
    ]

    cursos = [Course(name=nombre, description="Curso de " + nombre, code=f"C-{i+100}") for i, nombre in enumerate(cursos_nombres)]
    db.session.add_all(cursos)
    db.session.commit()
    print("20 cursos creados.")

    # ---------- Course Instances y Secciones ----------
    profesores = Teacher.query.all()
    secciones = []

    for curso in cursos:
        # Crea una instancia del curso
        instancia = CourseInstance(
            year=2025,
            semester=1,
            course_id=curso.id
        )
        db.session.add(instancia)
        db.session.commit()

        # Crea una sección asociada a la instancia
        profesor = random.choice(profesores)
        seccion = CourseSection(
            nrc=f"NRC{instancia.id + 1000}",
            overall_ponderation_type=random.choice(["Porcentaje", "Peso"]),
            course_instance_id=instancia.id,
            teacher_id=profesor.id
        )
        secciones.append(seccion)

    db.session.add_all(secciones)
    db.session.commit()
    print("Instancias y secciones creadas para cada curso.")

    # ---------- Prerequisitos ----------
    relaciones = [
        ("Matemáticas II", "Matemáticas I"),
        ("Estructuras de Datos", "Programación"),
        ("Algoritmos", "Estructuras de Datos"),
        ("Machine Learning", "Inteligencia Artificial"),
        ("Sistemas Operativos", "Estructuras de Datos"),
        ("Sistemas Distribuidos", "Sistemas Operativos"),
        ("Criptografía", "Probabilidades"),
        ("Desarrollo Web", "Ingeniería de Software"),
        ("Compiladores", "Algoritmos"),
        ("Robótica", "Sistemas Distribuidos")
    ]

    curso_dict = {c.name: c.id for c in cursos}

    prerequisitos = []
    for curso, prereq in relaciones:
        if curso in curso_dict and prereq in curso_dict:
            prereq_entry = CoursePrerequisite(
                course_id=curso_dict[curso],
                prerequisite_id=curso_dict[prereq]
            )
            prerequisitos.append(prereq_entry)

    db.session.add_all(prerequisitos)
    db.session.commit()
    print("10 prerequisitos agregados.")
