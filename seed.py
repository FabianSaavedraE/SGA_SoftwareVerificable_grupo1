from app import create_app, db
from app.models.student import Student
from app.models.course import Course
from app.models.course_section import CourseSection
from app.models.teacher import Teacher

app = create_app()

with app.app_context():
    # Re-instantiate the database.
    db.drop_all()
    db.create_all()
    print("Database reset (tables dropped and recreated).")

    # Creating 5 students.
    new_students = [
        Student(first_name="Sofía", last_name="Gómez", email="sofia.gomez@example.com"),
        Student(first_name="Ignacio", last_name="Pérez", email="ignacio.perez@example.com"),
        Student(first_name="Camila", last_name="Rojas", email="camila.rojas@example.com"),
        Student(first_name="Benjamín", last_name="Torres", email="benjamin.torres@example.com"),
        Student(first_name="Fernanda", last_name="Molina", email="fernanda.molina@example.com")
    ]
    db.session.add_all(new_students)
    db.session.commit()
    print("5 students created successfully.")

    # Creating 5 courses.
    new_courses = [
        Course(name="Mathematics I"),
        Course(name="Advanced Programming"),
        Course(name="General Physics"),
        Course(name="Databases"),
        Course(name="Artificial Intelligence")
    ]
    db.session.add_all(new_courses)
    db.session.commit()
    print("5 courses created successfully.")

    # Create a teacher
    teacher = Teacher(first_name="Claudia", last_name="Valdés", email="claudia.valdes@example.com")
    db.session.add(teacher)
    db.session.commit()
    print("Example teacher created.")

    # Create 5 sections, one for each course
    courses = Course.query.all()
    new_sections = []
    for i, course in enumerate(courses):
        section = CourseSection(
            nrc=f"NRC00{i+1}",
            semester="2025-1",
            course_id=course.id,
            teacher_id=teacher.id
        )
        new_sections.append(section)

    db.session.add_all(new_sections)
    db.session.commit()
    print("5 sections created successfully.")