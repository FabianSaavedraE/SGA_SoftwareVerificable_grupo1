from flask import Blueprint, render_template, request, url_for

from app.controllers.schedule_controller import generate_schedule

FILE_NAME = "horario.xlsx"

schedule_bp = Blueprint("schedules", __name__, url_prefix="/schedules")


@schedule_bp.route("/", methods=["GET"])
def show_generate_schedule_view():
    """Render the view to generate a schedule."""
    return render_template("schedules/generate_schedule.html")


@schedule_bp.route("/", methods=["POST"])
def generate_schedule_view():
    """Generate a schedule based on year and semester."""
    year = int(request.form.get("year"))
    semester = int(request.form.get("semester"))

    success, message = generate_schedule(year=year, semester=semester)
    error = None

    if success:
        error = False
        file_link = url_for("static", filename=FILE_NAME)
    else:
        error = True
        file_link = None

    return render_template(
        "schedules/generate_schedule.html",
        message=message,
        file_link=file_link,
        error=error,
    )
