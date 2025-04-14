from flask import Blueprint, request, render_template, redirect, url_for
from app.models.course_instance import CourseInstance
from app.controllers.course_instance_controller import getCourseInstance, createCourseInstance, updateCourseInstance, deleteCourseInstance
from app.controllers.course_controller import getCourse

course_instance_bp = Blueprint('course_instances', __name__, url_prefix='/course_instances')

@course_instance_bp.route('/<int:course_instance_id>/show', methods=['GET'])
def showCourseInstanceView(course_instance_id):
    course_instance = getCourseInstance(course_instance_id)
    if not course_instance:
        return redirect(url_for('courses.showCourseView', course_id=course_instance.course.id))
    
    return render_template('course_instances/show.html', course_instance=course_instance)

@course_instance_bp.route('/create/<int:course_id>', methods=['GET', 'POST'])
def createCourseInstanceView(course_id):
    course = getCourse(course_id)

    if not course:
        return redirect(url_for('courses.getCourseView'))
    
    if request.method == 'POST':
        data = request.form.to_dict()
        data['course_id'] = course_id
        createCourseInstance(data)
        return redirect(url_for('courses.showCourseView', course_id=course_id))
    
    return render_template('course_instances/create.html', course=course)

@course_instance_bp.route('/<int:course_instance_id>', methods=['GET', 'POST'])
def updateCourseInstanceView(course_instance_id):
    course_instance = getCourseInstance(course_instance_id)
    if not course_instance:
        return redirect(url_for('courses.showCourseView', course_id=course_instance.course.id))
    
    if request.method == 'POST':
        data = request.form
        updateCourseInstance(course_instance, data)
        return redirect(url_for('courses.showCourseView', course_id=course_instance.course.id))
    
    return render_template('course_instances/edit.html', course_instance=course_instance)

@course_instance_bp.route('/delete/<int:course_instance_id>/<int:course_id>', methods=['POST'])
def deleteCourseInstanceView(course_instance_id, course_id):
    course_instance = getCourseInstance(course_instance_id)
    if course_instance:
        deleteCourseInstance(course_instance)
        return redirect(url_for('courses.showCourseView', course_id=course_id))
    
    return render_template(url_for('courses.showCourseView', coures_id=course_id))