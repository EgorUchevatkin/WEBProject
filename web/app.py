from flask import Flask, render_template, redirect, request, url_for
from web.data import db_session
from web.data.db_class import Student

app = Flask(__name__)
db_session.global_init("db/web_db.db")


@app.route('/')
def index():
    return render_template('profile_student.html')


@app.route('/profile')
def profile_student():
    return render_template('profile_student.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
