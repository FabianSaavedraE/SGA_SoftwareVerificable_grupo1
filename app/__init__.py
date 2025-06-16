import os
import sqlite3

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.config import Config

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.close()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = os.getenv('SECRET_KEY')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

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
