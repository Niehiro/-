from __future__ import annotations

import re

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

ALLOWED_ROLES = {"student", "instructor"}


def validate_username(username: str) -> str:
    username = username.strip()

    if len(username) < 3:
        raise ValueError("Username must contain at least 3 characters.")

    if " " in username:
        raise ValueError("Username cannot contain spaces.")

    return username


def validate_email(email: str) -> str:
    email = email.strip().lower()

    if not EMAIL_PATTERN.fullmatch(email):
        raise ValueError(f"Invalid email address: {email}")

    return email


def validate_full_name(full_name: str) -> str:
    full_name = " ".join(full_name.split())

    if len(full_name) < 3:
        raise ValueError("Full name is too short.")

    return full_name


def validate_role(role: str) -> str:
    role = role.strip().lower()

    if role not in ALLOWED_ROLES:
        allowed = ", ".join(sorted(ALLOWED_ROLES))
        raise ValueError(f"Role must be one of: {allowed}")

    return role


def validate_course_code(code: str) -> str:
    code = code.strip().upper()

    if len(code) < 3:
        raise ValueError("Course code must contain at least 3 characters.")

    return code


def validate_course_title(title: str) -> str:
    title = " ".join(title.split())

    if len(title) < 3:
        raise ValueError("Course title is too short.")

    return title
