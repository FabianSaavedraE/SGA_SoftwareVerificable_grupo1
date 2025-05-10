from datetime import time

from app import db
from app.models import TimeSlot

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
VALID_TIME_BLOCKS = [
    (9, 10), (10, 11), (11, 12), (12, 13),
    (14, 15), (15, 16), (16, 17), (17, 18)
]

def get_all_timeslots():
    return TimeSlot.query.all()

def get_timeslots_by_parameters(year, semester):
    return TimeSlot.query.filter_by(year=year, semester=semester).all()

def create_timeslots(year, semester):
    if timeslots_exist(year, semester):
        print(f"TimeSlots ya existen para {year} semester {semester}")
        return

    generate_and_save_timeslot(year, semester)
    print(f"TimeSlots generados para {year} semester{semester}")

def timeslots_exist(year, semester):
    return (
        TimeSlot.query.filter_by(year=year, semester=semester).first() 
        is not None
    )

def generate_and_save_timeslot(year, semester):
    for day in DAYS_OF_WEEK:
        for start_hour, end_hour in VALID_TIME_BLOCKS:
            slot = TimeSlot(
                day=day,
                start_time=time(hour=start_hour),
                end_time=time(hour=end_hour),
                year=year,
                semester=semester
            )

            db.session.add(slot)
    db.session.commit()

def group_timeslots_by_day(timeslots):
    timeslots_by_day = {}
    for slot in timeslots:
        timeslots_by_day.setdefault(slot.day, []).append(slot)

    return timeslots_by_day

def are_consecutive_blocks(time_block):
    for index in range(len(time_block) - 1):
        current_end = time_block[index].end_time
        next_start = time_block[index + 1].start_time

        if current_end != next_start:
            return False
        
    return True

def find_consecutive_timeslot_blocks(section, timeslots):
    print("\nSECTION:", section)
    required_block_size = section['num_credits']
    consecutive_blocks = []

    timeslots_by_day = group_timeslots_by_day(timeslots)

    for day, day_slots in timeslots_by_day.items():
        sorted_slots = sorted(day_slots, key=lambda slot: slot.start_time)

        for start_index in range(len(sorted_slots) - required_block_size + 1):
            block = sorted_slots[start_index:start_index + required_block_size]

            if are_consecutive_blocks(block):
                consecutive_blocks.append(block)

    return consecutive_blocks
