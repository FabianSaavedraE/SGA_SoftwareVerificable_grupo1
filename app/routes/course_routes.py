from flask import Blueprint, request, render_template, redirect, url_for

from app.validators.course_validator import validate_course_data
from app.controllers.course_controller import (
    get_all_courses, get_course, create_course, update_course, delete_course,
    create_courses_from_json
)

course_bp = Blueprint('courses', __name__, url_prefix='/courses')

@course_bp.route('/', methods=['GET'])
def get_courses_view():
    courses = get_all_courses()
    return render_template('courses/index.html', courses=courses)

@course_bp.route('/<int:course_id>/show', methods=['GET'])
def show_course_view(course_id):
    course = get_course(course_id)
    if not course:
        return redirect(url_for('courses.get_courses_view'))

    return render_template('courses/show.html', course=course)

@course_bp.route('/create', methods=['GET', 'POST'])
def create_course_view():
    if request.method == 'POST':
        data = request.form
        errors = validate_course_data(data)

        if errors:
            return render_template(
                'courses/create.html', errors=errors, data=data
            )

        create_course(data)
        return redirect(url_for('courses.get_courses_view'))

    return render_template('courses/create.html')

@course_bp.route('/<int:course_id>', methods=['GET', 'POST'])
def update_course_view(course_id):
    course = get_course(course_id)
    if not course:
        return redirect(url_for('courses.get_courses_view'))

    if request.method == 'POST':
        data = request.form
        errors = validate_course_data(data, course_id=course_id)

        if errors:
            return render_template(
                'courses/edit.html', course=course, errors=errors, data=data
            )

        update_course(course, data)
        return redirect(url_for('courses.get_courses_view'))

    return render_template('courses/edit.html', course=course)

@course_bp.route('/delete/<int:course_id>', methods=['POST'])
def delete_course_view(course_id):
    course = get_course(course_id)
    if course:
        delete_course(course)
        return redirect(url_for('courses.get_courses_view'))

    return redirect(url_for('courses.get_courses_view'))

@course_bp.route('/upload-json', methods=['POST'])
def upload_courses_json():
    file = request.files.get('jsonFile')
    if not file:
        return redirect(url_for('courses.get_courses_view'))

    import json
    try:
        data = json.load(file)
    except Exception as e:
        print("Error leyendo JSON:", e)
        return redirect(url_for('courses.get_courses_view'))
    
    create_courses_from_json(data)

    return redirect(url_for('courses.get_courses_view'))
