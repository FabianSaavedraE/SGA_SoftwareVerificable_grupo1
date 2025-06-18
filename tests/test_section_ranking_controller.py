from app.controllers import section_ranking_controller as controller


class MockCourse:
    """Mock class to simulate a Course with credits."""

    def __init__(self, credits):
        self.credits = credits


class MockCourseInstance:
    """Mock class to simulate a CourseInstance with a linked Course."""

    def __init__(self, credits):
        self.course = MockCourse(credits)


class MockStudent:
    """Mock class to simulate a Student with an ID."""

    def __init__(self, id):
        self.id = id


class MockSection:
    """Mock class to simulate a Section with students and course info."""

    def __init__(self, id, students, credits):
        self.id = id
        self.students = students
        self.course_instance = MockCourseInstance(credits)


def test_get_students_ids():
    """Test getting a set of student IDs from a section."""
    section = MockSection(1, [MockStudent(1), MockStudent(2)], 5)
    result = controller.get_students_ids(section)
    assert result == {1, 2}


def test_count_shared_sections():
    """Test counting how many sections share students with a given section."""
    s1 = MockSection(1, [MockStudent(1), MockStudent(2)], 5)
    s2 = MockSection(2, [MockStudent(2), MockStudent(3)], 5)
    s3 = MockSection(3, [MockStudent(4)], 5)
    result = controller.count_shared_sections(s1, [s1, s2, s3])

    assert result == 1


def test_normalize():
    """Test normalization of a list of numeric values."""
    values = [10, 20, 30]
    normalized = controller.normalize(values)

    assert normalized == [0.0, 0.5, 1.0]


def test_normalize_all_equal():
    """Test normalization when all values are equal (returns zeros)."""
    values = [5, 5, 5]
    normalized = controller.normalize(values)

    assert normalized == [0.0, 0.0, 0.0]


def test_calculate_scores():
    """Test that scores are calculated and returned as floats."""
    section = MockSection(1, [MockStudent(1), MockStudent(2)], 5)
    section_data = {
        "section": section,
        "num_students": 2,
        "num_credits": 5,
        "shared_sections": 1,
    }
    result = controller.calculate_scores([section_data])

    assert "score" in result[0]
    assert isinstance(result[0]["score"], float)


def test_rank_sections():
    """Test ranking of sections by their calculated scores descending."""
    s1 = {
        "section": None,
        "num_students": 10,
        "num_credits": 5,
        "shared_sections": 1,
    }
    s2 = {
        "section": None,
        "num_students": 20,
        "num_credits": 3,
        "shared_sections": 2,
    }
    s3 = {
        "section": None,
        "num_students": 5,
        "num_credits": 4,
        "shared_sections": 0,
    }

    result = controller.rank_sections([s1, s2, s3])
    scores = [s["score"] for s in result]

    assert scores == sorted(scores, reverse=True)
