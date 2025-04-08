from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.models.course_prerequisite import CoursePrerequisite
from app.controllers.course_prerequisite_controller import createCoursePrerequisite, getCoursePrerequisite, updateCoursePrerequisite, deleteCoursePrerequisite
from app import db

course_prerequisite_bp = Blueprint('course_prerequisites', __name__, url_prefix='/course_prerequisites')

# Ruta para ver todos los course prerequisites
@course_prerequisite_bp.route('/', methods=['GET'])
def getAllCoursePrerequisites():
    course_prerequisites = CoursePrerequisite.query.all()
    return jsonify([{
        'course_id': cp.course_id,
        'prerequisite_id': cp.prerequisite_id
    } for cp in course_prerequisites])

# Ruta para ver un solo course prerequisite por su ID
@course_prerequisite_bp.route('/<int:course_id>/<int:prerequisite_id>', methods=['GET'])
def getCoursePrerequisiteView(course_id, prerequisite_id):
    course_prerequisite = CoursePrerequisite.query.get((course_id, prerequisite_id))
    if not course_prerequisite:
        return jsonify({'message': 'Course prerequisite not found'}), 404
    return jsonify({
        'course_id': course_prerequisite.course_id,
        'prerequisite_id': course_prerequisite.prerequisite_id
    })

# Ruta para crear un nuevo course prerequisite
@course_prerequisite_bp.route('/create', methods=['GET', 'POST'])
def createCoursePrerequisiteView():
    if request.method == 'POST':
        data = request.form.to_dict()
        createCoursePrerequisite(data)
        return redirect(url_for('course_prerequisites.getAllCoursePrerequisites'))
    return render_template('course_prerequisites/create.html')

# Ruta para actualizar un course prerequisite
@course_prerequisite_bp.route('/update/<int:course_id>/<int:prerequisite_id>', methods=['GET', 'POST'])
def updateCoursePrerequisiteView(course_id, prerequisite_id):
    course_prerequisite = getCoursePrerequisite(course_id, prerequisite_id)
    if not course_prerequisite:
        return jsonify({'message': 'Course prerequisite not found'}), 404

    if request.method == 'POST':
        data = request.form.to_dict()
        updateCoursePrerequisite(course_prerequisite, data)
        return redirect(url_for('course_prerequisites.getCoursePrerequisiteView', course_id=course_id, prerequisite_id=prerequisite_id))

    return render_template('course_prerequisites/edit.html', course_prerequisite=course_prerequisite)

# Ruta para eliminar un course prerequisite
@course_prerequisite_bp.route('/delete/<int:course_id>/<int:prerequisite_id>', methods=['POST'])
def deleteCoursePrerequisiteView(course_id, prerequisite_id):
    course_prerequisite = getCoursePrerequisite(course_id, prerequisite_id)
    if not course_prerequisite:
        return jsonify({'message': 'Course prerequisite not found'}), 404
    deleteCoursePrerequisite(course_prerequisite)
    return redirect(url_for('course_prerequisites.getAllCoursePrerequisites'))
