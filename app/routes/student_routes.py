from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.controllers.student_controller import get_all_students, get_student, create_student, update_student, delete_student

student_bp = Blueprint('students', __name__, url_prefix='/students')

@student_bp.route('/', methods=['GET'])
def get_students_view():
    students = get_all_students()
    return render_template('students/index.html', students=students)

@student_bp.route('/create', methods=['GET', 'POST'])
def create_student_view():
    if request.method == 'POST':
        data = request.form
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
