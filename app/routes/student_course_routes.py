from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.models.student_course import StudentCourses
from app.controllers.student_course_controller import createStudentCourse
from app.controllers.course_section_controller import getSection
from app.controllers.student_controller import getAllStudents

from app import db

student_course_bp = Blueprint('student_courses', __name__, url_prefix='/student_courses')

@student_course_bp.route('/create/<int:course_section_id>', methods=['GET', 'POST'])
def createStudentCourseView(course_section_id):
    section = getSection(course_section_id)
    students = getAllStudents()
    
    if not section:
        return redirect(url_for('course_sections.showSectionView', course_id=section.course_id))

    if request.method == 'POST':
        data = request.form.to_dict()
        data['course_section_id'] = course_section_id
        data['state'] = 'enrolled'
        createStudentCourse(data)
        return redirect(url_for('student_courses.createStudentCourseView', course_section_id=course_section_id))

    return render_template('student_courses/create.html', section=section, students=students)
