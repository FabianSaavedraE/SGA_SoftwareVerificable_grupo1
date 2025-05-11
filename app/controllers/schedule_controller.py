import pandas as pd

from app import db
from app.models import Schedule
from app.controllers.section_ranking_controller import get_sections_ranking
from app.controllers.timeslot_controller import (
    create_timeslots, find_consecutive_timeslot_blocks, 
    get_timeslots_by_parameters, is_timeslot_block_suitable
)
from app.controllers.classroom_controller import (
    get_available_classrooms_for_block, get_all_classrooms
)

from app.controllers.teacher_controller import is_teacher_available_for_timeslot
from app.controllers.student_controller import are_students_available_for_timeslot

YEAR = 2025
SEMESTER = 1
SCHEDULE_PATH = "horario.xlsx"

def generate_schedule():
    # BORRAR TODOS LOS HORARIOS EXISTENTES, HAGO ESTO PARA PODER PROBAR ETERNAMENTE
    # CON LAS MISMAS SECCIONES Y QUE NO TIRE PROBLEMAS DE QUE HAY TOPES DE HORARIOS
    # Se borra cuando este todo listo
    Schedule.query.delete()
    db.session.commit()
    print("[INFO] Todos los horarios anteriores han sido eliminados.")




    # Obtener ranking de CourseSections del año y semestre que se va a crear el horario
    # Cuando este listo, la idea es que el parametro de YEAR y SEMESTER se obtengan 
    # desde el front, con el usuario eligiendo estos valores
    ranked_sections = get_sections_ranking(year=YEAR, semester=SEMESTER)


    # si una de las secciones tiene más de 4 créditos, no se puede generar el horario
    if not ranked_sections:
        print(f"[DEBUG] No se puede generar un horario por problemas de créditos en las secciones.")
        return
    
    # si una sección no tiene estudiantes, no se puede generar el horario
    if not all_sections_have_students(ranked_sections):
        print(f"[DEBUG] No se puede generar un horario porque hay secciones sin estudiantes.")
        return
    
    if not can_all_sections_fit_in_classrooms(ranked_sections):
        print(f"[DEBUG] No se puede generar un horario por problema de Classrooms.")
        return





    create_timeslots(year=YEAR, semester=SEMESTER)

    timeslots = get_timeslots_by_parameters(YEAR, SEMESTER)

    print("\nRANKING:")
    for section in ranked_sections:
        print(section)

    for section in ranked_sections:
        print("SECTION IN MAIN:", section)
        # print(section)
        timeslot_block = find_consecutive_timeslot_blocks(section, timeslots)

        # block es un bloque de la cantidad de horas consecutivas para una seccion
        # si una seccion tienen 2 créditos, el bloque sería Ej: [9:00-10:00, 10:00-11:00]
        for block in timeslot_block:
            print("BLOCK:", block)

            # salas disponibles para ese bloque en particular
            available_classrooms = get_available_classrooms_for_block(block, section['num_students'])
            print("AVAILABLE CLASSROOMS:", available_classrooms)
            if not available_classrooms:
                continue

            # print("\nAVAILABLE CLASSROOMS:", available_classrooms)

            # valida si el profesor está disponible en ese bloque de horario
            if not is_teacher_available_for_timeslot(section, block):
                continue

            # valida si todos los estudiantes están disponibles para ese bloque de horario
            if not are_students_available_for_timeslot(section, block):
                continue

            classroom = available_classrooms[0]

            for timeslot in block:
                new_schedule = Schedule(
                    section_id=section['section'].id,
                    classroom_id=classroom.id,
                    time_slot_id=timeslot.id
                )

                db.session.add(new_schedule)

                print(f"[INFO] Section {section['section'].id} asignada a sala {classroom.name} en TimeSlot {timeslot.start_time} - {timeslot.end_time}")
            break

    db.session.commit()

    export_schedule_to_excel()

def all_sections_have_students(sections):
    for section_data in sections:
        if not section_data['section'].students:
            print(f"[DEBUG] La secction {section_data['section'].nrc} no tiene estudiantes asignados.")
            return False
        
    return True

def can_all_sections_fit_in_classrooms(sections):
    classrooms = get_all_classrooms()

    if not classrooms:
        print("[ERROR] No hay salas registradas en el sistema.")
        return False
    
    max_classroom_capacity = max(classroom.capacity for classroom in classrooms)

    for section_data in sections:
        if section_data['num_students'] > max_classroom_capacity:
            print(f"[ERROR] Max capacidad de Classrooms ({max_classroom_capacity}) "
                  f"es más chica que la máx cantidad de estudiantes. ({section_data['num_students']} en seccion {section_data['section'].nrc})")
            
            return False
        
    return True

def get_all_schedules():
    return Schedule.query.all()

def export_schedule_to_excel(filename=SCHEDULE_PATH):
    schedules = get_all_schedules()

    if not schedules:
        print("[INFO] No hay horarios generados.")
        return
    
    data = []
    for schedule in schedules:
        data.append({
            "NRC": schedule.section.nrc,
            "Day": schedule.time_slot.day,
            "TimeSlot": f"{schedule.time_slot.start_time.strftime('%H:%M')}-{schedule.time_slot.end_time.strftime('%H:%M')}",
            "Classroom": schedule.classroom.name
        })

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"[INFO] Horario exportado exitosamente a {filename}")
    