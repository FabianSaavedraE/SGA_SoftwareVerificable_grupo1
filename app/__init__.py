from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()


from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)   

    from app.models import course_section
    from app.models import course_instance
    from app.models import student_course
    from app.models import evaluation_type
    from app.models import evaluation
    from app.models import course
    from app.models import student
    from app.models import teacher
    from app.models import course_prerequisite
    from app.models import student_evaluation
    from app.models import schedule
    from app.models import classroom


    from app.routes.course_routes import course_bp
    app.register_blueprint(course_bp)

    from app.routes.student_routes import student_bp
    app.register_blueprint(student_bp)

    from app.routes.teacher_routes import teacher_bp
    app.register_blueprint(teacher_bp)

    from app.routes.course_section_routes import course_section_bp
    app.register_blueprint(course_section_bp)

    from app.routes.student_course_routes import student_course_bp
    app.register_blueprint(student_course_bp)

    from app.routes.evaluation_type_routes import evaluation_type_bp
    app.register_blueprint(evaluation_type_bp)

    from app.routes.evaluation_routes import evaluation_bp
    app.register_blueprint(evaluation_bp)
    
    from app.routes.student_evaluation_routes import student_evaluation_bp
    app.register_blueprint(student_evaluation_bp)

    from app.routes.course_prerequisite_routes import course_prerequisite_bp  
    app.register_blueprint(course_prerequisite_bp)  

    from app.routes.course_instance_routes import course_instance_bp
    app.register_blueprint(course_instance_bp)

    from app.routes.schedule_routes import schedule_bp
    app.register_blueprint(schedule_bp)

    from app.routes.classroom_routes import classroom_bp
    app.register_blueprint(classroom_bp)

    return app