from flask import Blueprint, redirect, render_template, request, url_for

from app.controllers.evaluation_controller import get_evaluation
from app.controllers.student_controller import get_student
from app.controllers.student_evaluation_controller import (
    create_student_evaluation,
    create_student_evaluation_json,
    get_student_evaluation,
    update_student_evaluation,
)
from app.validators.data_load_validators import (
    validate_json_file_and_return_processed_file,
)
from app.validators.student_evaluation_validator import (
    validate_student_evaluation_data,
)

student_evaluation_bp = Blueprint(
    "student_evaluations", __name__, url_prefix="/student_evaluations"
)


@student_evaluation_bp.route(
    "/create/<int:evaluation_id>/<int:student_id>", methods=["GET", "POST"]
)
def create_student_evaluation_view(student_id, evaluation_id):
    """Handle creating a new student evaluation."""
    evaluation = get_evaluation(evaluation_id)
    student = get_student(student_id)
    student_evaluation = get_student_evaluation(student_id, evaluation_id)

    if not evaluation or not student:
        return redirect(url_for("evaluations.indexView"))

    if request.method == "POST":
        data = build_student_evaluation_data(
            request.form,
            evaluation_id,
            student_id,
            evaluation.evaluation_type_id,
        )
        errors = validate_student_evaluation_data(data)

        if errors:
            return render_template(
                "student_evaluations/create.html",
                evaluation=evaluation,
                student=student,
                student_evaluation=student_evaluation,
                errors=errors,
            )

        create_student_evaluation(data)
        return redirect(
            url_for(
                "evaluations.show_evaluation_view", evaluation_id=evaluation_id
            )
        )

    return render_template(
        "student_evaluations/create.html",
        evaluation=evaluation,
        student=student,
        student_evaluation=student_evaluation,
    )


@student_evaluation_bp.route("/upload-json", methods=["POST"])
def upload_student_evaluation_json():
    """Handle uploading a JSON file to create student evaluations."""
    file = request.files.get("jsonFile")
    if not file:
        return redirect(url_for("course_sections.get_sections_view"))

    data = validate_json_file_and_return_processed_file(file)

    if data:
        create_student_evaluation_json(data)

    return redirect(url_for("course_sections.get_sections_view"))


@student_evaluation_bp.route(
    "/<int:evaluation_id>/students/<int:student_id>/edit",
    methods=["GET", "POST"],
)
def update_student_evaluation_view(student_id, evaluation_id):
    """Handle updating an existing student evaluation."""
    student_evaluation = get_student_evaluation(student_id, evaluation_id)
    evaluation = get_evaluation(evaluation_id)
    student = get_student(student_id)

    if not student_evaluation:
        return redirect(
            url_for(
                "evaluations.show_evaluation_view", evaluation_id=evaluation_id
            )
        )

    errors = None
    if request.method == "POST":
        data = build_student_evaluation_data(
            request.form,
            evaluation_id,
            student_id,
            evaluation.evaluation_type_id,
        )

        errors = validate_student_evaluation_data(
            data,
            original_student_id=student_id,
            original_evaluation_id=evaluation_id,
        )

        if errors:
            return render_template(
                "student_evaluations/edit.html",
                student_evaluation=student_evaluation,
                student=student,
                evaluation=evaluation,
                errors=errors,
            )

        update_student_evaluation(student_evaluation, data)
        return redirect(
            url_for(
                "evaluations.show_evaluation_view", evaluation_id=evaluation_id
            )
        )

    return render_template(
        "student_evaluations/edit.html",
        student_evaluation=student_evaluation,
        student=student,
        evaluation=evaluation,
    )


def build_student_evaluation_data(
    form_data, evaluation_id, student_id, evaluation_type_id
):
    """Build student evaluation data from form data and IDs."""
    data = form_data.to_dict()
    data["evaluation_id"] = evaluation_id
    data["student_id"] = student_id
    data["evaluation_type_id"] = evaluation_type_id
    return data
