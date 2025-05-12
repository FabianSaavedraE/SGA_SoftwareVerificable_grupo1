from flask import Blueprint, request, render_template, redirect, url_for

from app.controllers.evaluation_type_controller import (
    get_evaluation_type, create_evaluation_type,
    update_evaluation_type, delete_evaluation_type
)
from app.controllers.course_section_controller import get_section

evaluation_type_bp = Blueprint(
    'evaluation_types', __name__, url_prefix='/evaluation_types'
)

@evaluation_type_bp.route('/<int:evaluation_type_id>/show', methods=['GET'])
def show_evaluation_type(evaluation_type_id):
    evaluation_type = get_evaluation_type(evaluation_type_id)
    if not evaluation_type:
        return redirect(url_for(
            'course_sections.show_section_view',
            course_section_id=evaluation_type.course_section_id
        ))

    return render_template(
        'evaluation_types/show.html',
        evaluation_type=evaluation_type
    )

@evaluation_type_bp.route(
    '/create/<int:course_section_id>',
    methods=['GET', 'POST']
)
def create_evaluation_type_view(course_section_id):
    course_section = get_section(course_section_id)
    if not course_section:
        return redirect(url_for(
            'course_sections.show_section_view',
            course_section_id=course_section_id
        ))

    if request.method == 'POST':
        data = build_evaluation_type_data(request.form, course_section_id)
        new_evaluation_type = create_evaluation_type(data)

        return redirect(url_for(
            'evaluations.create_evaluation_view',
            evaluation_type_id=new_evaluation_type.id
        ))
    
    return render_template(
        'evaluation_types/create.html',
        course_section=course_section
    )

@evaluation_type_bp.route('/<int:evaluation_type_id>', methods=['GET', 'POST'])
def update_evaluation_type_view(evaluation_type_id):
    evaluation_type = get_evaluation_type(evaluation_type_id)
    if not evaluation_type:
        return redirect(url_for(
            'course_sections.show_section_view',
            course_section_id=evaluation_type.course_section_id
        ))

    if request.method == 'POST':
        data = request.form
        update_evaluation_type(evaluation_type, data)

        return redirect(url_for(
            'course_sections.show_section_view',
            course_section_id=evaluation_type.course_section_id
        ))

    return render_template(
        'evaluation_types/edit.html',
        evaluation_type=evaluation_type
    )

@evaluation_type_bp.route(
    '/delete/<int:evaluation_type_id>/<int:course_section_id>',
    methods=['POST']
)
def delete_evaluation_type_view(evaluation_type_id, course_section_id):
    evaluation_type = get_evaluation_type(evaluation_type_id)
    if evaluation_type:
        delete_evaluation_type(evaluation_type)
        return redirect(url_for(
            'course_sections.show_section_view',
            course_section_id=course_section_id
        ))

    return redirect(url_for(
        'course_sections.show_section_view',
        course_section_id=course_section_id
    ))

def build_evaluation_type_data(form_data, course_section_id):
    data = form_data.to_dict()
    data['course_section_id'] = course_section_id
    return data
