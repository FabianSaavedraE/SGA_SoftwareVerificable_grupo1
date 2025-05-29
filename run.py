from flask import render_template

from app import create_app
from app.models import (
    Course, Student, CourseSection, Teacher,
    CoursePrerequisite, Classroom, CourseInstance
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
    classrooms = Classroom.query.all()
    course_instances = CourseInstance.query.all()

    return render_template(
        'main.html',
        courses=courses,
        students=students,
        course_sections=course_sections,
        teachers=teachers,
        course_prerequisites=course_prerequisites,
        course_instances=course_instances,
        classrooms=classrooms
    ) 

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
