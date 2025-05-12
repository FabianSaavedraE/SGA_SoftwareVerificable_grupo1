import pandas as pd

from app.models import Schedule

def export_schedule_to_excel(path):
    schedules = Schedule.query.all()

    if not schedules:
        print("[INFO] No hay horarios para exportar.")
        return
    
    data = [{
        "NRC": schedule.section.nrc,
        "Day": schedule.time_slot.day,
        "TimeSlot": f"{schedule.time_slot.start_time.strftime('%H:%M')}-"
                    f"{schedule.time_slot.end_time.strftime('%H:%M')}",
        "Classroom": schedule.classroom.name
    } for schedule in schedules]

    pd.DataFrame(data).to_excel(path, index=False)
    print(f"[INFO] Horario exportado a {path}")
