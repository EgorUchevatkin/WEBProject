import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Student(SqlAlchemyBase):
    __tablename__ = 'student'

    id_student = sqlalchemy.Column(sqlalchemy.Integer,
                                   primary_key=True, unique=True, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(15), nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.TIME(20), nullable=True)
    data_of_birth = sqlalchemy.Column(sqlalchemy.DATE, nullable=True)
    id_group = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id_group"))
    gender = sqlalchemy.Column(sqlalchemy.BOOLEAN,
                               nullable=True)


class SprStill(SqlAlchemyBase):
    __tablename__ = 'spr_still'

    id_still = sqlalchemy.Column(sqlalchemy.Integer,
                                 primary_key=True, unique=True, nullable=True)
    still = sqlalchemy.Column(sqlalchemy.VARCHAR(10), unique=True, nullable=True)


class SprDist(SqlAlchemyBase):
    __tablename__ = 'spr_dist'

    id_spr_dist = sqlalchemy.Column(sqlalchemy.INT,
                                    primary_key=True, unique=True, nullable=True)
    long = sqlalchemy.Column(sqlalchemy.VARCHAR(4), unique=True, nullable=True)


class Result(SqlAlchemyBase):
    __tablename__ = 'result'

    id_result = sqlalchemy.Column(sqlalchemy.Integer,
                                  primary_key=True, autoincrement=True)
    id_still = sqlalchemy.Column(sqlalchemy.ForeignKey("spr_still.id_still"), nullable=True)
    id_dist = sqlalchemy.Column(sqlalchemy.ForeignKey("spr_dist.id_spr_dist"), nullable=True)
    id_student = sqlalchemy.Column(sqlalchemy.ForeignKey("student.id_student"), nullable=True)
    result = sqlalchemy.Column(sqlalchemy.TIME, nullable=True)
    id_competition = sqlalchemy.Column(sqlalchemy.ForeignKey("competition.id_competition"), nullable=True)


class Group(SqlAlchemyBase):
    __tablename__ = 'group'

    id_group = sqlalchemy.Column(sqlalchemy.Integer,
                                 primary_key=True, nullable=True)
    name_group = sqlalchemy.Column(sqlalchemy.VARCHAR(5), unique=True, nullable=True)
    id_couch = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("coach.id_coach"))


class Competition(SqlAlchemyBase):
    __tablename__ = 'competition'

    id_competition = sqlalchemy.Column(sqlalchemy.INT,
                                       primary_key=True, UNIQUE=True, nullable=True)
    competition = sqlalchemy.Column(sqlalchemy.VARCHAR(20), nullable=True)
    data = sqlalchemy.Column(sqlalchemy.DATE, nullable=True)


class Coach(SqlAlchemyBase):
    __tablename__ = 'coach'

    id_coach = sqlalchemy.Column(sqlalchemy.Integer,
                                 primary_key=True, unique=True, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(15), nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.VARCHAR(20), nullable=True)
