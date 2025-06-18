from flask import Blueprint, redirect, render_template, request, url_for

from app.controllers.course_section_controller import get_section
from app.controllers.evaluation_type_controller import (
    create_evaluation_type,
    delete_evaluation_type,
    get_evaluation_type,
    update_evaluation_type,
)

evaluation_type_bp = Blueprint(
    "evaluation_types", __name__, url_prefix="/evaluation_types"
)


@evaluation_type_bp.route("/<int:evaluation_type_id>/show", methods=["GET"])
def show_evaluation_type(evaluation_type_id):
    """Render the view to display a single evaluation type."""
    evaluation_type = get_evaluation_type(evaluation_type_id)
    if not evaluation_type:
        return redirect(
            url_for(
                "course_sections.show_section_view",
                course_section_id=evaluation_type.course_section_id,
            )
        )

    return render_template(
        "evaluation_types/show.html", evaluation_type=evaluation_type
    )


@evaluation_type_bp.route(
    "/create/<int:course_section_id>", methods=["GET", "POST"]
)
def create_evaluation_type_view(course_section_id):
    """Handle creating a new evaluation type."""
    course_section = get_section(course_section_id)
    error = None
    if not course_section:
        return redirect(
            url_for(
                "course_sections.show_section_view",
                course_section_id=course_section_id,
            )
        )

    if request.method == "POST":
        data = build_evaluation_type_data(request.form, course_section_id)
        new_evaluation_type, current_sum = create_evaluation_type(data)

        if new_evaluation_type is None:
            error = (
                f"Suma actual de porcentajes: {current_sum}%. "
                f"No puede exceder 100% al agregar este tipo."
            )
        else:
            return redirect(
                url_for(
                    "evaluations.create_evaluation_view",
                    evaluation_type_id=new_evaluation_type.id,
                )
            )

    return render_template(
        "evaluation_types/create.html",
        course_section=course_section,
        error=error,
    )


@evaluation_type_bp.route("/<int:evaluation_type_id>", methods=["GET", "POST"])
def update_evaluation_type_view(evaluation_type_id):
    """Handle updating an existing evaluation type."""
    evaluation_type = get_evaluation_type(evaluation_type_id)
    error = None
    if not evaluation_type:
        return redirect(
            url_for(
                "course_sections.show_section_view",
                course_section_id=evaluation_type.course_section_id,
            )
        )

    if request.method == "POST":
        data = request.form
        updated_evaluation_type, current_sum = update_evaluation_type(
            evaluation_type, data
        )

        if updated_evaluation_type is None:
            error = (
                f"Suma actual de porcentajes sin este tipo: {current_sum}%. "
                f"No puede exceder 100% al actualizar."
            )
        else:
            return redirect(
                url_for(
                    "course_sections.show_section_view",
                    course_section_id=evaluation_type.course_section_id,
                )
            )

    return render_template(
        "evaluation_types/edit.html",
        evaluation_type=evaluation_type,
        error=error,
    )


@evaluation_type_bp.route(
    "/delete/<int:evaluation_type_id>/<int:course_section_id>",
    methods=["POST"],
)
def delete_evaluation_type_view(evaluation_type_id, course_section_id):
    """Handle deleting an evaluation type."""
    evaluation_type = get_evaluation_type(evaluation_type_id)
    if evaluation_type:
        delete_evaluation_type(evaluation_type)
        return redirect(
            url_for(
                "course_sections.show_section_view",
                course_section_id=course_section_id,
            )
        )

    return redirect(
        url_for(
            "course_sections.show_section_view",
            course_section_id=course_section_id,
        )
    )


def build_evaluation_type_data(form_data, course_section_id):
    """Build evaluation type data from form data and a course section ID."""
    data = form_data.to_dict()
    data["course_section_id"] = course_section_id
    return data
