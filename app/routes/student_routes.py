from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.controllers.student_controller import getAllStudents, getStudent, createStudent, updateStudent, deleteStudent

student_bp = Blueprint('students', __name__, url_prefix='/students')

@student_bp.route('/', methods=['GET'])
def getStudentsView():
    students = getAllStudents()
    return render_template('students/index.html', students=students)

@student_bp.route('/create', methods=['GET', 'POST'])
def createStudentView():
    if request.method == 'POST':
        data = request.form
        createStudent(data)
        return redirect(url_for('students.getStudentsView'))

    return render_template('students/create.html')

@student_bp.route('/<int:student_id>', methods=['GET', 'POST'])
def updateStudentView(student_id):
    student = getStudent(student_id)
    if not student:
        return redirect(url_for('students.getStudentsView'))

    if request.method == 'POST':
        data = request.form
        updateStudent(student, data)

        return redirect(url_for('students.getStudentsView'))

    return render_template('students/edit.html', student=student)

@student_bp.route('/<int:student_id>', methods=['DELETE'])
def deleteStudentView(student_id):
    student = getStudent(student_id)
    if student:
        deleteStudent(student)
        return redirect(url_for('students.getAllStudents'))

    return redirect(url_for('students.getAllStudents'))
