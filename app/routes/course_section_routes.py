from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.models.course_section import CourseSection
from app.controllers.course_section_controller import getAllSections, getSection, createSection, updateSection
from app.controllers.course_controllers import getCourse
from app.controllers.teacher_controller import getAllTeachers
from app import db

course_section_bp = Blueprint('course_sections', __name__, url_prefix='/course_sections')

@course_section_bp.route('/', methods=['GET'])
def getSectionsView():
    sections = getAllSections()
    return render_template('course_sections/index.html', sections=sections)

@course_section_bp.route('/create/<int:course_id>', methods=['GET', 'POST'])
def createSectionView(course_id):
    course = getCourse(course_id)
    teachers = getAllTeachers()
    if not course:
        return redirect(url_for('courses.getCourseView'))

    if request.method == 'POST':
        data = request.form.to_dict()
        data['course_id'] = course_id
        createSection(data)
        return redirect(url_for('courses.showCourseView', course_id=course_id))

    return render_template('course_sections/create.html', course=course, teachers=teachers)

@course_section_bp.route('/<int:course_section_id>', methods=['GET', 'POST'])
def updateSectionView(course_section_id):
    course_section = getSection(course_section_id)
    teachers = getAllTeachers()
    if not course_section:
        return redirect(url_for('courses.getCoursesView'))

    if request.method == 'POST':
        data = request.form
        updateSection(course_section, data)

        return redirect(url_for('courses.showCourseView', course_id=course_section.course_id))

    return render_template('course_sections/edit.html', course_section=course_section, teachers=teachers)
