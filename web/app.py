from flask import Flask, render_template, redirect, request, url_for
from web.data import db_session
from flask import Flask, render_template, redirect, request
from web.data.db_class import Student, Coach, Group, Result, SprStill, SprDist, Competition
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import date
from web.form.form import LoginForm
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/web_db.db")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    db_sess = db_session.create_session()
    return db_sess.query(Coach).get(id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def home_group():
    return render_template("group.html")


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Coach).filter(Coach.email_couch == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/sing-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        name = request.form.get('Name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        db_sess = db_session.create_session()
        if password2 != password1:
            return render_template("sign_up.html", user=current_user, incorrect='Пароли не совподают')
        elif db_sess.query(Coach).filter(Coach.email_couch == email).first():
            return render_template("sign_up.html", user=current_user, incorrect='Почта уже есть в базе данных')
        else:
            new_coach = Coach()
            new_coach.id_coach = None
            new_coach.name = name
            new_coach.surname = first_name
            new_coach.set_password(password1)
            new_coach.email_couch = email
            db_sess = db_session.create_session()
            db_sess.add(new_coach)
            db_sess.commit()
            login_user(new_coach, remember=True)
            return redirect('/')

    return render_template("sign_up.html", user=current_user, incorrect='')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
