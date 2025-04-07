from app import create_app
from flask import render_template #Allows the use of templates
from app.models.course import Course #Imports from DB
from app.models.student import Student #Imports from DB
from app.models.course_section import CourseSection
from app.models.teacher import Teacher



app = create_app()


#This is the file where the instance of the page it's initialized. The following route states the main page and should be used as an index to access different sections of the page.

@app.route('/')
def landing_page():

    courses = Course.query.all() #Access all course instances as course variable
    students = Student.query.all() #Access all students instances as students variable
    course_sections = CourseSection.query.all()
    teachers= Teacher.query.all()

    return render_template(
        'main.html',
        courses=courses,
        students=students,
        course_sections=course_sections,
        teachers=teachers
    ) #Location is templates/main.html, adds variables to template




#This are the configurations for runing the page. I -Vicente Acevedo- stated host as 0.0.0.0 to use both local host and local ip adress as it was standard in the documentation I studied for flask developement.

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
