from __future__ import annotations

from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models import Course, Profile, User
from app.validation import (
    validate_course_code,
    validate_course_title,
    validate_email,
    validate_full_name,
    validate_role,
    validate_username,
)


# ---------------------------
# USER CRUD
# ---------------------------

def create_user(
    session: Session,
    *,
    username: str,
    email: str,
    full_name: str,
    role: str,
    bio: str,
    city: str,
    website: str | None = None,
) -> User:
    """CREATE a user together with a one-to-one profile."""
    username = validate_username(username)
    email = validate_email(email)
    full_name = validate_full_name(full_name)
    role = validate_role(role)

    duplicate = session.scalar(
        select(User).where(
            or_(
                User.username == username,
                User.email == email,
            )
        )
    )
    if duplicate is not None:
        raise ValueError("A user with this username or email already exists.")

    user = User(
        username=username,
        email=email,
        full_name=full_name,
        role=role,
    )
    user.profile = Profile(
        bio=bio.strip(),
        city=city.strip(),
        website=website.strip() if website else None,
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_id(session: Session, user_id: int) -> User | None:
    """READ a user by primary key."""
    return session.get(User, user_id)


def get_user_by_email(session: Session, email: str) -> User | None:
    """READ a user by a non-ID field."""
    email = validate_email(email)
    return session.scalar(select(User).where(User.email == email))


def get_user_by_username(session: Session, username: str) -> User | None:
    """READ a user by username."""
    username = validate_username(username)
    return session.scalar(select(User).where(User.username == username))


def update_user(
    session: Session,
    user_id: int,
    **changes: Any,
) -> User:
    """UPDATE allowed fields on a user."""
    user = get_user_by_id(session, user_id)
    if user is None:
        raise LookupError(f"User with id={user_id} was not found.")

    if "username" in changes:
        new_username = validate_username(str(changes["username"]))
        duplicate = session.scalar(
            select(User).where(
                User.username == new_username,
                User.id != user_id,
            )
        )
        if duplicate is not None:
            raise ValueError("This username is already in use.")
        user.username = new_username

    if "email" in changes:
        new_email = validate_email(str(changes["email"]))
        duplicate = session.scalar(
            select(User).where(
                User.email == new_email,
                User.id != user_id,
            )
        )
        if duplicate is not None:
            raise ValueError("This email is already in use.")
        user.email = new_email

    if "full_name" in changes:
        user.full_name = validate_full_name(str(changes["full_name"]))

    if "role" in changes:
        user.role = validate_role(str(changes["role"]))

    if user.profile is not None:
        if "bio" in changes:
            user.profile.bio = str(changes["bio"]).strip()
        if "city" in changes:
            user.profile.city = str(changes["city"]).strip()
        if "website" in changes:
            website = changes["website"]
            user.profile.website = (
                str(website).strip() if website else None
            )

    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    """DELETE a user. Cascades also remove the related profile."""
    user = get_user_by_id(session, user_id)
    if user is None:
        return False

    session.delete(user)
    session.commit()
    return True


def get_or_create_user(
    session: Session,
    *,
    username: str,
    email: str,
    full_name: str,
    role: str,
    bio: str,
    city: str,
    website: str | None = None,
) -> tuple[User, bool]:
    """Bonus: return an existing user or create a new one."""
    existing = get_user_by_email(session, email)
    if existing is not None:
        return existing, False

    user = create_user(
        session,
        username=username,
        email=email,
        full_name=full_name,
        role=role,
        bio=bio,
        city=city,
        website=website,
    )
    return user, True


# ---------------------------
# COURSE OPERATIONS
# ---------------------------

def create_course(
    session: Session,
    *,
    code: str,
    title: str,
    description: str,
    instructor: User,
) -> Course:
    if instructor.role != "instructor":
        raise ValueError("Only a user with role='instructor' can teach.")

    code = validate_course_code(code)
    title = validate_course_title(title)

    duplicate = session.scalar(
        select(Course).where(Course.code == code)
    )
    if duplicate is not None:
        raise ValueError(f"Course code {code!r} already exists.")

    course = Course(
        code=code,
        title=title,
        description=description.strip(),
        instructor=instructor,
    )
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


def get_course_by_code(session: Session, code: str) -> Course | None:
    code = validate_course_code(code)
    return session.scalar(select(Course).where(Course.code == code))


def enroll_student(
    session: Session,
    *,
    student: User,
    course: Course,
) -> bool:
    """Add a many-to-many link without creating duplicates."""
    if student.role != "student":
        raise ValueError("Only users with role='student' can enroll.")

    if course in student.enrolled_courses:
        return False

    student.enrolled_courses.append(course)
    session.commit()
    return True
