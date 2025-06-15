from app.controllers import teacher_controller as controller

def test_get_teacher_id_from_section():
    mock_section = {'section': type('Section', (), {'teacher_id': 123})()}
    assert controller.get_teacher_id_from_section(mock_section) == 123

def test_extract_timeslot_ids():
    class MockSlot:
        def __init__(self, id):
            self.id = id
    block = [MockSlot(1), MockSlot(2), MockSlot(3)]

    assert controller.extract_timeslot_ids(block) == [1, 2, 3]

def test_validate_teacher_overload_passes():
    class MockSection:
        def __init__(self, teacher_id):
            self.teacher_id = teacher_id

    ranked_sections = [
        {'section': MockSection(1), 'num_credits': 2},
        {'section': MockSection(2), 'num_credits': 3},
        {'section': MockSection(1), 'num_credits': 1}
    ]

    class MockTimeslot:
        def __init__(self, day, start_time):
            self.day = day
            self.start_time = start_time

    timeslots = [
        MockTimeslot('Monday', 9),
        MockTimeslot('Tuesday', 9),
        MockTimeslot('Wednesday', 9)
    ]

    result, message = (
        controller.validate_teacher_overload(ranked_sections, timeslots)
    )

    assert result is True
    assert message == ''

def test_validate_teacher_overload_fails():
    class MockSection:
        def __init__(self, teacher_id):
            self.teacher_id = teacher_id

    ranked_sections = [
        {'section': MockSection(1), 'num_credits': 4},
    ]

    class MockTimeslot:
        def __init__(self, day, start_time):
            self.day = day
            self.start_time = start_time

    timeslots = [
        MockTimeslot('Monday', 9),
        MockTimeslot('Tuesday', 9),
        MockTimeslot('Wednesday', 9)
    ]

    result, message = (
        controller.validate_teacher_overload(ranked_sections, timeslots)
    )

    assert result is False
    assert 'profesor con ID 1' in message
