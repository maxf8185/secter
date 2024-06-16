from flask import render_template, redirect, url_for, request
import sqlalchemy as sa
from flask_login import logout_user, current_user, login_required, login_user

from app import app, db
from .models import Tour, User


@app.route('/')
def index():
    tours = db.session.scalars(sa.select(Tour)).all()
    return render_template('index.html', tours=tours)