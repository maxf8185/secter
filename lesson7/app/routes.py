from flask import render_template, request, redirect, url_for
import sqlalchemy as sa
from flask_login import login_user, logout_user, current_user, login_required

from app import app, db
from app.models import User


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return '<h1>log out please</h1>'
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.session.scalar(sa.select(User).where(User.username == username))
        if not user or not user.check_password(password):
            return '<h1>User not valid</h1>'
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return '<h1>logged out</h1>'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return '<h1>log out please</h1>'
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('login')
    return render_template('signup.html')