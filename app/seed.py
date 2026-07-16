from __future__ import annotations

from sqlalchemy.orm import Session

from app.crud import create_course, create_user, enroll_student
from app.models import Course, User


def seed_database(
    session: Session,
) -> dict[str, User | Course]:
    """Insert realistic data that demonstrates every relationship."""

    amina = create_user(
        session,
        username="amina.sadykova",
        email="amina.sadykova@academy.edu",
        full_name="Amina Sadykova",
        role="instructor",
        bio="Database lecturer and backend developer.",
        city="Bishkek",
        website="https://academy.example/amina",
    )

    timur = create_user(
        session,
        username="timur.bekov",
        email="timur.bekov@academy.edu",
        full_name="Timur Bekov",
        role="instructor",
        bio="Python engineer focused on web services.",
        city="Almaty",
        website="https://academy.example/timur",
    )

    aidar = create_user(
        session,
        username="aidar.niyazov",
        email="aidar.niyazov@student.edu",
        full_name="Aidar Niyazov",
        role="student",
        bio="Student interested in backend development.",
        city="Bishkek",
    )

    dana = create_user(
        session,
        username="dana.karimova",
        email="dana.karimova@student.edu",
        full_name="Dana Karimova",
        role="student",
        bio="Student learning databases and analytics.",
        city="Astana",
    )

    emil = create_user(
        session,
        username="emil.tursunov",
        email="emil.tursunov@student.edu",
        full_name="Emil Tursunov",
        role="student",
        bio="Student practicing Python and OOP.",
        city="Bishkek",
    )

    database_course = create_course(
        session,
        code="DB101",
        title="Database Systems",
        description="Relational modeling, SQL and database design.",
        instructor=amina,
    )

    oop_course = create_course(
        session,
        code="OOP110",
        title="Object-Oriented Programming",
        description="Classes, inheritance, polymorphism and clean design.",
        instructor=amina,
    )

    python_course = create_course(
        session,
        code="PY201",
        title="Python Backend Development",
        description="Python services, ORM and backend architecture.",
        instructor=timur,
    )

    enroll_student(
        session,
        student=aidar,
        course=database_course,
    )
    enroll_student(
        session,
        student=aidar,
        course=python_course,
    )
    enroll_student(
        session,
        student=dana,
        course=database_course,
    )
    enroll_student(
        session,
        student=dana,
        course=oop_course,
    )
    enroll_student(
        session,
        student=emil,
        course=oop_course,
    )
    enroll_student(
        session,
        student=emil,
        course=python_course,
    )

    return {
        "amina": amina,
        "timur": timur,
        "aidar": aidar,
        "dana": dana,
        "emil": emil,
        "database_course": database_course,
        "oop_course": oop_course,
        "python_course": python_course,
    }
