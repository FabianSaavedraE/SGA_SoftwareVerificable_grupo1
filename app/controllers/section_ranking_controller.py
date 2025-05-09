def rank_sections(rankings, weights=None):
    num_students_list = [r['num_students'] for r in rankings]
    num_credits_list = [r['num_credits'] for r in rankings]
    shared_sections_list = [r['shared_sections'] for r in rankings]

    students_normalized = normalize(num_students_list)
    credits_normalized = normalize(num_credits_list)
    shared_sections_normalized = normalize(shared_sections_list)

    for i, r in enumerate(rankings):
        weight_students = weights['students'] if weights else 1
        weights_credits = weights['credits'] if weights else 1
        weights_shared_sections = weights['shared'] if weights else 1

        r['score'] = (
            students_normalized[i] * weight_students +
            credits_normalized[i] * weights_credits +
            shared_sections_normalized[i] * weights_shared_sections
        )

    return sorted(rankings, key=lambda x: x['score'], reverse=True)

def generate_section_ranking(sections):
    return [build_section_ranking(section, sections) for section in sections]

def build_section_ranking(section, all_sections):
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
