# Diseño de Software Verificable - Sistema de Gestión Académica (SGA)

Este proyecto es una implementación de un Sistema de Gestión Académica (SGA), desarrollado como parte del curso "Diseño de Software Verificable". El sistema tiene como objetivo principal gestionar cursos, profesores, alumnos, secciones y evaluaciones y sus relaciones. Utiliza Python 3.9+, Flask como framework web y MySQL como base de datos.

# Requisitos previos
Antes de comenzar, deben estar instalados:
- Python 3.9 o superior
- pip
- MySQL

# Setup
1. Clonar el repositorio

2. Crear un entorno virtual 
```
python -m venv venv
```

3. Activar el entorno virtual:
- En Linux/Macos: 

`source venv/bin/activate`
- En Windows (Command Prompt): 

`cd venv/Scripts && activate && cd ../../`
- En Windows (PowerShell): 

`.\venv\Scripts\Activate.ps1`

4. Instalar las dependencias:
```
pip install -r requirements.txt
```

5. Crear la base de datos MySQL:

Abrir el cliente MySQL (con el usuario root) y ejecutar:
```
CREATE DATABASE academic_db;
```

6. Crear un archivo .env en la raíz del proyecto:

Crear un archivo llamado .env en el directorio raíz del proyecto con el siguiente contenido:
```
DATABASE_URI=mysql://root:tu_contraseña_mysql@localhost:3306/academic_db
FLASK_APP=run.py
FLASK_ENV=development
```

7. Inicializar las migraciones y crear las tablas en la base de datos
```
flask db init
flask db migrate
flask db upgrade
```

8. Ejecutar la aplicación 
```
python run.py
```

9. Carga de datos JSON

La carga de datos JSON debe seguir el siguiente órden dado:

 - Primeros tres, cualquiera de entre alumnos (botón de carga disponible en vista de alumnos), profesores (botón de carga disponible en vista de profesores), cursos (botón de carga disponible en vista de cursos)

 - Luego, el JSON de instancias de cursos (botón de carga disponible en vista de instancias de cursos).

 - Luego, el JSON de secciones de cursos con evaluaciones (botón de carga disponible en vista de secciones).

- Luego, el JSON de alumnos por sección (botón de carga disponible en vista de secciones).

- El JSON de evaluaciones y notas para alumnos (botón de carga disponible en vista de secciones)

- Finalmente las salas, el botón para agregar este JSON se encuentra en la vista de Salas.

Todos los JSON, especialmente los de creaciones de evaluación, siguen la lógica de verificación de suma de porcentajes.
Es necesario que estén en el formato correcto para cargar los datos. De otra forma, los datos simplemente no se guardan en la base de datos definida.

11. Generación de horarios.

Para la generación de horarios se debe hacer uso del ícono de calendario a la izquierda de todo, en el navbar.

Esto lleva a un menú donde se puede seleccionar el año y el semestre en que se genera el horario. Una vez generado el horario, este se puede descargar, reflejando el NRC, bloque de horario y sala para todas las secciones correspondientes del período de tiempo estipulado.
