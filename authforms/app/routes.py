from flask import render_template, redirect, url_for, request
import sqlalchemy as sa
from flask_login import logout_user, current_user, login_required, login_user
from .forms import RegistrationForm, LoginForm
from app import app, db
from app.models import User


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))  # Перенаправлення на сторінку входу після реєстрації
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/posts')
def posts():
    return render_template('posts.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))  # Можна додати повідомлення про помилку
        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html', form=form)
