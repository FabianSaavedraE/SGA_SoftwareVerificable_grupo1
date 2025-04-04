from flask import Blueprint, jsonify, request
from app.models.course import Course
from app.controllers.course_controllers import getAllCourses
from app import db

course_bp = Blueprint('course_bp', __name__, url_prefix='/courses')

@course_bp.route('/', methods=['GET'])
def getCourses():
    return jsonify(getAllCourses())