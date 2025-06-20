from flask import Blueprint, redirect, render_template, request, url_for

from app.controllers.classroom_controller import (
    create_classroom,
    create_classroom_from_json,
    delete_classroom,
    get_all_classrooms,
    get_classroom,
    update_classroom,
)
from app.validators.classroom_validator import (
    validate_classroom_data_and_return_errors,
)
from app.validators.data_load_validators import (
    validate_json_file_and_return_processed_file,
)

classroom_bp = Blueprint("classrooms", __name__, url_prefix="/classrooms")


@classroom_bp.route("/", methods=["GET"])
def get_classrooms_view():
    """Render all classrooms in the index template."""
    classrooms = get_all_classrooms()
    return render_template("classrooms/index.html", classrooms=classrooms)


@classroom_bp.route("/create", methods=["GET", "POST"])
def create_classroom_view():
    """Handle creation of a new classroom."""
    if request.method == "POST":
        data = request.form
        errors = validate_classroom_data_and_return_errors(data)

        if errors:
            return render_template("classrooms/create.html", errors=errors)

        create_classroom(data)
        return redirect(url_for("classrooms.get_classrooms_view"))

    return render_template("classrooms/create.html")


@classroom_bp.route("/<int:classroom_id>", methods=["GET", "POST"])
def update_classroom_view(classroom_id):
    """Handle classroom update or delete by ID."""
    classroom = get_classroom(classroom_id)
    if request.form.get("_method") == "DELETE":
        delete_classroom(classroom)
        return redirect(url_for("classrooms.get_classrooms_view"))

    if not classroom:
        return redirect(url_for("classrooms.get_classrooms_view"))

    if request.method == "POST":
        data = request.form
        errors = validate_classroom_data_and_return_errors(data, classroom_id)

        if errors:
            return render_template(
                "classrooms/edit.html", classroom=classroom, errors=errors
            )

        update_classroom(classroom, data)
        return redirect(url_for("classrooms.get_classrooms_view"))

    return render_template("classrooms/edit.html", classroom=classroom)


@classroom_bp.route("/delete/<int:classroom_id>", methods=["POST"])
def delete_classroom_view(classroom_id):
    """Delete a classroom by ID and redirect."""
    classroom = get_classroom(classroom_id)
    if classroom:
        delete_classroom(classroom)
        return redirect(url_for("classrooms.get_classrooms_view"))

    return redirect(url_for("classrooms.get_classrooms_view"))


@classroom_bp.route("/upload-json", methods=["POST"])
def upload_classrooms_json():
    """Upload and process a JSON file of classrooms."""
    file = request.files.get("jsonFile")
    if not file:
        return redirect(url_for("classrooms.get_classrooms_view"))

    data = validate_json_file_and_return_processed_file(file)

    if data:
        create_classroom_from_json(data)

    return redirect(url_for("classrooms.get_classrooms_view"))
