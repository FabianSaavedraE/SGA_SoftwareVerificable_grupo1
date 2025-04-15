# Diseño de Software Verificable - Sistema de Gestión Académica (SGA)

Este proyecto es una implementación de un Sistema de Gestión Académica (SGA), desarrollado como parte del curso "Diseño de Software Verificable". El sistema tiene como objetivo principal gestionar cursos, profesores, alumnos, secciones y evaluaciones y sus relaciones. Utiliza Python 3.9+, Flask como framework web y MySQL como base de datos.

# Setup
1. Crear un virtual environment 

```
python -m venv .venv
```

2. Activar el virtual environment:
- En Linux/Macos: ``source .venv/bin/activate``
- En Windows (Command Prompt): ``cd .venv/Scripts && activate && cd ../../``
- En Windows (PowerShell): ``.\.venv\Scripts\Activate.ps1``

3. Instalar las dependencias:
```
pip install -r requirements.txt
```

4. Crear una base de datos en MySQL


5. Crear un archivo .env en la carpeta raíz del proyecto. Es decir, en SGA_SOFTWAREVERIFICABLE_GRUPO1/

6. Dentro de este archivo .env, agregar las credenciales de la base de datos MySQL. Ejemplo:
```
DATABASE_URI=mysql://root:{mysql password}@localhost/{database name}
FLASK_APP=run.py
FLASK_ENV=development
```

7. Antes de ejecutar la aplicación, correr el archivo seed.py con `python seed.py` (Esto es opcional, pero sugerido para revisar eliminaciones y testear las relaciones entre entidades rápidamente)

8. Ejecutar la aplicación con: `python run.py`
