import pandas as pd

from app.models import Schedule


def get_schedule_data():
    """Get all schedules as a list of dictionaries."""
    schedules = Schedule.query.all()
    if not schedules:
        return []

    return [
        {
            "NRC": schedule.section.nrc,
            "Day": schedule.time_slot.day,
            "TimeSlot": format_time_slot(schedule),
            "Classroom": schedule.classroom.name,
        }
        for schedule in schedules
    ]


def format_time_slot(schedule):
    """Return the time slot as a string like '08:00-09:30'."""
    start = schedule.time_slot.start_time.strftime("%H:%M")
    end = schedule.time_slot.end_time.strftime("%H:%M")

    return f"{start}-{end}"


def export_schedule_to_excel(path):
    """Save the schedule to an Excel file at the given path."""
    data = get_schedule_data()
    if data:
        pd.DataFrame(data).to_excel(path, index=False)
