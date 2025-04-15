from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.models.course_section import CourseSection
from app.controllers.course_section_controller import getAllSections, getSection, createSection, updateSection, deleteSection
from app.controllers.course_instance_controller import getCourseInstance
from app.controllers.teacher_controller import getAllTeachers
from app import db

course_section_bp = Blueprint('course_sections', __name__, url_prefix='/course_sections')

@course_section_bp.route('/', methods=['GET'])
def getSectionsView():
    sections = getAllSections()
    return render_template('course_sections/index.html', sections=sections)

@course_section_bp.route('/<int:course_section_id>/show', methods=['GET'])
def showSectionView(course_section_id):
    course_section = getSection(course_section_id)
    if not course_section:
        return redirect(url_for('courses.getCoursesView'))

    return render_template('course_sections/show.html', course_section=course_section)

@course_section_bp.route('/create/<int:course_instance_id>', methods=['GET', 'POST'])
def createSectionView(course_instance_id):
    course_instance = getCourseInstance(course_instance_id)
    teachers = getAllTeachers()
    if not course_instance:
        return redirect(url_for('course_instances.getCourseInstanceView', course_id=course_instance.course.id))

    if request.method == 'POST':
        data = request.form.to_dict()
        data['course_instance_id'] = course_instance_id
        createSection(data)
        return redirect(url_for('course_instances.showCourseInstanceView', course_instance_id=course_instance_id))

    return render_template('course_sections/create.html', course_instance=course_instance, teachers=teachers)

@course_section_bp.route('/<int:course_section_id>', methods=['GET', 'POST'])
def updateSectionView(course_section_id):
    course_section = getSection(course_section_id)
    teachers = getAllTeachers()
    if not course_section:
        return redirect(url_for('course_sections.showCourseInstance', course_instance_id=course_section.course_instance.id))

    if request.method == 'POST':
        data = request.form
        updateSection(course_section, data)
        
        return redirect(url_for('course_sections.getSectionsView'))
    
    return render_template('course_sections/edit.html', course_section=course_section, teachers=teachers)

@course_section_bp.route('/<int:course_section_id>/<int:course_instance_id>/delete', methods=['POST'])
def deleteSectionView(course_section_id, course_instance_id):
    course_section = getSection(course_section_id)
    if course_section:
        deleteSection(course_section)
        return redirect(url_for('course_sections.getSectionsView'))
    
    return render_template('course_sections.getSectionsView')

@course_section_bp.route('/delete/<int:course_section_id>/<int:course_instance_id>', methods=['POST'])
def deleteSectionViewFromShow(course_section_id, course_instance_id):
    course_section = getSection(course_section_id)
    if course_section:
        deleteSection(course_section)
        return redirect(url_for('course_instances.showCourseInstanceView', course_instance_id=course_instance_id))
    
    render_template('course_instances.showCourseInstanceView', course_instance_id=course_instance_id)
