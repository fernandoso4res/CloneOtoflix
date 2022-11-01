from flask_pymongo import PyMongo
from config import MONGO_URI_USERS, MONGO_URI_COURSES, MONGO_URI_QUESTIONS, MONGO_URI_BENEFITS_CLUB, REDIS_HOST, REDIS_PORT
import redis



users_db = PyMongo()
courses_db = PyMongo()
questions_db = PyMongo()
benefits_club_bd = PyMongo()


def init_app(app):
    users_db.init_app(app, uri=MONGO_URI_USERS)
    courses_db.init_app(app, uri=MONGO_URI_COURSES)
    questions_db.init_app(app, uri=MONGO_URI_QUESTIONS)
    benefits_club_bd.init_app(app, uri=MONGO_URI_BENEFITS_CLUB)


def redis_conn():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
