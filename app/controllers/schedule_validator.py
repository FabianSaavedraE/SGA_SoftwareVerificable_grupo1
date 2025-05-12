from app.controllers.teacher_controller import validate_teacher_overload

def is_schedule_feasible(sections, timeslots):
    valid, message = validate_teacher_overload(sections, timeslots)
    if not valid:
        print(f"[ERROR] {message}")
        return False
    
    if not all_sections_have_students(sections):
        print(f"[DEBUG] Hay secciones sin estudiantes.")
        return False
    
    return True

def all_sections_have_students(sections):
    for section_data in sections:
        section = section_data['section']
        if not section.students:
            print(f"[DEBUG] La sección {section_data['section'].nrc} no tiene estudiantes asignados.")
            return False
        
        return True
