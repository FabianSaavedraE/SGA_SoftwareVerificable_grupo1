from flask import Blueprint, request, render_template, redirect, url_for, flash

from app.controllers.schedule_controller import generate_schedule

FILE_NAME = "horario.xlsx"

schedule_bp = Blueprint('schedules', __name__, url_prefix='/schedules')

@schedule_bp.route('/', methods=['GET'])
def show_generate_schedule_view():
    return render_template('schedules/generate_schedule.html')

@schedule_bp.route('/', methods=['POST'])
def generate_schedule_view():
    year = int(request.form.get('year'))
    semester = int(request.form.get('semester'))

    success = generate_schedule(year=year, semester=semester)

    if success:
        message = "Horario generado exitosamente. Puedes descargar el archivo."
        file_link = url_for('static', filename=FILE_NAME)
    else:
        message = "No se pudo generar un horario válido."
        file_link = None

    return render_template(
        'schedules/generate_schedule.html',
        message=message,
        file_link=file_link
    )
