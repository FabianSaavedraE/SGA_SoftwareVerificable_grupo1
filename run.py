from app import create_app
from flask import render_template #Allows the use of templates
from app.models.course import Course #Imports from DB
from app.models.student import Student #Imports from DB
from app.models.course_section import CourseSection
from app.models.teacher import Teacher
from app.models.course_prerequisite import CoursePrerequisite
from app.models.course_instance import CourseInstance


from app import create_app
from app.models import (
    Course, Student, CourseSection, Teacher, CoursePrerequisite, Classroom
)

app = create_app()

# This is the file where the instance of the page it's initialized. 
# The following route states the main page and should be used as an index to 
# access different sections of the page.

@app.route('/')
def landing_page():
    courses = Course.query.all() 
    students = Student.query.all() 
    course_sections = CourseSection.query.all()
    teachers= Teacher.query.all()
    course_prerequisites = CoursePrerequisite.query.all()
    course_instances = CourseInstance.query.all()
    classrooms = Classroom.query.all()


    return render_template(
        'main.html',
        courses=courses,
        students=students,
        course_sections=course_sections,
        teachers=teachers,
        course_instances=course_instances,
        course_prerequisites=course_prerequisites
        course_prerequisites=course_prerequisites,
        classrooms=classrooms
    ) 

# This are the configurations for runing the page. I -Vicente Acevedo- stated 
# host as 0.0.0.0 to use both local host and local ip adress as it was standard
# in the documentation I studied for flask developement.

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
