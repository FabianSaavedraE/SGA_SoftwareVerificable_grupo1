from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.models.course_prerequisite import CoursePrerequisite
from app.controllers.course_prerequisites_controllers import createCoursePrerequisite, getCoursePrerequisite, updateCoursePrerequisite, deleteCoursePrerequisite
from app import db

course_prerequisite_bp = Blueprint('course_prerequisites', __name__, url_prefix='/course_prerequisites')

@course_prerequisite_bp.route('/', methods=['GET'])
def getCoursePrerequisites():
    course_prerequisites = CoursePrerequisite.query.all()
    grouped_prerequisites = {}

    for pair in course_prerequisites:
        course = pair.course
        prereq = pair.prerequisite

        if course.id not in grouped_prerequisites:
            grouped_prerequisites[course.id] = {
                "name": course.name,
                "prerequisites": []
                }
        grouped_prerequisites[course.id]["prerequisites"].append({
            "id": prereq.id,
            "name": prereq.name
        })
    return render_template('course_prerequisites/index.html', grouped_prerequisites=grouped_prerequisites)

@course_prerequisite_bp.route('/create', methods=['GET', 'POST'])
def createCoursePrerequisiteView():
    from app.models.course import Course  
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        prerequisite_ids = request.form.getlist('prerequisite_ids')  

        for prereq_id in prerequisite_ids:
            if prereq_id != course_id:  
                new_pair = CoursePrerequisite(course_id=course_id, prerequisite_id=prereq_id)
                db.session.add(new_pair)

        db.session.commit()
        return redirect(url_for('course_prerequisites.getCoursePrerequisites'))

    courses = Course.query.all()
    return render_template('course_prerequisites/create.html', courses=courses)

@course_prerequisite_bp.route('/update/<int:course_id>', methods=['GET', 'POST'])
def updateCoursePrerequisiteView(course_id):
    from app.models.course import Course  
    course = Course.query.get(course_id)

    if not course:
        return jsonify({'message': 'Course not found'}), 404

    if request.method == 'POST':
        ids_to_delete = request.form.getlist('prerequisite_ids')
        for prereq_id in ids_to_delete:
            pair = CoursePrerequisite.query.get((course_id, int(prereq_id)))
            if pair:
                db.session.delete(pair)
        new_prereq_ids = request.form.getlist('new_prerequisite[]')
        for new_id in new_prereq_ids:
            if new_id and new_id != str(course_id):
                existing = CoursePrerequisite.query.get((course_id, int(new_id)))
                if not existing:
                    new_pair = CoursePrerequisite(course_id=course_id, prerequisite_id=int(new_id))
                    db.session.add(new_pair)

        db.session.commit()
        return redirect(url_for('course_prerequisites.updateCoursePrerequisiteView', course_id=course_id))

    prerequisites = CoursePrerequisite.query.filter_by(course_id=course_id).all()
    available_prereqs = Course.query.all()
    return render_template('course_prerequisites/edit.html', course=course, prerequisites=prerequisites, available_prereqs=available_prereqs)

@course_prerequisite_bp.route('/delete/<int:course_id>/<int:prerequisite_id>', methods=['POST'])
def deleteCoursePrerequisiteView(course_id, prerequisite_id):
    print(f"Deleting prerequisite: {prerequisite_id} for course {course_id}")
    course_prerequisite = getCoursePrerequisite(course_id, prerequisite_id)
    if not course_prerequisite:
        return jsonify({'message': 'Course prerequisite not found'}), 404
    deleteCoursePrerequisite(course_id, prerequisite_id)
    return redirect(url_for('course_prerequisites.getCoursePrerequisites'))