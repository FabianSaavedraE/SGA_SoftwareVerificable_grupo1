from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy import or_

from app.controllers.course_section_controller import get_section
from app.controllers.student_course_controller import (
    create_student_course,
    create_student_courses_from_json,
    delete_student_course,
    get_student_course,
    update_student_course,
)
from app.models.student import Student
from app.validators.data_load_validators import (
    validate_json_file_and_return_processed_file,
)
from app.validators.student_course_validator import check_prerequisites

student_course_bp = Blueprint(
    "student_courses", __name__, url_prefix="/student_courses"
)


@student_course_bp.route(
    "/create/<int:course_section_id>", methods=["GET", "POST"]
)
def create_student_course_view(course_section_id):
    """Handle creating a new student-course enrollment."""
    section = get_section(course_section_id)
    if not section:
        return redirect(
            url_for(
                "course_sections.show_section_view",
                course_section_id=course_section_id,
            )
        )

    query = request.args.get("q") or request.form.get("q")
    students = get_students_by_query(query) if query else []
    error = None

    if request.method == "POST":
        data = build_student_course_data(request.form, course_section_id)
        has_passed_requisites, error_message = check_prerequisites(data)

        if not has_passed_requisites:
            return render_template(
                "student_courses/create.html",
                section=section,
                students=students,
                error=error_message["prerrequisito"],
                q=query,
            )

        create_student_course(data)

        return redirect(
            url_for(
                "student_courses.create_student_course_view",
                course_section_id=course_section_id,
                q=query,
            )
        )

    return render_template(
        "student_courses/create.html",
        section=section,
        students=students,
        error=error,
        q=query,
    )


@student_course_bp.route(
    "/<int:student_id>/<int:course_section_id>", methods=["GET", "POST"]
)
def update_student_course_view(student_id, course_section_id):
    """Handle updating an existing student-course enrollment."""
    student_course = get_student_course(student_id, course_section_id)
    if not student_course:
        return redirect(
            url_for(
                "course_sections.show_section_view",
                course_id=course_section_id,
            )
        )

    if request.method == "POST":
        data = request.form
        update_student_course(student_course, data)

        return redirect(
            url_for(
                "course_sections.show_section_view",
                course_section_id=course_section_id,
            )
        )

    return render_template(
        "student_courses/edit.html", student_course=student_course
    )


@student_course_bp.route("/upload-json", methods=["POST"])
def upload_student_courses_json():
    """Handle uploading a JSON file to create student-course enrollments."""
    file = request.files.get("jsonFile")
    if not file:
        return redirect(url_for("course_sections.get_sections_view"))

    data = validate_json_file_and_return_processed_file(file)

    if data:
        create_student_courses_from_json(data)

    return redirect(url_for("course_sections.get_sections_view"))


@student_course_bp.route(
    "/delete/<int:student_id>/<int:course_section_id>", methods=["POST"]
)
def delete_student_course_view(student_id, course_section_id):
    """Handle deleting a student-course enrollment."""
    student_course = get_student_course(student_id, course_section_id)
    if student_course:
        delete_student_course(student_id, course_section_id)
        return redirect(
            url_for(
                "course_sections.show_section_view",
                course_section_id=course_section_id,
            )
        )

    return render_template(
        "course_sections.show_section_view",
        course_section_id=course_section_id,
    )


def build_student_course_data(form_data, course_section_id):
    """Build student course data from form data and section ID."""
    data = form_data.to_dict()
    data["course_section_id"] = course_section_id
    data["state"] = "Inscrito"
    return data


def get_students_by_query(query):
    """Retrieve students from the database based on a query string."""
    return Student.query.filter(
        or_(
            Student.first_name.ilike(f"%{query}%"),
            Student.last_name.ilike(f"%{query}%"),
        )
    ).all()
