# Users (teachers / students) constants ---------------------------------------
MAX_LENGTH_FIRST_NAME = 50
MAX_LENGTH_LAST_NAME = 50
MAX_LENGTH_EMAIL = 50
KEY_FIRST_NAME_ENTRY = "first_name"
KEY_LAST_NAME_ENTRY = "last_name"
KEY_EMAIL_ENTRY = "email"
KEY_ENTRY_YEAR = "entry_year"
MAX_LENGTH_USERS_NAME = 50
KEY_USER_NAME = "nombre"
MIN_VALID_ENTRY_YEAR = 1980
MAX_VALID_ENTRY_YEAR = 2025

# General use constants -------------------------------------------------------
MAX_NAME_LENGTH = 20
KEY_ID_ENTRY = "id"
KEY_NAME_ENTRY = "name"

# Classroom constants ---------------------------------------------------------
MIN_CAPACITY = 1
MAX_CAPACITY = 400
KEY_CAPACITY_JSON = "capacidad"
KEY_CAPACITY_ENTRY = "capacity"

# Course constants ------------------------------------------------------------
MAX_DESCRIPTION_LENGTH = 100
MIN_CREDITS_VALUE = 1
MAX_CREDITS_VALUE = 4
KEY_DESCRIPTION_ENTRY = "description"
KEY_CODE_ENTRY = "code"
KEY_CREDITS_ENTRY = "credits"
KEY_COURSE_ID_ENTRY = "course_id"

# Instance constants ----------------------------------------------------------
KEY_INSTANCE_JSON = "instancias"
KEY_SEMESTER_JSON = "semestre"
KEY_INSTANCE_COURSE_ID_JSON = "curso"
KEY_YEAR_JSON = "año"
KEY_YEAR_ENTRY = "year"
KEY_SEMESTER_ENTRY = "semester"
KEY_INSTANCE_ID_ENTRY = "instance_id"
KEY_COURSE_ID_JSON = "curso_id"
KEY_INSTANCE_COURSE_ID_ENTRY = "course_id"
KEY_INSTANCE_COURSE_ID_JSON = "curso_id"

# Section constants -----------------------------------------------------------

KEY_COURSE_INSTANCE_JSON = "instancia_curso"
KEY_TEACHER_ID_JSON = "profesor_id"
KEY_EVALUATION_JSON = "evaluacion"
KEY_EVALUATION_TYPE_JSON = "tipo"
KEY_TOPIC_COMBINATION_JSON = "combinacion_topicos"
KEY_TOPIC_NAME_JSON = "nombre"
KEY_TOPIC_VALUE_JSON = "valor"
KEY_TOPIC_JSON = "topicos"
KEY_TOPIC_QUANTITY_JSON = "cantidad"
KEY_TOPIC_TYPE_JSON = "tipo"
KEY_TOPIC_VALUES_JSON = "valores"
KEY_MANDATORY_EVALUATIONS_JSON = "obligatorias"

# Student Course constants ----------------------------------------------------
KEY_STUDENT_ENTRY = "alumno"
KEY_SECTION_ENTRY = "sección"
KEY_STUDENT_ID_JSON = "alumno_id"
KEY_STUDENT_ID_ENTRY = "student_id"
KEY_SECTION_ID_JSON = "seccion_id"
KEY_SECTION_ID_ENTRY = "course_section_id"
KEY_STATE_ENTRY = "inscrito"
KEY_PREREQUISITE = "prerrequisito"
NOT_COMPLETED_PREREQUISITES = "El alumno no ha aprobado todos los requisitos."

# Student Evaluations constants
KEY_TOPIC_ID_JSON = "topico_id"
KEY_TOPIC_ID_ENTRY = "evaluation_type_id"
KEY_INSTANCE_ID_JSON = "instancia"
KEY_INSTANCE_ID_ENTRY = "evaluation_id"
KEY_GRADE_JSON = "nota"
KEY_GRADE_ENTRY = "grade"
KEY_EVALUATION_TYPE = "topico"
NOT_ENROLLED_IN_SECTION = (
    "no pertenece a la sección del curso correspondiente a esta evaluación"
)

# Type checking text alerts ---------------------------------------------------

MUST_BE_STRING = "debe ser un string."
MUST_BE_INT = "debe ser un int"
MUST_BE_FLOAT = "debe ser un número."
MUST_BE_STRING_OR_INT = "debe ser un string o un int"
MUST_BE = "es obligatorio"
MUST_BE_LIST = "debe ser una lista"
MUST_BE_DICT = "debe ser un diccionario"
MUST_CONTAIN = "debe contener"
OVERFLOWS = "cae fuera del rango establecido de"
CHARACTERS = "caracteres"
ALREADY_EXISTS = "ya existe en la base de datos"
DOESNT_EXIST = "no existe en la base de datos"
DUPLICATED = "duplicado"
FORMAT_ERROR = "Error de formato, no es JSON."
FORMAT_KEY = "formato"
KEY_MUST_CONTAIN_INTS = "debe contener únicamente floats/ints"
MUST_BE_BOOL = "debe ser un booleano"

# JSON files KEYS -------------------------------------------------------------
KEY_DESCRIPTION_JSON = "descripcion"
KEY_CODE_JSON = "codigo"
KEY_CREDITS_JSON = "creditos"
KEY_COURSE_JSON = "cursos"

# Abbreviations ---------------------------------------------------------------
COURSE_CODE_PREFIX = "ICC"
CODE_LENGTH = 4
PERCENTAGE = "porcentaje"
