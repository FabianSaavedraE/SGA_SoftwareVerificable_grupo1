from flask import (
    Blueprint, request, render_template, redirect, url_for
)

from app.controllers.course_instance_controller import (
    get_course_instance, create_course_instance, update_course_instance, 
    delete_course_instance, validate_course_instance
)
from app.controllers.course_controller import get_course

course_instance_bp = Blueprint(
    'course_instances', __name__, url_prefix='/course_instances'
)

@course_instance_bp.route('/<int:course_instance_id>/show', methods=['GET'])
def show_course_instance_view(course_instance_id):
    course_instance = get_course_instance(course_instance_id)
    if not course_instance:
        return redirect(url_for(
            'courses.show_course_view',
            course_id=course_instance.course.id
        ))

    return render_template(
        'course_instances/show.html',
        course_instance=course_instance
    )

@course_instance_bp.route('/create/<int:course_id>', methods=['GET', 'POST'])
def create_course_instance_view(course_id):
    course = get_course(course_id)

    if not course:
        return redirect(url_for('courses.get_course_view'))

    error = None
    if request.method == 'POST':
        data = build_course_instance_data(request.form, course_id)
        errors = validate_course_instance(data)

        if errors:
            return render_template(
                'course_instances/create.html', course=course, errors=errors
            )

        create_course_instance(data)
        return redirect(url_for(
            'courses.show_course_view', course_id=course_id
        ))

    return render_template(
        'course_instances/create.html', course=course, error=error
    )

@course_instance_bp.route('/<int:course_instance_id>', methods=['GET', 'POST'])
def update_course_instance_view(course_instance_id):
    course_instance = get_course_instance(course_instance_id)
    if not course_instance:
        return redirect(url_for(
            'courses.show_course_view',
            course_id=course_instance.course.id
        ))

    if request.method == 'POST':
        data = request.form
        errors = validate_course_instance(data, course_instance_id)

        if errors:
            return render_template(
                'course_instances/edit.html',
                course_instance=course_instance,
                errors=errors
            )

        update_course_instance(course_instance, data)
        return redirect(url_for(
            'courses.show_course_view',
            course_id=course_instance.course.id
        ))

    return render_template(
        'course_instances/edit.html',
        course_instance=course_instance
    )

@course_instance_bp.route(
        '/delete/<int:course_instance_id>/<int:course_id>',
        methods=['POST']
)
def delete_course_instance_view(course_instance_id, course_id):
    course_instance = get_course_instance(course_instance_id)
    if course_instance:
        delete_course_instance(course_instance)
        return redirect(url_for(
            'courses.show_course_view',
            course_id=course_id
        ))

    return render_template(
        url_for('courses.show_course_view', coures_id=course_id)
    )

def build_course_instance_data(form_data, course_id):
    data = form_data.to_dict()
    data['course_id'] = course_id
    return data
