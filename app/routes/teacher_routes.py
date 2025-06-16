from flask import Blueprint, redirect, render_template, request, url_for

from app.controllers.teacher_controller import (
    create_teacher,
    create_teachers_from_json,
    delete_teacher,
    get_all_teachers,
    get_teacher,
    update_teacher,
)
from app.validators.teacher_validator import validate_teacher_data

teacher_bp = Blueprint('teachers', __name__, url_prefix='/teachers')


@teacher_bp.route('/', methods=['GET'])
def get_teachers_view():
    teachers = get_all_teachers()
    return render_template('teachers/index.html', teachers=teachers)


@teacher_bp.route('/create', methods=['GET', 'POST'])
def create_teacher_view():
    if request.method == 'POST':
        data = request.form
        errors = validate_teacher_data(data)

        if errors:
            return render_template('teachers/create.html', errors=errors)

        create_teacher(request.form)
        return redirect(url_for('teachers.get_teachers_view'))

    return render_template('teachers/create.html')


@teacher_bp.route('/<int:teacher_id>', methods=['GET', 'POST'])
def update_teacher_view(teacher_id):
    teacher = get_teacher(teacher_id)
    if not teacher:
        return redirect(url_for('teachers.get_teachers_view'))

    if request.method == 'POST':
        data = request.form
        errors = validate_teacher_data(data, teacher_id)

        if errors:
            return render_template(
                'teachers/edit.html', teacher=teacher, errors=errors
            )

        update_teacher(teacher, data)
        return redirect(url_for('teachers.get_teachers_view'))

    return render_template('teachers/edit.html', teacher=teacher)


@teacher_bp.route('/delete/<int:teacher_id>', methods=['POST'])
def delete_teacher_view(teacher_id):
    teacher = get_teacher(teacher_id)
    if teacher:
        delete_teacher(teacher)
        return redirect(url_for('teachers.get_teachers_view'))

    return redirect(url_for('teachers.get_teachers_view'))


@teacher_bp.route('/upload-json', methods=['POST'])
def upload_teachers_json():
    file = request.files.get('jsonFile')
    if not file:
        return redirect(url_for('teachers.get_teachers_view'))

    import json

    try:
        data = json.load(file)
    except Exception:
        return redirect(url_for('teachers.get_teachers_view'))

    create_teachers_from_json(data)
    return redirect(url_for('teachers.get_teachers_view'))
