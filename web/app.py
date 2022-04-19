from flask import Flask, render_template, redirect, request
from data import db_session
from data.__all_models import *


@app.route('/')
def index():
    db_sess = db_session.create_session()
    student = db_sess.query(Student).all()
    student = student[::-1]


