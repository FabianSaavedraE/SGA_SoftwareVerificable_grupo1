from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.models.course import Course
from app.controllers.course_controller import getAllCourses, getCourse, createCourse, updateCourse, deleteCourse
from app import db

course_bp = Blueprint('courses', __name__, url_prefix='/courses')

@course_bp.route('/', methods=['GET'])
def getCoursesView():
    courses = getAllCourses()
    return render_template('courses/index.html', courses=courses)

@course_bp.route('/<int:course_id>/show', methods=['GET'])
def showCourseView(course_id):
    course = getCourse(course_id)
    if not course:
        return redirect(url_for('courses.getCoursesView'))

    return render_template('courses/show.html', course=course)

@course_bp.route('/create', methods=['GET', 'POST'])
def createCourseView():
    if request.method == 'POST':
        data = request.form
        createCourse(data)
        return redirect(url_for('courses.getCoursesView'))

    return render_template('courses/create.html')

@course_bp.route('/<int:course_id>', methods=['GET', 'POST'])
def updateCourseView(course_id):
    course = getCourse(course_id)
    if not course:
        return redirect(url_for('courses.getCoursesView'))

    if request.method == 'POST':
        data = request.form
        updateCourse(course, data)

        return redirect(url_for('courses.getCoursesView'))

    return render_template('courses/edit.html', course=course)

@course_bp.route('/delete/<int:course_id>', methods=['POST'])
def deleteCourseView(course_id):
    course = getCourse(course_id)
    if course:
        deleteCourse(course)
        return redirect(url_for('courses.getCoursesView'))

    return redirect(url_for('courses.getCoursesView'))
    