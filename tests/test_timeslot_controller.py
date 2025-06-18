from datetime import time

from app.controllers import timeslot_controller as controller


class MockSlot:
    def __init__(self, day, start_time, end_time):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time


def test_sort_timeslots_by_start_time():
    """Test sorting timeslots by their start time."""
    slots = [
        MockSlot("Monday", time(10), time(11)),
        MockSlot("Monday", time(9), time(10)),
        MockSlot("Monday", time(11), time(12)),
    ]
    sorted_slots = controller.sort_timeslots_by_start_time(slots)

    assert [s.start_time for s in sorted_slots] == [
        time(9),
        time(10),
        time(11),
    ]


def test_are_consecutive_blocks_true():
    """Test that consecutive time blocks are detected as True."""
    slots = [
        MockSlot("Monday", time(9), time(10)),
        MockSlot("Monday", time(10), time(11)),
        MockSlot("Monday", time(11), time(12)),
    ]

    assert controller.are_consecutive_blocks(slots) is True


def test_are_consecutive_blocks_false():
    """Test that non-consecutive time blocks are detected as False."""
    slots = [
        MockSlot("Monday", time(9), time(10)),
        MockSlot("Monday", time(11), time(12)),
    ]

    assert controller.are_consecutive_blocks(slots) is False


def test_group_timeslots_by_day():
    """Test grouping timeslots by day of the week."""
    slots = [
        MockSlot("Monday", time(9), time(10)),
        MockSlot("Tuesday", time(9), time(10)),
        MockSlot("Monday", time(10), time(11)),
    ]
    grouped = controller.group_timeslots_by_day(slots)

    assert set(grouped.keys()) == {"Monday", "Tuesday"}
    assert len(grouped["Monday"]) == 2
    assert len(grouped["Tuesday"]) == 1


def test_extract_valid_blocks():
    """Test extracting valid consecutive blocks of a given size."""
    slots = [
        MockSlot("Monday", time(9), time(10)),
        MockSlot("Monday", time(10), time(11)),
        MockSlot("Monday", time(11), time(12)),
        MockSlot("Monday", time(13), time(14)),
    ]
    valid_blocks = controller.extract_valid_blocks(slots, 3)

    assert len(valid_blocks) == 1
    assert valid_blocks[0] == slots[:3]


def test_get_consecutive_blocks():
    """Test getting all consecutive blocks of timeslots by day."""
    slots_by_day = {
        "Monday": [
            MockSlot("Monday", time(9), time(10)),
            MockSlot("Monday", time(10), time(11)),
            MockSlot("Monday", time(11), time(12)),
            MockSlot("Monday", time(13), time(14)),
        ],
        "Tuesday": [
            MockSlot("Tuesday", time(9), time(10)),
            MockSlot("Tuesday", time(10), time(11)),
        ],
    }
    blocks = controller.get_consecutive_blocks(slots_by_day, 3)

    assert len(blocks) == 1
    assert blocks[0] == slots_by_day["Monday"][:3]
