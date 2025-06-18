from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from app.controllers.student_controller import (
    create_student,
    create_students_from_json,
    delete_student,
    export_student_report_to_excel,
    get_all_students,
    get_student,
    update_student,
)
from app.validators.data_load_validators import (
    validate_json_file_and_return_processed_file,
)
from app.validators.student_validator import (
    validate_student_data_and_return_errors,
)

student_bp = Blueprint("students", __name__, url_prefix="/students")


@student_bp.route("/", methods=["GET"])
def get_students_view():
    """Render the view to display all students."""
    error = request.args.get("error")
    students = get_all_students()
    return render_template(
        "students/index.html", students=students, error=error
    )


@student_bp.route("/create", methods=["GET", "POST"])
def create_student_view():
    """Handle creating a new student."""
    if request.method == "POST":
        data = request.form
        errors = validate_student_data_and_return_errors(data)

        if errors:
            return render_template("students/create.html", errors=errors)

        create_student(data)
        return redirect(url_for("students.get_students_view"))

    return render_template("students/create.html")


@student_bp.route("/<int:student_id>", methods=["GET", "POST"])
def update_student_view(student_id):
    """Handle updating or deleting a student."""
    student = get_student(student_id)
    if request.form.get("_method") == "DELETE":
        delete_student(student)
        return redirect(url_for("students.get_students_view"))

    if not student:
        return redirect(url_for("students.get_students_view"))

    if request.method == "POST":
        data = request.form
        errors = validate_student_data_and_return_errors(data, student_id)

        if errors:
            return render_template(
                "students/edit.html", student=student, errors=errors
            )

        update_student(student, data)
        return redirect(url_for("students.get_students_view"))

    return render_template("students/edit.html", student=student)


@student_bp.route("/delete/<int:student_id>", methods=["POST"])
def delete_student_view(student_id):
    """Handle deleting a student."""
    student = get_student(student_id)
    if student:
        delete_student(student)
        return redirect(url_for("students.get_students_view"))

    return redirect(url_for("students.get_students_view"))


@student_bp.route("/upload-json", methods=["POST"])
def upload_students_json():
    """Handle uploading a JSON file to create students."""
    file = request.files.get("jsonFile")
    if not file:
        return redirect(url_for("students.get_students_view"))

    data = validate_json_file_and_return_processed_file(file)

    if data:
        create_students_from_json(data)

    return redirect(url_for("students.get_students_view"))


@student_bp.route("/<int:student_id>/report", methods=["GET"])
def download_student_report(student_id):
    """Download an Excel report for a specific student."""
    student = get_student(student_id)
    result = export_student_report_to_excel(student)

    if result is None:
        flash(
            "Este estudiante no tiene cursos cerrados para generar un "
            "certificado",
            "error",
        )
        return redirect(url_for("students.get_students_view"))

    file_buffer, filename = result
    return send_file(file_buffer, as_attachment=True, download_name=filename)
