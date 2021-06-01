from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session, Response
from werkzeug.security import generate_password_hash, check_password_hash
import DB
import datetime
import os
import jwt
from functools import wraps

auth = Blueprint('auth', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if session.get('Auth-token'):
            token = session['Auth-token']
        if not token:
            return redirect(url_for('auth.login'))
        try:
            data = jwt.decode(token, os.getenv('JWT_SECRET'), 'HS256')
            username = data['username']
        except Exception as e:
            print(e)
            return redirect(url_for('auth.login'))

        return f(username, *args, **kwargs)
    return decorated


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    session.pop('Auth-token', None)
    nickname = request.form.get('nickname')
    password = request.form.get('password')

    user = DB.check_if_user_exist(nickname)

    if not user or not check_password_hash(user[0], password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page
    token = jwt.encode({'username': nickname,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=int(os.getenv('JWT_EXP', 30)))},
                        os.getenv('JWT_SECRET', 'shaylevin'), 'HS256')
    response = redirect(url_for('main.profile'))
    session['Auth-token'] = token
    return response


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    nickname = request.form.get('nickname')
    name = request.form.get('name')
    password = request.form.get('password')
    user = DB.check_if_user_exist(nickname)
    if user:
        flash('nickname already exists')
        return redirect(url_for('auth.signup'))

    DB.insert_new_user(name, nickname, generate_password_hash(password, method='sha256'))
    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    session.pop('Auth-token', None)
    return redirect(url_for('auth.login'))