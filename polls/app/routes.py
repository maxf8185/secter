from flask import render_template, redirect, url_for
import sqlalchemy as sa

from app import app, db
from app.models import Poll, Option, Category


@app.route('/')
def index():
    polls = db.session.scalars(sa.select(Poll)).all()
    categories = db.session.scalars(sa.select(Category)).all()
    return render_template('index.html', polls=polls, categories=categories)


@app.route('/poll/<int:poll_id>')
def poll(poll_id):
    poll = db.session.scalar(sa.select(Poll).where(Poll.id == poll_id))
    options = db.session.scalars(poll.options.select()).all()
    return render_template('poll.html', poll=poll, options=options)


@app.route('/option/<int:poll_id>/<int:option_id>')
def option(poll_id, option_id):
    option = db.session.scalar(sa.select(Option).where(Option.id == option_id))
    option.votes += 1
    db.session.add(option)
    db.session.commit()
    return redirect(url_for('poll', poll_id=poll_id))


@app.route('/category/<int:category_id>')
def category(category_id):
    category = db.session.scalar(sa.select(Category).where(Category.id == category_id))
    polls = db.session.scalars(category.polls.select()).all()
    return render_template('category.html', polls=polls)