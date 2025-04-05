from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.controllers.teacher_controller import getAllTeachers, getTeacher, createTeacher, updateTeacher, deleteTeacher

teacher_bp = Blueprint('teachers', __name__, url_prefix='/teachers')

@teacher_bp.route('/', methods=['GET'])
def getTeachersView():
    teachers = getAllTeachers()
    return render_template('teachers/index.html', teachers=teachers)

@teacher_bp.route('/create', methods=['GET', 'POST'])
def createTeacherView():
    if request.method == 'POST':
        data = request.form
        createTeacher(data)
        return redirect(url_for('teachers.getTeachersView'))

    return render_template('teachers/create.html')

@teacher_bp.route('/<int:teacher_id>', methods=['GET', 'POST'])
def updateTeacherView(teacher_id):
    teacher = getTeacher(teacher_id)
    if not teacher:
        return redirect(url_for('teachers.getTeachersView'))

    if request.method == 'POST':
        data = request.form
        updateTeacher(teacher, data)

        return redirect(url_for('teachers.getTeachersView'))

    return render_template('teachers/edit.html', teacher=teacher)

@teacher_bp.route('/<int:teacher_id>', methods=['DELETE'])
def deleteTeacherView(teacher_id):
    teacher = getTeacher(teacher_id)
    if teacher:
        deleteTeacher(teacher)
        return redirect(url_for('teachers.getAllTeachers'))

    return redirect(url_for('teachers.getAllTeachers'))
