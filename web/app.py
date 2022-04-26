from flask import Flask, render_template, redirect, request, url_for
from web.data import db_session
from flask import Flask, render_template, redirect, request
from web.data.db_class import Student, Coach, Group, Result, SprStill, SprDist, Competition
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import date
from web.form.form import LoginForm
import requests
import datetime

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
    print(current_user.id_coach)
    return render_template("group.html", user=current_user)


@app.route('/profile/<id>')
@login_required
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
        result_st.append('   '.join([db_sess.query(SprDist).filter(SprDist.id_spr_dist == result.id_dist).first().long,
                                     db_sess.query(SprStill).filter(SprStill.id_still == result.id_still).first().still,
                                     result.result, db_sess.query(Competition).filter(
                Competition.id_competition == result.id_competition_r).first().competition,
                                     db_sess.query(Competition).filter(
                                         Competition.id_competition == result.id_competition_r).first().data]))
    if len(result_st) < 1:
        result_st = ['Достижений нет']
        px = -13
    else:
        px = (len(result_st) - 1) * -40 - 10
    info_student = [student.name + ' ' + student.surname, str(student_birth), coach.surname + ' ' + coach.name,
                    group.name_group, result_st, px, id]
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
    return render_template('login.html', title='Авторизация', form=form, user=current_user)


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
            return render_template("sign_up.html", incorrect='Пароли не совподают')
        elif db_sess.query(Coach).filter(Coach.email_couch == email).first():
            return render_template("sign_up.html", incorrect='Почта уже есть в базе данных')
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


@app.route('/add-result/<id>', methods=['GET', 'POST'])
@login_required
def add_result(id):
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id_student == id).first()
    group = db_sess.query(Group).filter(Group.id_group == student.id_group).first()
    coach = db_sess.query(Coach).filter(Coach.id_coach == group.id_couch).first()
    today = date.today()
    birth_date = student.data_of_birth
    student_birth = today.year - birth_date.year
    info_student = [student.name + ' ' + student.surname, str(student_birth), coach.surname + ' ' + coach.name,
                    group.name_group, id]
    competition_list = []
    for i in db_sess.query(Competition).all():
        competition_list.append(i.competition)
    if today.month < birth_date.month or today.month == birth_date.month and today.day < birth_date.day:
        student_birth -= 1
    if request.method == 'POST':
        dist_long = request.form.get('dist_long')
        dist_still = request.form.get('dist_still')
        competition1 = request.form.get('competition')
        time = request.form.get('time')
        print(time)
        if not time:
            return render_template('new_resultt.html', incorrect='Укажате время', info_student=info_student,
                                   competition_list=competition_list, user=current_user)
        elif len(time.split(':')) != 3 or len(time.split(':')[0]) != 2 or len(time.split(':')[1]) != 2 or len(
                time.split(':')[2]) != 2:
            return render_template('new_resultt.html', incorrect='Время указоно не верно', info_student=info_student,
                                   competition_list=competition_list, user=current_user)
        else:
            db_sess = db_session.create_session()
            result = Result()
            result.id_result = None
            result.id_still = db_sess.query(SprStill).filter(SprStill.still == dist_still).first().id_still
            result.id_dist = db_sess.query(SprDist).filter(SprDist.long == dist_long.split()[0]).first().id_spr_dist
            result.id_student = id
            result.result = '-'.join(time.split(':'))
            result.id_competition_r = db_sess.query(Competition).filter(
                Competition.competition == competition1).first().id_competition
            db_sess = db_session.create_session()
            db_sess.add(result)
            db_sess.commit()
            return redirect(url_for('profile_student', id=id))

    return render_template('new_resultt.html', incorrect='', info_student=info_student,
                           competition_list=competition_list, user=current_user)


