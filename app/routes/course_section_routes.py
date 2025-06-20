from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from app.controllers.course_instance_controller import get_course_instance
from app.controllers.course_section_controller import (
    create_course_sections_from_json,
    create_section,
    delete_section,
    export_section_report_to_excel,
    get_all_sections,
    get_section,
    update_section,
)
from app.controllers.teacher_controller import get_all_teachers
from app.validators.course_section_validator import (
    validate_course_section,
    validate_evaluation_types_warning,
    validate_evaluations_warning,
)
from app.validators.data_load_validators import (
    validate_json_file_and_return_processed_file,
)

course_section_bp = Blueprint(
    "course_sections", __name__, url_prefix="/course_sections"
)


@course_section_bp.route("/", methods=["GET"])
def get_sections_view():
    """Render view with all course sections."""
    sections = get_all_sections()
    return render_template("course_sections/index.html", sections=sections)


@course_section_bp.route("/<int:course_section_id>/show", methods=["GET"])
def show_section_view(course_section_id):
    """Show details of a single course section."""
    course_section = get_section(course_section_id)
    if not course_section:
        return redirect(url_for("courses.get_courses_view"))

    warning_evaluation_types = validate_evaluation_types_warning(
        course_section
    )
    warning_evaluations = validate_evaluations_warning(course_section)

    return render_template(
        "course_sections/show.html",
        course_section=course_section,
        warning_evaluation_types=warning_evaluation_types,
        warning_evaluations=warning_evaluations,
    )


@course_section_bp.route(
    "/create/<int:course_instance_id>", methods=["GET", "POST"]
)
def create_section_view(course_instance_id):
    """Create a course section for a given course instance."""
    course_instance = get_course_instance(course_instance_id)
    teachers = get_all_teachers()
    if not course_instance:
        return redirect(
            url_for(
                "course_instances.get_course_instance_view",
                course_id=course_instance.course.id,
            )
        )

    if request.method == "POST":
        data = build_section_data(request.form, course_instance_id)
        errors = validate_course_section(data)

        if errors:
            return render_template(
                "course_sections/create.html",
                course_instance=course_instance,
                teachers=teachers,
                errors=errors,
            )

        create_section(data)
        return redirect(
            url_for(
                "course_instances.show_course_instance_view",
                course_instance_id=course_instance_id,
            )
        )

    return render_template(
        "course_sections/create.html",
        course_instance=course_instance,
        teachers=teachers,
    )


@course_section_bp.route("/<int:course_section_id>", methods=["GET", "POST"])
def update_section_view(course_section_id):
    """Update a course section by its ID."""
    course_section = get_section(course_section_id)
    teachers = get_all_teachers()
    if not course_section:
        return redirect(
            url_for(
                "course_sections.show_course_instance",
                course_instance_id=course_section.course_instance.id,
            )
        )

    if request.method == "POST":
        data = request.form
        errors = validate_course_section(data, course_section_id)

        if errors:
            return render_template(
                "course_sections/edit.html",
                course_section=course_section,
                teachers=teachers,
                errors=errors,
            )

        update_section(course_section, data)

        return redirect(url_for("course_sections.get_sections_view"))

    return render_template(
        "course_sections/edit.html",
        course_section=course_section,
        teachers=teachers,
    )


@course_section_bp.route(
    "/<int:course_section_id>/<int:course_instance_id>/delete",
    methods=["POST"],
)
def delete_section_view(course_section_id, course_instance_id):
    """Delete a course section."""
    course_section = get_section(course_section_id)
    if course_section:
        delete_section(course_section)
        return redirect(url_for("course_sections.get_sections_view"))

    return render_template("course_sections.get_sections_view")


@course_section_bp.route("/upload-json", methods=["POST"])
def upload_course_sections_json():
    """Upload and create course section from a JSON file."""
    file = request.files.get("jsonFile")
    if not file:
        return redirect(url_for("courses.get_courses_view"))

    data = validate_json_file_and_return_processed_file(file)
    if data:
        create_course_sections_from_json(data)

    return redirect(url_for("course_sections.get_sections_view"))


@course_section_bp.route(
    "/delete/<int:course_section_id>/<int:course_instance_id>",
    methods=["POST"],
)
def delete_section_view_from_show(course_section_id, course_instance_id):
    """Delete a section and redirects to the course instance view."""
    course_section = get_section(course_section_id)
    if course_section:
        delete_section(course_section)
        return redirect(
            url_for(
                "course_instances.show_course_instance_view",
                course_instance_id=course_instance_id,
            )
        )

    render_template(
        "course_instances.show_course_instance_view",
        course_instance_id=course_instance_id,
    )


@course_section_bp.route("/<int:course_section_id>/report", methods=["GET"])
def download_course_section_report(course_section_id):
    """Download an Excel report for a specific course section."""
    course_section = get_section(course_section_id)
    result = export_section_report_to_excel(course_section)

    if result is None:
        flash(
            "No se pudo generar el reporte de notas para esta sección.",
            "error",
        )
        return redirect(
            url_for(
                "course_instances.show_course_instance_view",
                course_instance_id=course_section.course_instance_id,
            )
        )

    file_buffer, filename = result
    return send_file(file_buffer, as_attachment=True, download_name=filename)


def build_section_data(form_data, course_instance_id):
    """Build section data from form data and a course instance ID."""
    data = form_data.to_dict()
    data["course_instance_id"] = course_instance_id
    return data
