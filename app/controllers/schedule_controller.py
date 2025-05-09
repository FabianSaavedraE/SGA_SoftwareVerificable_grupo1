from app.controllers.course_section_controller import (
    get_course_sections_by_parameters
)

from app.controllers.section_ranking_controller import (
    generate_section_ranking,
    rank_sections
)

SHARED_SECTIONS_WEIGHT = 0.5
CREDITS_WEIGHT = 0.3
STUDENTS_WEIGHT = 0.2

def generate_schedule():
    course_sections = get_course_sections_by_parameters(year=2025, semester=1)
    raw_rankings = generate_section_ranking(course_sections)

    for r in raw_rankings:
        print(r)

    weights = {
        'shared': SHARED_SECTIONS_WEIGHT,
        'credits': CREDITS_WEIGHT,
        'students': STUDENTS_WEIGHT
    }

    final_rankings = rank_sections(raw_rankings, weights)

    print("\nFINAL RANKINGS")
    for f in final_rankings:
        print(f)
