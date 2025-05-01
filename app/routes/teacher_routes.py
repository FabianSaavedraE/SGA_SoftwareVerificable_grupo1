from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.controllers.teacher_controller import get_all_teachers, get_teacher, create_teacher, update_teacher, delete_teacher

teacher_bp = Blueprint('teachers', __name__, url_prefix='/teachers')

@teacher_bp.route('/', methods=['GET'])
def get_teachers_view():
    teachers = get_all_teachers()
    return render_template('teachers/index.html', teachers=teachers)

@teacher_bp.route('/create', methods=['GET', 'POST'])
def create_teacher_view():
    if request.method == 'POST':
        data = request.form
        create_teacher(data)
        return redirect(url_for('teachers.get_teachers_view'))

    return render_template('teachers/create.html')

@teacher_bp.route('/<int:teacher_id>', methods=['GET', 'POST'])
def update_teacher_view(teacher_id):
    teacher = get_teacher(teacher_id)
    if not teacher:
        return redirect(url_for('teachers.get_teachers_view'))

    if request.method == 'POST':
        data = request.form
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
