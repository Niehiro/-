from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models import Course, Profile, User, enrollments


def get_courses_by_instructor(
    session: Session,
    instructor_id: int,
) -> list[Course]:
    """One-to-many query: all courses taught by one instructor."""
    statement = (
        select(Course)
        .where(Course.instructor_id == instructor_id)
        .order_by(Course.code)
    )
    return list(session.scalars(statement).all())


def get_students_for_course(
    session: Session,
    course_id: int,
) -> list[User]:
    """Many-to-many query: all students enrolled in one course."""
    statement = (
        select(User)
        .join(User.enrolled_courses)
        .where(Course.id == course_id)
        .order_by(User.full_name)
    )
    return list(session.scalars(statement).unique().all())


def get_courses_for_student(
    session: Session,
    student_id: int,
) -> list[Course]:
    """Get related courses for a specific student."""
    statement = (
        select(Course)
        .join(Course.students)
        .where(User.id == student_id)
        .order_by(Course.title)
    )
    return list(session.scalars(statement).unique().all())


def find_students_by_course_title(
    session: Session,
    title_text: str,
) -> list[User]:
    """Filter users through the many-to-many course relationship."""
    statement = (
        select(User)
        .join(User.enrolled_courses)
        .where(Course.title.ilike(f"%{title_text.strip()}%"))
        .order_by(User.full_name)
    )
    return list(session.scalars(statement).unique().all())


def find_users_by_city(
    session: Session,
    city: str,
) -> list[User]:
    """Filter users through the one-to-one Profile relationship."""
    statement = (
        select(User)
        .join(User.profile)
        .where(Profile.city.ilike(city.strip()))
        .options(selectinload(User.profile))
        .order_by(User.full_name)
    )
    return list(session.scalars(statement).all())


def course_enrollment_report(
    session: Session,
) -> list[tuple[str, str, int]]:
    """Bonus JOIN query: course, instructor and enrollment count."""
    statement = (
        select(
            Course.code,
            User.full_name.label("instructor_name"),
            func.count(enrollments.c.student_id).label("student_count"),
        )
        .join(User, User.id == Course.instructor_id)
        .outerjoin(
            enrollments,
            enrollments.c.course_id == Course.id,
        )
        .group_by(Course.id, Course.code, User.full_name)
        .order_by(
            func.count(enrollments.c.student_id).desc(),
            Course.code,
        )
    )
    return [
        (row.code, row.instructor_name, row.student_count)
        for row in session.execute(statement)
    ]
