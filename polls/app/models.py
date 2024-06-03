from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional


class Category(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    name: so.MappedColumn[str] = so.mapped_column(sa.String(100))
    description: so.MappedColumn[str] = so.mapped_column(sa.String(100))
    polls: so.WriteOnlyMapped['Poll'] = so.relationship(back_populates='category')

    def __repr__(self):
        return f'Category: {self.name}'

class Poll(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    topic: so.MappedColumn[str] = so.mapped_column(sa.String(100))
    options: so.WriteOnlyMapped['Option'] = so.relationship(back_populates='poll')
    category_id: so.MappedColumn[int] = so.mapped_column(sa.ForeignKey(Category.id))
    category: so.Mapped[Category] = so.relationship(back_populates='polls')

    def __repr__(self):
        return f'Poll: {self.topic}'


class Option(db.Model):
    id: so.MappedColumn[int] = so.mapped_column(primary_key=True)
    title: so.MappedColumn[str] = so.mapped_column(sa.String(100))
    votes: so.MappedColumn[int]
    poll_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Poll.id))
    poll: so.Mapped[Poll] = so.relationship(back_populates='options')

    def __repr__(self):
        return f'Option: {self.title}'