from flask import (
    Blueprint, request, render_template, redirect,
    url_for, send_file, flash
)

from app.controllers.student_controller import (
    get_all_students, get_student, create_student, update_student,
    delete_student, create_students_from_json, export_student_report_to_excel
)
from app.validators.student_validator import validate_student_data

student_bp = Blueprint('students', __name__, url_prefix='/students')

@student_bp.route('/', methods=['GET'])
def get_students_view():
    error = request.args.get('error')
    students = get_all_students()
    return render_template('students/index.html', students=students, error=error)

@student_bp.route('/create', methods=['GET', 'POST'])
def create_student_view():
    if request.method == 'POST':
        data = request.form
        errors = validate_student_data(data)
    
        if errors:
            return render_template('students/create.html', errors=errors)

        create_student(data)
        return redirect(url_for('students.get_students_view'))

    return render_template('students/create.html')

@student_bp.route('/<int:student_id>', methods=['GET', 'POST'])
def update_student_view(student_id):
    student = get_student(student_id)
    if request.form.get('_method') == 'DELETE':
        delete_student(student)
        return redirect(url_for('students.get_students_view'))

    if not student:
        return redirect(url_for('students.get_students_view'))

    if request.method == 'POST':
        data = request.form
        errors = validate_student_data(data, student_id)

        if errors:
            return render_template(
                'students/edit.html', student=student, errors=errors
            )
        
        update_student(student, data)
        return redirect(url_for('students.get_students_view'))

    return render_template('students/edit.html', student=student)

@student_bp.route('/delete/<int:student_id>', methods=['POST'])
def delete_student_view(student_id):
    student = get_student(student_id)
    if student:
        delete_student(student)
        return redirect(url_for('students.get_students_view'))

    return redirect(url_for('students.get_students_view'))

@student_bp.route('/upload-json', methods=['POST'])
def upload_students_json():
    file = request.files.get('jsonFile')
    if not file:
        return redirect(url_for('students.get_students_view'))

    import json
    try:
        data = json.load(file)
    except Exception as e:
        return redirect(url_for('students.get_students_view'))
    
    create_students_from_json(data)
    return redirect(url_for('students.get_students_view'))

@student_bp.route("/<int:student_id>/report", methods=['GET'])
def download_student_report(student_id):
    student = get_student(student_id)
    result = export_student_report_to_excel(student)

    if result is None:
        flash(
            'Este estudiante no tiene cursos cerrados para generar un ' \
            'certificado', 'error'
        )
        return redirect(url_for('students.get_students_view'))

    file_buffer, filename = result
    return send_file(file_buffer, as_attachment=True, download_name=filename)