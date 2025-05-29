from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# class User(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
#     password: Mapped[str] = mapped_column(nullable=False)
#     is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }

"""
    Esta es una relación de uno a uno 
"""

class Parent(db.Model):
    __tablename__ = "parent"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)

    # la relación con el hijo (para poder raer cosas del hijo)
    children: Mapped["Child"] = relationship(back_populates="parent")


class Child(db.Model):
    __tablename__ = "child"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[String] = mapped_column(String(80), nullable=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))

    # la relación con el padre (para poder raer cosas del padre)
    parents: Mapped["Parent"] = relationship(back_populates="children")
