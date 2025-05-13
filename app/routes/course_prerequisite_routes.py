from flask import (
    Blueprint, jsonify, request, render_template, redirect, url_for
)

from app import db
from app.models.course_prerequisite import CoursePrerequisite
from app.controllers.course_prerequisites_controllers import (
    get_course_prerequisite, delete_course_prerequisite,
    create_course_prerequisites
)
from app.controllers.course_controller import get_all_courses, get_course
from app.validators.course_prerequisites_validator import (
    validate_prerequisites
)

course_prerequisite_bp = Blueprint(
    'course_prerequisites', __name__, url_prefix='/course_prerequisites'
)

@course_prerequisite_bp.route('/', methods=['GET'])
def get_course_prerequisites():
    all_prerequisites = get_all_prerequisites()
    grouped = group_course_prerequisites(all_prerequisites)

    return render_template(
        'course_prerequisites/index.html',
        grouped_prerequisites=grouped
    )

@course_prerequisite_bp.route('/create', methods=['GET', 'POST'])
def create_course_prerequisite_view():
    courses = get_all_courses()
    if request.method == 'POST':
        data = request.form
        course_id = data.get('course_id')
        prerequisite_ids = data.getlist('prerequisite_ids')  
        errors = validate_prerequisites(course_id, prerequisite_ids)
        
        if errors:
            return render_template(
                'course_prerequisites/create.html',
                courses=courses,
                errors=errors
            )

        create_course_prerequisites(course_id, prerequisite_ids)
        return redirect(url_for(
            'course_prerequisites.get_course_prerequisites'
        ))

    return render_template('course_prerequisites/create.html', courses=courses)

@course_prerequisite_bp.route(
    '/update/<int:course_id>',
    methods=['GET', 'POST']
)
def update_course_prerequisite_view(course_id):
    course = get_course(course_id)

    if not course:
        return jsonify({'message': 'Course not found'}), 404

    if request.method == 'POST':
        if 'delete_prerequisite_id' in request.form:
            to_delete = request.form['delete_prerequisite_id']
            delete_course_prerequisite(course_id, int(to_delete))

            return redirect(url_for(
                'course_prerequisites.update_course_prerequisite_view',
                course_id=course_id
            ))

        ids_to_delete = request.form.getlist('prerequisite_ids')
        for prereq_id in ids_to_delete:
            delete_course_prerequisite(course_id, prereq_id)

        new_prereq_ids = request.form.getlist('new_prerequisite[]')
        errors = validate_prerequisites(course_id, new_prereq_ids)

        if errors:
            return render_template(
                'course_prerequisites/edit.html',
                course=course,
                prerequisites=filter_prerequisites(course_id),
                available_prereqs=get_all_courses(),
                errors=errors
            )
    
        create_course_prerequisites(course_id, new_prereq_ids)

        return redirect(url_for(
            'course_prerequisites.update_course_prerequisite_view',
            course_id=course_id
        ))

    prerequisites = filter_prerequisites(course_id)
    available_prereqs = get_all_courses()
    
    return render_template(
        'course_prerequisites/edit.html',
        course=course,
        prerequisites=prerequisites,
        available_prereqs=available_prereqs
    )

@course_prerequisite_bp.route(
    '/delete/<int:course_id>/<int:prerequisite_id>',
    methods=['POST']
)
def delete_course_prerequisite_view(course_id, prerequisite_id):
    course_prerequisite = get_course_prerequisite(course_id, prerequisite_id)
    if not course_prerequisite:
        return jsonify({'message': 'Course prerequisite not found'}), 404
    
    delete_course_prerequisite(course_id, prerequisite_id)
    return redirect(url_for('course_prerequisites.get_course_prerequisites'))


def group_course_prerequisites(prerequisites):
    grouped = {}
    for pair in prerequisites:
        course = pair.course
        prereq = pair.prerequisite

        if course.id not in grouped:
            grouped[course.id] = {
                "name": course.name,
                "prerequisites": []
            }

        grouped[course.id]["prerequisites"].append({
            "id": prereq.id,
            "name": prereq.name
        })

    return grouped

def get_all_prerequisites():
    return CoursePrerequisite.query.all()

def get_course_prerequisite(course_id, prerequisite_id):
    return CoursePrerequisite.query.get((course_id, prerequisite_id))

def filter_prerequisites(course_id):
    return CoursePrerequisite.query.filter_by(course_id=course_id).all()
