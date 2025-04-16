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

``source venv/bin/activate``
- En Windows (Command Prompt): 

``cd venv/Scripts && activate && cd ../../``
- En Windows (PowerShell): 

``.\venv\Scripts\Activate.ps1``

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

8. (Opcional, pero recomendado) Poblar la base de datos con datos de prueba

Ejecutar el siguiente comando:
```
python seed.py
```

9. Ejecutar la aplicación 
```
python run.py
```
