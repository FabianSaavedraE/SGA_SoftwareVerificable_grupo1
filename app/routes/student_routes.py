from flask import Blueprint, request, jsonify
from app.controllers.student_controller import getAllStudents, createStudent, updateStudent, deleteStudent

student_bp = Blueprint('students', __name__, url_prefix='/students')

@student_bp.route('/', methods=['GET'])
def getStudents():
    return jsonify(getAllStudents())

@student_bp.route('/', methods=['POST'])
def addStudent():
    data = request.get_json()
    student = createStudent(data)
    return jsonify(student), 201

@student_bp.route('/<int:student_id>', methods=['PUT'])
def updateStudentRoute(student_id):
    data = request.get_json()
    student = updateStudent(student_id, data)
    if student is None:
        return jsonify({"message": "Student not found"}), 404
    
    return jsonify(student)

@student_bp.route('/<int:student_id>', methods=['DELETE'])
def deleteStudentRoute(student_id):
    success = deleteStudent(student_id)
    if not success:
        return jsonify({"message": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully"}), 200
    