@app.route('/add-competition', methods=['GET', 'POST'])
@login_required
def add_competition():
    print(request.method)
    if request.method == 'POST':
        data_c = request.form.get('data')
        print([data_c])
        name_c = request.form.get('name_competition')
        print(name_c)
        if len(data_c.split('-')) != 3 or len(data_c.split('-')[0]) != 4 or len(data_c.split('-')[1]) != 2 or len(
                data_c.split('-')[2]) != 2:
            print(data_c.split('-'), data_c)
            return render_template('new_competition.html', incorrect='Неверно указана дата', user=current_user)
        elif not name_c:
            return render_template('new_competition.html', incorrect='Неуказано имя соревнований', user=current_user)
        else:
            coach = Competition()
            coach.id_competition = None
            coach.data = data_c
            coach.competition = name_c
            db_sess = db_session.create_session()
            db_sess.add(coach)
            db_sess.commit()
            return redirect(url_for('home_group'))
    return render_template('new_competition.html', incorrect='', user=current_user)


@app.route('/competition')
@login_required
def competition():
    info = []
    db_sess = db_session.create_session()
    competition_list = db_sess.query(Competition)
    competition_list = competition_list.order_by(Competition.data)
    for i in competition_list:
        info.append([i.competition, i.data])
    info = reversed(info)
    return render_template('competition.html', info=info)


@app.route('/add-group', methods=['GET', 'POST'])
@login_required
def add_group():
    name_ch_lst = []
    db_sess = db_session.create_session()
    ch_list = db_sess.query(Coach).all()
    for i in ch_list:
        name_ch_lst.append(i.name + ' ' + i.surname + ' ' + str(i.id_coach))
    if request.method == 'POST':
        name_coach = request.form.get('name_ch')
        name_group = request.form.get('name_group')
        print(name_coach, name_group)
        if not name_group:
            return render_template('new_group.html', incorrect='Неуказано имя группы', name_ch_lst=name_ch_lst, user=current_user)
        else:
            group = Group()
            group.id_group = None
            group.name_group = name_group
            group.id_couch = int(name_coach.split(' ')[-1])
            db_sess = db_session.create_session()
            db_sess.add(group)
            db_sess.commit()
            return redirect(url_for('home_group'))
    return render_template('new_group.html', incorrect='', name_ch_lst=name_ch_lst, user=current_user)


@app.route('/add-student', methods=['GET', 'POST'])
@login_required
def add_student():
    id_coach = 1  # id_coach долже ровняться id пользователя который зашел в систему я незнаю как это сделать
    name_group = []
    db_sess = db_session.create_session()
    gr_list = db_sess.query(Group).filter(Group.id_couch == id_coach).all()
    for i in gr_list:
        name_group.append(i.name_group + ' ' + str(i.id_group))
    if request.method == 'POST':
        surname_student = request.form.get('surname')
        name_student = request.form.get('name')
        data_student = request.form.get('data')
        name_gr = request.form.get('g')
        print(name_gr, surname_student, name_student, data_student)
        pol_st = request.form.get('pol')
        print(pol_st)
        if len(data_student.split('-')) != 3 or len(data_student.split('-')[0]) != 4 or len(
                data_student.split('-')[1]) != 2 or len(data_student.split('-')[2]) != 2:
            return render_template('new_student.html', incorrect='Неверно указана дата', name_group=name_group, user=current_user)
        elif not surname_student or not name_student or not data_student:
            return render_template('new_student.html', incorrect='Неуказано одно из полей', name_group=name_group, user=current_user)
        else:
            student = Student()
            student.id_student = None
            student.id_group = name_gr.split()[-1]
            student.name = name_student
            student.surname = surname_student
            student.data_of_birth = datetime.date(int(data_student.split('-')[0]), int(data_student.split('-')[1]),
                                                  int(data_student.split('-')[2]))
            if pol_st == 'м':
                student.gender = 1
            else:
                student.gender = 0
            db_sess = db_session.create_session()
            db_sess.add(student)
            db_sess.commit()
            return redirect(url_for('home_group'))
    return render_template('new_student.html', incorrect='', name_group=name_group, user=current_user)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
