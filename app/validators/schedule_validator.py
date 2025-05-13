from app.controllers.teacher_controller import validate_teacher_overload
from app.controllers.classroom_controller import get_all_classrooms

MAX_CREDITS = 4

def is_schedule_feasible(sections, timeslots):
    valid_students, message = all_sections_have_students(sections)
    if not valid_students:
        return False, message
    
    valid_teachers, message = all_sections_have_teacher(sections)
    if not valid_teachers:
        return False, message
    
    valid_classrooms, message = validate_classroom_capacity(sections)
    if not valid_classrooms:
        return False, message
    
    valid_teacher_credits, message = validate_teacher_overload(
        sections, timeslots
    )
    if not valid_teacher_credits:
        return False, message
    
    valid_max_credits, message = validate_max_credits_per_section(sections)
    if not valid_max_credits:
        return False, message
    
    valid_demanded_timeslots, message = (
        validate_classroom_capacity_with_blocks(sections, timeslots)
    )
    if not valid_demanded_timeslots:
        return False, message
    
    return True, None

def all_sections_have_students(sections):
    for section_data in sections:
        section = section_data['section']
        if not section.students:
            message = (
                f"Sección {section_data['section'].nrc} no tiene "
                f"estudiantes asignados."
            )
            return False, message
        
    return True, None

def all_sections_have_teacher(sections):
    for section_data in sections:
        section = section_data['section']
        if not section.teacher:
            message = f"Sección {section.nrc} no tiene un profesor asignado."
            return False, message
        
    return True, None

def validate_max_credits_per_section(sections):
    for section_data in sections:
        section = section_data['section']

        if section.course_instance.course.credits > MAX_CREDITS:
            message = (
                f"No se le puede asignar un bloque consecutivo de "
                f"horario a la sección {section.nrc}."
            )
            
            return False, message
        
    return True, None

def validate_classroom_capacity(sections):
    classrooms = get_all_classrooms()
    if not classrooms:
        return False, "No hay salas disponibles en el sistema."
    
    max_section_size = max(
        section_data['num_students'] for section_data in sections
    )
    max_classroom_capacity = max(
        classroom.capacity for classroom in classrooms
    )

    if max_classroom_capacity < max_section_size:
        message = (
            f"La sala con mayor capacidad no puede acomodar a la "
            f"sección más grande."
        )
        return False, message

    return True, None

"""
Se compara la oferta total de bloques (40 * cantidad salas) con la demanda.
La demanda en este caso es la cantidad de créditos totales
"""
def validate_classroom_capacity_with_blocks(sections, timeslots):
    classrooms = get_all_classrooms()

    total_demanded_block = sum(
        section['section'].course_instance.course.credits for section in sections
    )

    total_available_block = len(timeslots) * len(classrooms)

    if total_demanded_block > total_available_block:
        message = (
            f"La demanda de horarios supera la oferta disponible. "
            f"No hay suficientes salas."
        )
        return False, message
    
    return True, None
