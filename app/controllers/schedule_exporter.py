import pandas as pd

from app.models import Schedule


def get_schedule_data():
    schedules = Schedule.query.all()
    if not schedules:
        return []

    return [
        {
            'NRC': schedule.section.nrc,
            'Day': schedule.time_slot.day,
            'TimeSlot': format_time_slot(schedule),
            'Classroom': schedule.classroom.name,
        }
        for schedule in schedules
    ]


def format_time_slot(schedule):
    start = schedule.time_slot.start_time.strftime('%H:%M')
    end = schedule.time_slot.end_time.strftime('%H:%M')

    return f'{start}-{end}'


def export_schedule_to_excel(path):
    data = get_schedule_data()
    if data:
        pd.DataFrame(data).to_excel(path, index=False)
