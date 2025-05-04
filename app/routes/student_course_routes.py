from flask import Blueprint, request, render_template, redirect, url_for

from sqlalchemy import or_

from app.controllers.student_course_controller import (
    create_student_course, get_student_course,
    update_student_course, delete_student_course
)
from app.controllers.course_section_controller import get_section
from app.models.student import Student

student_course_bp = Blueprint(
    'student_courses', __name__, url_prefix='/student_courses'
)

@student_course_bp.route(
    '/create/<int:course_section_id>',
    methods=['GET', 'POST']
)
def create_student_course_view(course_section_id):
    section = get_section(course_section_id)
    if not section:
        return redirect(url_for(
            'course_sections.show_section_view',
            course_section_id=course_section_id
        ))

    if request.method == 'POST':
        data = build_student_course_data(request.form, course_section_id)

        create_student_course(data)
        # Preservamos el valor del query de búsqueda
        q = request.form.get('q', '')
        return redirect(url_for(
            'student_courses.create_student_course_view',
            course_section_id=course_section_id,
            q=q
        ))

    query = request.args.get('q')
    students = get_students_by_query(query) if query else []

    return render_template(
        'student_courses/create.html',
        section=section,
        students=students
    )

@student_course_bp.route(
    '/<int:student_id>/<int:course_section_id>',
    methods=['GET', 'POST']
)
def update_student_course_view(student_id, course_section_id):
    student_course = get_student_course(student_id, course_section_id)
    if not student_course:
        return redirect(url_for(
            'course_sections.show_section_view',
            course_id=course_section_id
        ))

    if request.method == 'POST':
        data = request.form
        update_student_course(student_course, data)

        return redirect(url_for(
            'course_sections.show_section_view',
            course_section_id=course_section_id
        ))

    return render_template(
        'student_courses/edit.html',
        student_course=student_course
    )

@student_course_bp.route(
    '/delete/<int:student_id>/<int:course_section_id>',
    methods=['POST']
)
def delete_student_course_view(student_id, course_section_id):
    student_course = get_student_course(student_id, course_section_id)
    if student_course:
        delete_student_course(student_id, course_section_id)
        return redirect(url_for(
            'course_sections.show_section_view',
            course_section_id=course_section_id
        ))

    return render_template(
        'course_sections.show_section_view',
        course_section_id=course_section_id
    )

def build_student_course_data(form_data, course_section_id):
    data = form_data.to_dict()
    data['course_section_id'] = course_section_id
    data['state'] = 'Inscrito'
    return data

def get_students_by_query(query):
    return Student.query.filter(
        or_(
            Student.first_name.ilike(f"%{query}%"),
            Student.last_name.ilike(f"%{query}%")
        )
    ).all()
