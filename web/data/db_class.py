import datetime
import sqlalchemy
# from db_session import SqlAlchemyBase
from flask_login import UserMixin, LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

class Student(SqlAlchemyBase):
    __tablename__ = 'student'

    id_student = sqlalchemy.Column(sqlalchemy.Integer,
                                   primary_key=True, unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(15), nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.VARCHAR(20), nullable=False)
    data_of_birth = sqlalchemy.Column(sqlalchemy.DATE, nullable=False)
    id_group = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("group.id_group"))
    gender = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=False)


class SprStill(SqlAlchemyBase):
    __tablename__ = 'spr_still'

    id_still = sqlalchemy.Column(sqlalchemy.Integer,
                                 primary_key=True, unique=True, nullable=False)
    still = sqlalchemy.Column(sqlalchemy.VARCHAR(10), unique=True, nullable=False)


class SprDist(SqlAlchemyBase):
    __tablename__ = 'spr_dist'

    id_spr_dist = sqlalchemy.Column(sqlalchemy.INT,
                                    primary_key=True, unique=True, nullable=False)
    long = sqlalchemy.Column(sqlalchemy.VARCHAR(4), unique=True, nullable=False)


class Result(SqlAlchemyBase):
    __tablename__ = 'result'

    id_result = sqlalchemy.Column(sqlalchemy.Integer,
                                  primary_key=True, autoincrement=True)
    id_still = sqlalchemy.Column(sqlalchemy.ForeignKey("spr_still.id_still"), nullable=False)
    id_dist = sqlalchemy.Column(sqlalchemy.ForeignKey("spr_dist.id_spr_dist"), nullable=False)
    id_student = sqlalchemy.Column(sqlalchemy.ForeignKey("student.id_student"), nullable=False)
    result = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    id_competition_r = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("competition.id_competition"),
                                         nullable=False)


class Group(SqlAlchemyBase):
    __tablename__ = 'group'

    id_group = sqlalchemy.Column(sqlalchemy.Integer,
                                 primary_key=True, unique=True, nullable=False)
    name_group = sqlalchemy.Column(sqlalchemy.VARCHAR(15), unique=True, nullable=False)
    id_couch = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("coach.id_coach"))


class Competition(SqlAlchemyBase):
    __tablename__ = 'competition'

    id_competition = sqlalchemy.Column(sqlalchemy.Integer,
                                       primary_key=True, unique=True, nullable=False)
    competition = sqlalchemy.Column(sqlalchemy.VARCHAR(20), nullable=False)
    data = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class Coach(SqlAlchemyBase, UserMixin):
    __tablename__ = 'coach'

    id_coach = sqlalchemy.Column(sqlalchemy.Integer,
                                 primary_key=True, unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(15), nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.VARCHAR(20), nullable=False)
    password_couch = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email_couch = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)

    def set_password(self, password):
        self.password_couch = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_couch, password)

    def get_id(self):
        return self.id_coach
