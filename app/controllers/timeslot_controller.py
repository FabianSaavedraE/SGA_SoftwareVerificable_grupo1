from datetime import time

from app import db
from app.models import TimeSlot
from app.controllers.teacher_controller import (
    is_teacher_available_for_timeslot
)
from app.controllers.student_controller import (
    are_students_available_for_timeslot
)
from app.controllers.classroom_controller import (
    get_available_classrooms_for_block
)

DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
VALID_TIME_BLOCKS = [
    (9, 10), (10, 11), (11, 12), (12, 13),
    (14, 15), (15, 16), (16, 17), (17, 18)
]

def create_timeslots(year, semester):
    if timeslots_exist(year, semester):
        return

    generate_and_save_timeslot(year, semester)

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

def get_all_timeslots():
    return TimeSlot.query.all()

def get_timeslots_by_parameters(year, semester):
    return TimeSlot.query.filter_by(year=year, semester=semester).all()

def generate_valid_block(section_data, timeslots):
    valid_options = []
    num_students = section_data['num_students']

    candidate_blocks = find_consecutive_timeslot_blocks(
        section_data, timeslots
    )

    for block in candidate_blocks:
        if not is_teacher_available_for_timeslot(section_data, block):
            continue

        if not are_students_available_for_timeslot(section_data, block):
            continue

        available_classrooms = get_available_classrooms_for_block(
            block, num_students
        )
        if not available_classrooms:
            continue

        valid_options.append((block, available_classrooms[0]))

    return valid_options

def find_consecutive_timeslot_blocks(section, timeslots):
    required_block_size = section['num_credits']
    consecutive_blocks = []

    timeslots_by_day = group_timeslots_by_day(timeslots)

    for _, day_slots in timeslots_by_day.items():
        sorted_slots = sorted(day_slots, key=lambda slot: slot.start_time)

        for start_index in range(len(sorted_slots) - required_block_size + 1):
            block = sorted_slots[start_index:start_index + required_block_size]

            if are_consecutive_blocks(block):
                consecutive_blocks.append(block)

    return consecutive_blocks

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
