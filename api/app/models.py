from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime


class Category(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    description: so.Mapped[str] = so.mapped_column(sa.Text)
    posts: so.Mapped['Post'] = so.relationship(back_populates='category')

    def __repr__(self):
        return self.name


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(100))
    content: so.Mapped[str] = so.mapped_column(sa.Text)
    time: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now())
    category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Category.id), index=True)
    category: so.Mapped[Category] = so.relationship(back_populates='posts')

    def __repr__(self):
        return self.title


