from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.models.evaluation_type import EvaluationType
from app.controllers.evaluation_type_controller import getEvaluationTypesByCourse, getEvaluationType, createEvaluationType, updateEvaluationType, deleteEvaluationType
from app.controllers.course_section_controller import getSection
from app import db

evaluation_type_bp = Blueprint('evaluation_types', __name__, url_prefix='/evaluation_types')

@evaluation_type_bp.route('/<int:evaluation_type_id>/show', methods=['GET'])
def showEvaluationType(evaluation_type_id):
    evaluation_type = getEvaluationType(evaluation_type_id)
    if not evaluation_type:
        return redirect(url_for('course_sections.showSectionView', course_section_id=evaluation_type.course_section_id))

    return render_template('evaluation_types/show.html', evaluation_type=evaluation_type)

@evaluation_type_bp.route('/create/<int:course_section_id>', methods=['GET', 'POST'])
def createEvaluationTypeView(course_section_id):
    course_section = getSection(course_section_id)
    if not course_section:
        return redirect(url_for('course_sections.showSectionView', course_section_id=course_section_id))

    if request.method == 'POST':
        data = request.form.to_dict()
        data['course_section_id'] = course_section_id
        createEvaluationType(data)
        return redirect(url_for('course_sections.showSectionView', course_section_id=course_section_id))

    return render_template('evaluation_types/create.html', course_section=course_section)

@evaluation_type_bp.route('/<int:evaluation_type_id>', methods=['GET', 'POST'])
def updateEvaluationTypeView(evaluation_type_id):
    evaluation_type = getEvaluationType(evaluation_type_id)
    if not evaluation_type:
        return redirect(url_for('course_sections.showSectionView', course_section_id=evaluation_type.course_section_id))

    if request.method == 'POST':
        data = request.form
        updateEvaluationType(evaluation_type, data)

        return redirect(url_for('course_sections.showSectionView', course_section_id=evaluation_type.course_section_id))

    return render_template('evaluation_types/edit.html', evaluation_type=evaluation_type)
    
@evaluation_type_bp.route('/delete/<int:evaluation_type_id>/<int:course_section_id>', methods=['POST'])
def deleteEvaluationTypeView(evaluation_type_id, course_section_id):
    evaluation_type = getEvaluationType(evaluation_type_id)
    if evaluation_type:
        deleteEvaluationType(evaluation_type)
        return redirect(url_for('course_sections.showSectionView', course_section_id=course_section_id))
    
    return redirect(url_for('course_sections.showSectionView', course_section_id=course_section_id))