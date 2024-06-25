from flask import render_template, redirect, url_for, request
import sqlalchemy as sa
from flask_login import logout_user, current_user, login_required, login_user
from .forms import RegistrationForm
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
        return redirect(url_for('home'))
    return render_template('register.html', form=form)