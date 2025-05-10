from app.controllers.section_ranking_controller import get_sections_ranking
from app.controllers.timeslot_controller import (
    create_timeslots, find_consecutive_timeslot_blocks, 
    get_timeslots_by_parameters
)
from app.controllers.classroom_controller import (
    get_available_classrooms_for_block
)

from app.controllers.teacher_controller import (
    is_teacher_available_for_timeslot
)

from app.controllers.student_controller import (
    are_students_available_for_timeslot
)

from app.models import Schedule, CourseSection, TimeSlot, StudentCourses

from app import db

YEAR = 2025
SEMESTER = 1

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

    if not ranked_sections:
        print(f"[DEBUG] No se puede generar un horario por problemas de créditos en las secciones.")
        return





    create_timeslots(year=YEAR, semester=SEMESTER)

    timeslots = get_timeslots_by_parameters(YEAR, SEMESTER)

    # for t in timeslots:
    #     print(t)

    # PARA MOSTRAR EL RANKING DE LAS SECCIONES, todavía me falta mejorar esta parte
    # para que se exluyan las secciones que no tienen estudiantes, o que el código
    # de generacion de horario simplemente termine si es que ocurre el caso de 
    # que hay secciones sin estudiantes
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




    """
    consecutive_block es una lista de listas, donde cada sublista es el bloque
    completo que requiere la seccion. 

    Ejemplo:    
        Si una sección tiene 4 créditos, las sublistas van a estar compuestas de 
        4 bloques (equivalentes a 4 horas).

        Un bloque se ve así:
        [Monday 09:00-10:00, Monday 10:00-11:00, Monday 11:00-12:00, Monday 12:00-13:00]
    """
