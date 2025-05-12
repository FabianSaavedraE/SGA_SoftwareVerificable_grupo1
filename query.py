#This .py file it's used to run querys. Similar to the Rails Console -using this analogy since it's the only web developement framework we studied oficially at UANDES- it will run the queries here written when called from console. To do this, it needs to acces the specific tables and structure.

from app import create_app, db
from app.models.course import Course
from app.models.student import Student
from app.models.course_prerequisite import CoursePrerequisite
from app.models.teacher import Teacher

#The app needs to be created for consultations
app = create_app()

with app.app_context():

    #Query for all existing courses.

    print("Cursos existentes:")
    cursos = Course.query.all()
    for curso in cursos:
        print(f"- {curso.id}: {curso.name}") 
    
    print("Profesores existentes:")
    profesores = Teacher.query.all()
    for profesor in profesores:
        print(f"- {profesor.id}: {profesor.first_name} {profesor.last_name}") 


    #Query for all existing students:

    print("\nEstudiantes existentes:")
    estudiantes = Student.query.all()
    for est in estudiantes:
        print(est) 


    #Query for all prerequisite pairings: (Im debugging this rn, love, vicente acevedo.)
        
    print("\nPares de prerequisitos:")
    prerequisites = CoursePrerequisite.query.all()
    for prerequisite in prerequisites:
        print(f"{prerequisite.course.name} requires {prerequisite.prerequisite.name}")  
    