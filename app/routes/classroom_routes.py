from flask import Blueprint, request, render_template, redirect, url_for, flash

from app.controllers.classroom_controller import (
    get_all_classrooms, get_classroom, create_classroom,
    update_classroom, delete_classroom, create_classroom_from_json
)
from app.validators.classroom_validator import validate_classroom_data

from app.validators.data_load_validators import(
     validate_json_file_and_return_processed_file
)


classroom_bp = Blueprint('classrooms', __name__, url_prefix='/classrooms')

@classroom_bp.route('/', methods=['GET'])
def get_classrooms_view():
    classrooms = get_all_classrooms()
    return render_template('classrooms/index.html', classrooms=classrooms)

@classroom_bp.route('/create', methods=['GET', 'POST'])
def create_classroom_view():
    if request.method == 'POST':
        data = request.form
        errors = validate_classroom_data(data)

        if errors:
            return render_template('classrooms/create.html', errors=errors)
        
        create_classroom(data)
        return redirect(url_for('classrooms.get_classrooms_view'))

    return render_template('classrooms/create.html')

@classroom_bp.route('/<int:classroom_id>', methods=['GET', 'POST'])
def update_classroom_view(classroom_id):
    classroom = get_classroom(classroom_id)
    if request.form.get('_method') == 'DELETE':
        delete_classroom(classroom)
        return redirect(url_for('classrooms.get_classrooms_view'))

    if not classroom:
        return redirect(url_for('classrooms.get_classrooms_view'))

    if request.method == 'POST':
        data = request.form
        errors = validate_classroom_data(data, classroom_id)

        if errors:
            return render_template(
                'classrooms/edit.html', classroom=classroom, errors=errors
            )
        
        update_classroom(classroom, data)
        return redirect(url_for('classrooms.get_classrooms_view'))

    return render_template('classrooms/edit.html', classroom=classroom)

@classroom_bp.route('/delete/<int:classroom_id>', methods=['POST'])
def delete_classroom_view(classroom_id):
    classroom = get_classroom(classroom_id)
    if classroom:
        delete_classroom(classroom)
        return redirect(url_for('classrooms.get_classrooms_view'))

    return redirect(url_for('classrooms.get_clasrooms_view'))

@classroom_bp.route('/upload-json', methods=['POST'])
def upload_classrooms_json():
    file = request.files.get('jsonFile')
    if not file:
        return redirect(url_for('classrooms.get_classrooms_view'))

    data = validate_json_file_and_return_processed_file(file)

    if data:
        create_classroom_from_json(data)

    return redirect(url_for('classrooms.get_classrooms_view'))
