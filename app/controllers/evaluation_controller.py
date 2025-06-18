from io import BytesIO

import pandas as pd
from sqlalchemy import func

from app import db
from app.models.evaluation import Evaluation
from app.models.evaluation_type import EvaluationType

REPORT_COLUMNS = [
    "Curso",
    "Sección",
    "Tipo de Evaluación",
    "Evaluación",
    "Estudiante",
    "Nota",
]


def get_all_evaluations():
    """Get all evaluations."""
    evaluations = Evaluation.query.all()
    return evaluations


def get_evaluations_by_topic(evaluation_type_id):
    """Get evaluations by evaluation type."""
    evaluations = Evaluation.query.filter_by(
        evaluation_type_id=evaluation_type_id
    ).all()
    return evaluations


def get_evaluation(evaluation_id):
    """Get one evaluation by ID."""
    evaluation = Evaluation.query.get(evaluation_id)
    return evaluation


def create_evaluation(data):
    """Create a new evaluation."""
    evaluation_type_id = data.get("evaluation_type_id")
    evaluation_type = EvaluationType.query.get(evaluation_type_id)

    evaluation_ponderation = float(data.get("ponderation") or 0)

    if not evaluation_type:
        return None

    if evaluation_type.ponderation_type == "Porcentaje":
        total = (
            db.session.query(
                func.coalesce(func.sum(Evaluation.ponderation), 0)
            )
            .filter_by(evaluation_type_id=evaluation_type_id)
            .scalar()
        )
        total = round(total or 0, 2)
        if total + evaluation_ponderation > 100:
            return None, round(total, 2)

    new_evaluation = Evaluation(
        name=data.get("name"),
        ponderation=evaluation_ponderation,
        optional=data.get("optional", False),
        evaluation_type_id=evaluation_type_id,
    )

    db.session.add(new_evaluation)
    db.session.commit()

    return new_evaluation, None


def update_evaluation(evaluation, data):
    """Update an evaluation."""
    if not evaluation:
        return None

    new_evaluation_ponderation = float(
        data.get("ponderation", evaluation.ponderation)
    )
    evaluation_type = evaluation.evaluation_type

    if evaluation_type.ponderation_type == "Porcentaje":
        total = (
            db.session.query(
                func.coalesce(func.sum(Evaluation.ponderation), 0)
            )
            .filter(
                Evaluation.evaluation_type_id == evaluation_type.id,
                Evaluation.id != evaluation.id,
            )
            .scalar()
        )
        total = round(total or 0, 2)
        if total + new_evaluation_ponderation > 100:
            return None, round(total, 2)

    evaluation.name = data.get("name", evaluation.name)
    evaluation.ponderation = new_evaluation_ponderation
    evaluation.optional = data.get("optional", evaluation.optional)

    db.session.commit()
    return evaluation, None


def delete_evaluation(evaluation):
    """Delete an evaluation."""
    if not evaluation:
        return False

    db.session.delete(evaluation)
    db.session.commit()
    return True


def export_evaluation_report_to_excel(evaluation):
    """Export evaluation data to an Excel file."""
    records = generate_records(evaluation)
    excel_buffer = convert_records_to_excel(records)

    if excel_buffer is None:
        return None

    filename = f"{evaluation.name}_reporte_notas.xlsx"
    return excel_buffer, filename


def generate_records(evaluation):
    """Generate records from evaluation for the report."""
    data = []

    evaluation_name = evaluation.name
    evaluation_type = evaluation.evaluation_type
    course_section = evaluation_type.course_section
    course_instance = course_section.course_instance
    course = course_instance.course

    student_evaluations = evaluation.student_evaluations
    for evaluation in student_evaluations:
        student = evaluation.student
        student_name = f"{student.first_name} {student.last_name}"
        grade = evaluation.grade

        data.append(
            {
                "Curso": course.name,
                "Sección": course_section.nrc,
                "Tipo de Evaluación": evaluation_type.topic,
                "Evaluación": evaluation_name,
                "Estudiante": student_name,
                "Nota": grade,
            }
        )

    return sorted(data, key=lambda r: (r["Estudiante"]))


def convert_records_to_excel(records):
    """Convert records to an Excel buffer."""
    if not records:
        return None

    dataframe = pd.DataFrame(records, columns=REPORT_COLUMNS)
    excel_buffer = BytesIO()
    dataframe.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    return excel_buffer
