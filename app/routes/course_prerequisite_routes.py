from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from app.controllers.course_controller import get_all_courses, get_course
from app.controllers.course_prerequisites_controllers import (
    create_course_prerequisites,
    delete_course_prerequisite,
    get_all_course_prerequisites,
    get_course_prerequisite,
    get_prerequisites_by_course,
)
from app.validators.course_prerequisites_validator import (
    validate_prerequisites,
)

course_prerequisite_bp = Blueprint(
    "course_prerequisites", __name__, url_prefix="/course_prerequisites"
)


@course_prerequisite_bp.route("/", methods=["GET"])
def get_course_prerequisites():
    """Show all course prerequisites grouped by course."""
    all_prerequisites = get_all_course_prerequisites()
    grouped = group_course_prerequisites(all_prerequisites)

    return render_template(
        "course_prerequisites/index.html", grouped_prerequisites=grouped
    )


@course_prerequisite_bp.route("/create", methods=["GET", "POST"])
def create_course_prerequisite_view():
    """Create prerequisites for a given course."""
    courses = get_all_courses()
    if request.method == "POST":
        data = request.form
        course_id = data.get("course_id")
        prerequisite_ids = data.getlist("prerequisite_ids")
        errors = validate_prerequisites(course_id, prerequisite_ids)

        if errors:
            return render_template(
                "course_prerequisites/create.html",
                courses=courses,
                errors=errors,
            )

        create_course_prerequisites(course_id, prerequisite_ids)
        return redirect(
            url_for("course_prerequisites.get_course_prerequisites")
        )

    return render_template("course_prerequisites/create.html", courses=courses)


@course_prerequisite_bp.route(
    "/update/<int:course_id>", methods=["GET", "POST"]
)
def update_course_prerequisite_view(course_id):
    """Update prerequisites for a specific course."""
    course = get_course(course_id)

    if not course:
        return jsonify({"message": "Course not found"}), 404

    if request.method == "POST":
        if "delete_prerequisite_id" in request.form:
            to_delete = request.form["delete_prerequisite_id"]
            delete_course_prerequisite(course_id, int(to_delete))

            return redirect(
                url_for(
                    "course_prerequisites.update_course_prerequisite_view",
                    course_id=course_id,
                )
            )

        ids_to_delete = request.form.getlist("prerequisite_ids")
        for prerequisite_id in ids_to_delete:
            delete_course_prerequisite(course_id, prerequisite_id)

        new_prerequisite_ids = request.form.getlist("new_prerequisite[]")
        errors = validate_prerequisites(course_id, new_prerequisite_ids)

        if errors:
            return render_template(
                "course_prerequisites/edit.html",
                course=course,
                prerequisites=get_prerequisites_by_course(course_id),
                available_prerequisites=get_all_courses(),
                errors=errors,
            )

        create_course_prerequisites(course_id, new_prerequisite_ids)

        return redirect(
            url_for(
                "course_prerequisites.update_course_prerequisite_view",
                course_id=course_id,
            )
        )

    prerequisites = get_prerequisites_by_course(course_id)
    available_prerequisites = get_all_courses()

    return render_template(
        "course_prerequisites/edit.html",
        course=course,
        prerequisites=prerequisites,
        available_prerequisites=available_prerequisites,
    )


@course_prerequisite_bp.route(
    "/delete/<int:course_id>/<int:prerequisite_id>", methods=["POST"]
)
def delete_course_prerequisite_view(course_id, prerequisite_id):
    """Delete a prerequisite from a specific course."""
    course_prerequisite = get_course_prerequisite(course_id, prerequisite_id)
    if not course_prerequisite:
        return jsonify({"message": "Course prerequisite not found"}), 404

    delete_course_prerequisite(course_id, prerequisite_id)
    return redirect(url_for("course_prerequisites.get_course_prerequisites"))


def group_course_prerequisites(prerequisites):
    """Group prerequisites by their related course."""
    grouped = {}
    for pair in prerequisites:
        course = pair.course
        prerequisite = pair.prerequisite

        if course.id not in grouped:
            grouped[course.id] = {"name": course.name, "prerequisites": []}

        grouped[course.id]["prerequisites"].append(
            {"id": prerequisite.id, "name": prerequisite.name}
        )

    return grouped
