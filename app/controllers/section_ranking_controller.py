from app.controllers.course_section_controller import (
    get_course_sections_by_parameters
)

SHARED_SECTIONS_WEIGHT = 0.3
CREDITS_WEIGHT = 0.5
STUDENTS_WEIGHT = 0.2

def get_sections_ranking(year, semester):
    course_sections = get_course_sections_by_parameters(year, semester)

    if not course_sections:
        message = f"No hay secciones para el periodo {year}-{semester}"
        return None, message

    sections_with_metrics = get_all_sections_metrics(course_sections)
    ranking = rank_sections(sections_with_metrics)

    return ranking, None

def rank_sections(sections):
    scored_sections = calculate_scores(sections)
    return sorted(
        scored_sections,
        key=lambda section: section['score'],
        reverse=True
    )

def calculate_scores(sections):
    num_students_list = get_attributes_from_sections(sections, 'num_students')
    num_credits_list = get_attributes_from_sections(sections, 'num_credits')
    shared_sections_list = get_attributes_from_sections(
        sections, 'shared_sections'
    )

    normalized_students = normalize(num_students_list)
    normalized_credits = normalize(num_credits_list)
    normalized_shared_sections = normalize(shared_sections_list)

    for index, section in enumerate(sections):
        section['score'] = (
            normalized_students[index] * STUDENTS_WEIGHT
            + normalized_credits[index] * CREDITS_WEIGHT
            + normalized_shared_sections[index] * SHARED_SECTIONS_WEIGHT
        )

    return sections

def get_attributes_from_sections(rankings, attribute):
    return [section[attribute] for section in rankings]

def get_all_sections_metrics(sections):
    return [build_section_metrics(section, sections) for section in sections]

def build_section_metrics(section, all_sections):
    return {
        'section': section,
        'num_students': len(get_students_ids(section)),
        'num_credits': section.course_instance.course.credits,
        'shared_sections': count_shared_sections(section, all_sections)
    }

def count_shared_sections(section, all_sections):
    """Obtener con cuántas otras secciones se comparten estudiantes"""
    section_ids = get_students_ids(section)
    count = 0

    for other in all_sections:
        if section.id == other.id:
            continue

        if section_ids & get_students_ids(other):
            count += 1
    
    return count

def get_students_ids(section):
    return {student.id for student in section.students}

def normalize(values):
    min_val = min(values)
    max_val = max(values)

    if min_val == max_val:
        return [0.0] * len(values)
    
    return [(v-min_val) / (max_val-min_val) for v in values]
