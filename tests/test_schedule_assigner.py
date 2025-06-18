from app.controllers.schedule_assigner import assign_sections


class MockTimeslot:
    """Mock timeslot with an identifier."""

    def __init__(self, id):
        self.id = id


class MockSection:
    """Mock section with an identifier."""

    def __init__(self, id):
        self.id = id


class MockClassroom:
    """Mock classroom with an identifier."""

    def __init__(self, id):
        self.id = id


def test_assign_sections_returns_false_when_no_valid_block(monkeypatch):
    """Returns False if no valid time block is found for section assignment."""
    section_data = {"section": MockSection(1), "num_students": 30}
    sections = [section_data]
    timeslots = [MockTimeslot(1), MockTimeslot(2)]

    monkeypatch.setattr(
        "app.controllers.schedule_assigner.generate_valid_block",
        lambda section, ts: [],
    )
    monkeypatch.setattr(
        "app.controllers.schedule_assigner.is_teacher_available_for_timeslot",
        lambda s, b: True,
    )
    monkeypatch.setattr(
        "app.controllers.schedule_assigner.are_students_available_for_timeslot",
        lambda s, b: True,
    )
    monkeypatch.setattr(
        "app.controllers.schedule_assigner.get_available_classrooms_for_block",
        lambda b, n: [MockClassroom(1)],
    )
    monkeypatch.setattr(
        "app.controllers.schedule_assigner.assign_section",
        lambda s, b, c: None,
    )
    monkeypatch.setattr(
        "app.controllers.schedule_assigner.unassign_section", lambda s, b: None
    )

    result = assign_sections(sections, timeslots)
    assert result is False


def test_assign_sections_success_path(monkeypatch):
    """Returns True when sections are successfully assigned to blocks."""
    section_data = {"section": MockSection(1), "num_students": 30}
    sections = [section_data]
    timeslots = [MockTimeslot(1), MockTimeslot(2)]
    block = [MockTimeslot(1), MockTimeslot(2)]

    monkeypatch.setattr(
        "app.controllers.schedule_assigner.generate_valid_block",
        lambda section, ts: [(block, None)],
    )
    monkeypatch.setattr(
        "app.controllers.schedule_assigner.is_teacher_available_for_timeslot",
        lambda s, b: True,
    )
    monkeypatch.setattr(
        "app.controllers.schedule_assigner.are_students_available_for_timeslot",
        lambda s, b: True,
    )
    monkeypatch.setattr(
        "app.controllers.schedule_assigner.get_available_classrooms_for_block",
        lambda b, n: [MockClassroom(1)],
    )
    monkeypatch.setattr(
        "app.controllers.schedule_assigner.assign_section",
        lambda s, b, c: None,
    )
    monkeypatch.setattr(
        "app.controllers.schedule_assigner.unassign_section", lambda s, b: None
    )

    result = assign_sections(sections, timeslots)
    assert result is True
