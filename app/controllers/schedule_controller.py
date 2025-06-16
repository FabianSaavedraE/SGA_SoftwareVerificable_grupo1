from app import db
from app.controllers.schedule_assigner import assign_sections
from app.controllers.schedule_exporter import export_schedule_to_excel
from app.controllers.section_ranking_controller import get_sections_ranking
from app.controllers.timeslot_controller import (
    create_timeslots,
    get_timeslots_by_parameters,
)
from app.models import Schedule
from app.validators.schedule_validator import is_schedule_feasible

SCHEDULE_PATH = 'app/static/horario.xlsx'


def generate_schedule(year, semester, export_path=SCHEDULE_PATH):
    clear_previous_schedule()

    ranked_sections, error_message = get_sections_ranking(year, semester)
    if not ranked_sections:
        return False, error_message

    create_timeslots(year, semester)
    timeslots = get_timeslots_by_parameters(year, semester)

    success_previous_validations, error_message = is_schedule_feasible(
        ranked_sections, timeslots
    )

    if not success_previous_validations:
        return False, error_message

    if assign_sections(ranked_sections, timeslots):
        export_schedule_to_excel(export_path)
        message = 'Horario generado exitosamente.'
        return True, message

    return False, 'No se pudo generar un horario.'


def clear_previous_schedule():
    Schedule.query.delete()
    db.session.commit()


def get_all_schedules():
    return Schedule.query.all()
