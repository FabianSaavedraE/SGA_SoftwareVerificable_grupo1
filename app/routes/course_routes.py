from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.models.course import Course
from app.controllers.course_controller import get_all_courses, get_course, create_course, update_course, delete_course
from app import db

course_bp = Blueprint('courses', __name__, url_prefix='/courses')

@course_bp.route('/', methods=['GET'])
def get_courses_view():
    courses = get_all_courses()
    return render_template('courses/index.html', courses=courses)

@course_bp.route('/<int:course_id>/show', methods=['GET'])
def show_course_view(course_id):
    course = get_course(course_id)
    if not course:
        return redirect(url_for('courses.get_courses_view'))

    return render_template('courses/show.html', course=course)

@course_bp.route('/create', methods=['GET', 'POST'])
def create_course_View():
    if request.method == 'POST':
        data = request.form
        create_course(data)
        return redirect(url_for('courses.get_courses_view'))

    return render_template('courses/create.html')

@course_bp.route('/<int:course_id>', methods=['GET', 'POST'])
def update_course_view(course_id):
    course = get_course(course_id)
    if not course:
        return redirect(url_for('courses.get_courses_view'))

    if request.method == 'POST':
        data = request.form
        update_course(course, data)

        return redirect(url_for('courses.get_courses_view'))

    return render_template('courses/edit.html', course=course)

@course_bp.route('/delete/<int:course_id>', methods=['POST'])
def delete_course_view(course_id):
    course = get_course(course_id)
    if course:
        delete_course(course)
        return redirect(url_for('courses.get_courses_view'))

    return redirect(url_for('courses.get_courses_view'))
    