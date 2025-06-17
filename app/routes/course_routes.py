from flask import Blueprint, redirect, render_template, request, url_for

from app.controllers.course_controller import (
    create_course,
    create_courses_from_json,
    delete_course,
    get_all_courses,
    get_course,
    update_course,
)
from app.validators.course_validator import (
    validate_course_data_and_return_errors,
)
from app.validators.data_load_validators import (
    validate_json_file_and_return_processed_file,
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
        errors = validate_course_data_and_return_errors(data)

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
        errors = validate_course_data_and_return_errors(
            data, course_id=course_id
        )

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

    data = validate_json_file_and_return_processed_file(file)

    if data:
        create_courses_from_json(data)

    return redirect(url_for('courses.get_courses_view'))
