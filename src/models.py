from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime, func, Text, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

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

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lo que quiera": self.email
        }


class Child(db.Model):
    __tablename__ = "child"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[String] = mapped_column(String(80), nullable=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))

    # la relación con el padre (para poder rae-->r cosas del padre)
    parent: Mapped["Parent"] = relationship(back_populates="children")


"""
    Este es el ejemplo de uno a muchos 
"""


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # relationshiop del ORM
    tareas: Mapped[List["Todos"]] = relationship(
        back_populates="usuarios_buenos")


class Todos(db.Model):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),  nullable=False)

    # relationshiop del ORM
    usuarios_buenos: Mapped["User"] = relationship(back_populates="tareas")


"""
    Este es el ejemplo de una relación muchos a muchos 
"""

association_table = Table(
    "association",
    db.metadata,
    Column("student_id", ForeignKey("student.id")),
    Column("course_id", ForeignKey("course.id"))
)


class Student(db.Model):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    couses: Mapped[List["Course"]] = relationship(
        "Course", secondary=association_table,
        back_populates="students")


class Course(db.Model):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)

    students: Mapped[List["Student"]] = relationship(
        "Student",
        secondary=association_table,
        back_populates="couses"
    )
