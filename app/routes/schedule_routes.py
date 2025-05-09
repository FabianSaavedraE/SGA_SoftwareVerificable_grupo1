from flask import Blueprint, request, render_template, redirect, url_for

from app.controllers.schedule_controller import generate_schedule

schedule_bp = Blueprint('schedules', __name__, url_prefix='/schedules')

@schedule_bp.route('/generate', methods=['GET'])
def show_generate_schedule_view():
    return render_template('schedules/generate_schedule.html')


@schedule_bp.route('/generate', methods=['POST'])
def generate_schedule_view():
    success = generate_schedule()

    if success:
        print("Horario generado exitosamente.")
    else:
        print("No se pudo generar un horario válido con los datos actuales")

    return redirect(url_for('landing_page'))