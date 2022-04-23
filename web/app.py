from flask import Flask, render_template, redirect, request, url_for
from web.data import db_session
from web.data.db_class import Student, Coach, Group, Result, SprStill, SprDist, Competition
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/web_db.db")


@app.route('/')
@app.route('/profile')
def index():
    id = 1
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id_student == id).first()
    group = db_sess.query(Group).filter(Group.id_group == student.id_group).first()
    coach = db_sess.query(Coach).filter(Coach.id_coach == group.id_couch).first()
    today = date.today()
    birth_date = student.data_of_birth
    student_birth = today.year - birth_date.year
    if today.month < birth_date.month or today.month == birth_date.month and today.day < birth_date.day:
        student_birth -= 1
    result_st = []
    for result in db_sess.query(Result).filter(Result.id_student == student.id_student).all():
        result_st.append([db_sess.query(SprDist).filter(SprDist.id_spr_dist == result.id_dist).first().long,
                          db_sess.query(SprStill).filter(SprStill.id_still == result.id_still).first().still,
                          result.result, db_sess.query(Competition).filter(
                Competition.id_competition == result.id_competition_r).first().competition,
                          db_sess.query(Competition).filter(
                              Competition.id_competition == result.id_competition_r).first().data])
    info_student = [student.name + ' ' + student.surname, str(student_birth), coach.surname + ' ' + coach.name,
                    group.name_group, result_st]
    print(info_student)  # ['Имя и Фам студента', str(дата рождение) 'Имя и Фам тр', 'Имя_Гру',
    # [[длина заплыва, назв стиля, время заплыва, имя соревнований, дата соревнований], и т.п]]

    return render_template('profile_student.html', info_student=info_student)


@app.route('/profile/<id>')
def profile_student(id):
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id_student == id).first()
    group = db_sess.query(Group).filter(Group.id_group == student.id_group).first()
    coach = db_sess.query(Coach).filter(Coach.id_coach == group.id_couch).first()
    today = date.today()
    birth_date = student.data_of_birth
    student_birth = today.year - birth_date.year
    if today.month < birth_date.month or today.month == birth_date.month and today.day < birth_date.day:
        student_birth -= 1
    result_st = []
    for result in db_sess.query(Result).filter(Result.id_student == student.id_student).all():
        result_st.append([db_sess.query(SprDist).filter(SprDist.id_spr_dist == result.id_dist).first().long,
                          db_sess.query(SprStill).filter(SprStill.id_still == result.id_still).first().still,
                          result.result, db_sess.query(Competition).filter(
                Competition.id_competition == result.id_competition_r).first().competition,
                          db_sess.query(Competition).filter(
                              Competition.id_competition == result.id_competition_r).first().data])
    info_student = [student.name + ' ' + student.surname, str(student_birth), coach.surname + ' ' + coach.name,
                    group.name_group, result_st]
    print(info_student)  # ['Имя и Фам студента', str(дата рождение) 'Имя и Фам тр', 'Имя_Гру',
    # [[длина заплыва, назв стиля, время заплыва, имя соревнований, дата соревнований], и т.п]]

    return render_template('profile_student.html', info_student=info_student)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
