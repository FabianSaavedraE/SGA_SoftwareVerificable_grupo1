from app import db
from app.models import Schedule
from app.controllers.section_ranking_controller import get_sections_ranking
from app.controllers.timeslot_controller import (
    create_timeslots, get_timeslots_by_parameters
)
from app.validators.schedule_validator import is_schedule_feasible
from app.controllers.schedule_assigner import assign_sections
from app.controllers.schedule_exporter import export_schedule_to_excel

SCHEDULE_PATH = "app/static/horario.xlsx"

def generate_schedule(year, semester, export_path=SCHEDULE_PATH):
    clear_previous_schedule()

    ranked_sections, message = get_sections_ranking(year, semester)
    if not ranked_sections:
        print(f"Horario inviable: {message}")
        return False
    
    create_timeslots(year, semester)
    timeslots = get_timeslots_by_parameters(year, semester)

    if not is_schedule_feasible(ranked_sections, timeslots):
        print("Horario inviable según validaciones previas.")
        return False
    
    if assign_sections(ranked_sections, timeslots):
        export_schedule_to_excel(export_path)
        print("[SUCCESS] Horario generado correctamente.")
        return True
    
    print("No se pudo generar un horario válido.")
    return False

def clear_previous_schedule():
    Schedule.query.delete()
    db.session.commit()
    print("[INFO] Horarios anteriores eliminados")

def get_all_schedules():
    return Schedule.query.all()
