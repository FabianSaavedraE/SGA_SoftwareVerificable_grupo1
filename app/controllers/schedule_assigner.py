from app import db
from app.controllers.classroom_controller import (
    get_available_classrooms_for_block,
)
from app.controllers.student_controller import (
    are_students_available_for_timeslot,
)
from app.controllers.teacher_controller import (
    is_teacher_available_for_timeslot,
)
from app.controllers.timeslot_controller import generate_valid_block
from app.models import Schedule


def assign_sections(sections, timeslots, index=0):
    if index == len(sections):
        return True

    section_data = sections[index]
    section = section_data['section']
    num_students = section_data['num_students']

    possible_blocks = generate_valid_block(section_data, timeslots)
    for block, _ in possible_blocks:
        if not is_teacher_available_for_timeslot(section_data, block):
            continue

        if not are_students_available_for_timeslot(section_data, block):
            continue

        classrooms = get_available_classrooms_for_block(block, num_students)
        if not classrooms:
            continue

        assign_section(section, block, classrooms[0])
        if assign_sections(sections, timeslots, index + 1):
            return True

        unassign_section(section, block)

    return False


def assign_section(section, block, classroom):
    for timeslot in block:
        new_schedule = Schedule(
            section_id=section.id,
            time_slot_id=timeslot.id,
            classroom_id=classroom.id,
        )
        db.session.add(new_schedule)

    db.session.commit()


def unassign_section(section, block):
    timeslot_ids = [timeslot.id for timeslot in block]

    Schedule.query.filter(
        Schedule.section_id == section.id,
        Schedule.time_slot_id.in_(timeslot_ids),
    ).delete(synchronize_session='fetch')

    db.session.commit()
