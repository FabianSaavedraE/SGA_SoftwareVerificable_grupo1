from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.models.student_course import StudentCourses
from app.controllers.student_course_controller import createStudentCourse, getStudentCourse, updateStudentCourse, deleteStudentCourse
from app.controllers.course_section_controller import getSection
from app.controllers.student_controller import getAllStudents
from sqlalchemy import or_
from app.models.student import Student

from app import db

student_course_bp = Blueprint('student_courses', __name__, url_prefix='/student_courses')

@student_course_bp.route('/create/<int:course_section_id>', methods=['GET', 'POST'])
def createStudentCourseView(course_section_id):
    section = getSection(course_section_id)
    
    if not section:
        return redirect(url_for('course_sections.showSectionView', course_id=section.course_id))

    if request.method == 'POST':
        data = request.form.to_dict()
        data['course_section_id'] = course_section_id
        data['state'] = 'Inscrito'
        createStudentCourse(data)
        return redirect(url_for('student_courses.createStudentCourseView', course_section_id=course_section_id))

    # Logica para el buscador
    query = request.args.get('q')
    if query:
        students = Student.query.filter(
            or_(
                Student.first_name.ilike(f"%{query}%"),
                Student.last_name.ilike(f"%{query}%")
            )
        ).all()
    else:
        students = []

    return render_template('student_courses/create.html', section=section, students=students)

@student_course_bp.route('/<int:student_id>/<int:course_section_id>', methods=['GET', 'POST'])
def updateStudentCourseView(student_id, course_section_id):
    student_course = getStudentCourse(student_id, course_section_id)
    if not student_course:
        return redirect(url_for('course_sections.showSectionView', course_id=course_section_id))

    if request.method == 'POST':
        data = request.form
        updateStudentCourse(student_course, data)

        return redirect(url_for('course_sections.showSectionView', course_section_id=course_section_id))

    return render_template('student_courses/edit.html', student_course=student_course)
    
@student_course_bp.route('/delete/<int:student_id>/<int:course_section_id>', methods=['POST'])
def deleteStudentCourseView(student_id, course_section_id):
    student_course = getStudentCourse(student_id, course_section_id)
    if student_course:
        deleteStudentCourse(student_id, course_section_id)
        return redirect(url_for('course_sections.showSectionView', course_section_id=course_section_id))
    
    return render_template('course_sections.showSectionView', course_section_id=course_section_id)