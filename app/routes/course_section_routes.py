from flask import Blueprint, request, render_template, redirect, url_for

from app.controllers.course_section_controller import (
    get_all_sections, get_section, create_section,
    update_section, delete_section
)
from app.controllers.course_instance_controller import get_course_instance
from app.controllers.teacher_controller import get_all_teachers

course_section_bp = Blueprint(
    'course_sections', __name__, url_prefix='/course_sections'
)

@course_section_bp.route('/', methods=['GET'])
def get_sections_view():
    sections = get_all_sections()
    return render_template('course_sections/index.html', sections=sections)

@course_section_bp.route('/<int:course_section_id>/show', methods=['GET'])
def show_section_view(course_section_id):
    course_section = get_section(course_section_id)
    if not course_section:
        return redirect(url_for('courses.get_courses_view'))

    return render_template(
        'course_sections/show.html',
        course_section=course_section
    )

@course_section_bp.route(
    '/create/<int:course_instance_id>',
    methods=['GET', 'POST']
)
def create_section_view(course_instance_id):
    course_instance = get_course_instance(course_instance_id)
    teachers = get_all_teachers()
    if not course_instance:
        return redirect(url_for(
            'course_instances.get_course_instance_view',
            course_id=course_instance.course.id
        ))

    if request.method == 'POST':
        data = build_section_data(request.form, course_instance_id)
        create_section(data)
        return redirect(url_for(
            'course_instances.show_course_instance_view',
            course_instance_id=course_instance_id
        ))

    return render_template(
        'course_sections/create.html',
        course_instance=course_instance,
        teachers=teachers
    )

@course_section_bp.route('/<int:course_section_id>', methods=['GET', 'POST'])
def update_section_view(course_section_id):
    course_section = get_section(course_section_id)
    teachers = get_all_teachers()
    if not course_section:
        return redirect(url_for(
            'course_sections.show_course_instance',
            course_instance_id=course_section.course_instance.id
        ))

    if request.method == 'POST':
        data = request.form
        update_section(course_section, data)

        return redirect(url_for('course_sections.get_sections_view'))

    return render_template(
        'course_sections/edit.html',
        course_section=course_section,
        teachers=teachers
    )

@course_section_bp.route(
    '/<int:course_section_id>/<int:course_instance_id>/delete',
    methods=['POST']
)
def delete_section_view(course_section_id, course_instance_id):
    course_section = get_section(course_section_id)
    if course_section:
        delete_section(course_section)
        return redirect(url_for('course_sections.get_sections_view'))

    return render_template('course_sections.get_sections_view')

@course_section_bp.route(
    '/delete/<int:course_section_id>/<int:course_instance_id>',
    methods=['POST']
)
def delete_section_view_from_show(course_section_id, course_instance_id):
    course_section = get_section(course_section_id)
    if course_section:
        delete_section(course_section)
        return redirect(url_for(
            'course_instances.show_course_instance_view',
            course_instance_id=course_instance_id
        ))

    render_template(
        'course_instances.show_course_instance_view',
        course_instance_id=course_instance_id
    )

def build_section_data(form_data, course_instance_id):
    data = form_data.to_dict()
    data['course_instance_id'] = course_instance_id
    return data