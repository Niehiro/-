from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""


# Many-to-many association table:
# one student can enroll in many courses;
# one course can contain many students.
enrollments = Table(
    "enrollments",
    Base.metadata,
    Column(
        "student_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "course_id",
        ForeignKey("courses.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "enrolled_at",
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    ),
)


class User(Base):
    """A student or instructor registered in the platform."""

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
        UniqueConstraint("email", name="uq_users_email"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)

    # One-to-one: User <-> Profile.
    profile: Mapped[Optional["Profile"]] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,
    )

    # One-to-many: one instructor can teach many courses.
    taught_courses: Mapped[list["Course"]] = relationship(
        back_populates="instructor",
        cascade="all, delete-orphan",
        foreign_keys="Course.instructor_id",
    )

    # Many-to-many: students can enroll in many courses.
    enrolled_courses: Mapped[list["Course"]] = relationship(
        secondary=enrollments,
        back_populates="students",
    )

    def __repr__(self) -> str:
        return (
            "User("
            f"id={self.id}, "
            f"username={self.username!r}, "
            f"email={self.email!r}, "
            f"full_name={self.full_name!r}, "
            f"role={self.role!r}"
            ")"
        )


class Profile(Base):
    """Additional information belonging to exactly one user."""

    __tablename__ = "profiles"
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_profiles_user_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    bio: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    website: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    user: Mapped["User"] = relationship(back_populates="profile")

    def __repr__(self) -> str:
        return (
            "Profile("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"city={self.city!r}, "
            f"website={self.website!r}"
            ")"
        )


class Course(Base):
    """A course taught by one instructor and joined by many students."""

    __tablename__ = "courses"
    __table_args__ = (
        UniqueConstraint("code", name="uq_courses_code"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    instructor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    instructor: Mapped["User"] = relationship(
        back_populates="taught_courses",
        foreign_keys=[instructor_id],
    )

    students: Mapped[list["User"]] = relationship(
        secondary=enrollments,
        back_populates="enrolled_courses",
    )

    def __repr__(self) -> str:
        return (
            "Course("
            f"id={self.id}, "
            f"code={self.code!r}, "
            f"title={self.title!r}, "
            f"instructor_id={self.instructor_id}"
            ")"
        )
