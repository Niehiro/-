from __future__ import annotations

from app.crud import (
    create_user,
    delete_user,
    get_or_create_user,
    get_user_by_email,
    get_user_by_id,
    update_user,
)
from app.database import SessionLocal, reset_database
from app.queries import (
    course_enrollment_report,
    find_students_by_course_title,
    find_users_by_city,
    get_courses_by_instructor,
    get_courses_for_student,
    get_students_for_course,
)
from app.seed import seed_database


def heading(text: str) -> None:
    print("\n" + "=" * 72)
    print(text)
    print("=" * 72)


def main() -> None:
    # Part 5: create a fresh database automatically.
    reset_database()

    with SessionLocal() as session:
        data = seed_database(session)

        heading("DATABASE CREATED AND REALISTIC DATA INSERTED")
        print("Users and profiles: 5")
        print("Courses: 3")
        print("Enrollment links: 6")

        # ---------------------------
        # CRUD DEMONSTRATION
        # ---------------------------
        heading("CRUD FOR THE MAIN ENTITY: USER")

        created_user = create_user(
            session,
            username="nurai.kasymova",
            email="nurai.kasymova@student.edu",
            full_name="Nurai Kasymova",
            role="student",
            bio="Student exploring software engineering.",
            city="Osh",
        )
        print("CREATE:", created_user)

        user_by_id = get_user_by_id(session, created_user.id)
        print("READ BY ID:", user_by_id)

        user_by_email = get_user_by_email(
            session,
            "nurai.kasymova@student.edu",
        )
        print("READ BY EMAIL:", user_by_email)

        updated_user = update_user(
            session,
            created_user.id,
            full_name="Nurai A. Kasymova",
            city="Bishkek",
            website="https://portfolio.example/nurai",
        )
        print("UPDATE:", updated_user)
        print("UPDATED PROFILE:", updated_user.profile)

        deleted = delete_user(session, created_user.id)
        print("DELETE:", deleted)
        print(
            "READ AFTER DELETE:",
            get_user_by_id(session, created_user.id),
        )

        # ---------------------------
        # REQUIRED RELATION QUERIES
        # ---------------------------
        heading("QUERY: ALL COURSES OF ONE INSTRUCTOR (1:N)")
        for course in get_courses_by_instructor(
            session,
            data["amina"].id,
        ):
            print(course)

        heading("QUERY: ALL STUDENTS OF ONE COURSE (N:N)")
        for student in get_students_for_course(
            session,
            data["database_course"].id,
        ):
            print(student)

        heading("QUERY: ALL COURSES OF ONE STUDENT (N:N)")
        for course in get_courses_for_student(
            session,
            data["aidar"].id,
        ):
            print(course)

        heading("FILTER THROUGH RELATIONSHIP: COURSE TITLE")
        for student in find_students_by_course_title(
            session,
            "Python Backend",
        ):
            print(student)

        heading("FILTER THROUGH ONE-TO-ONE PROFILE: CITY")
        for user in find_users_by_city(session, "Bishkek"):
            print(user, "->", user.profile)

        # ---------------------------
        # BONUS FEATURES
        # ---------------------------
        heading("BONUS: GET OR CREATE")
        existing, created = get_or_create_user(
            session,
            username="aidar.niyazov",
            email="aidar.niyazov@student.edu",
            full_name="Aidar Niyazov",
            role="student",
            bio="This data is not inserted again.",
            city="Bishkek",
        )
        print("RESULT:", existing)
        print("WAS CREATED:", created)

        heading("BONUS: COMPLEX JOIN AND GROUPING")
        for code, instructor_name, student_count in (
            course_enrollment_report(session)
        ):
            print(
                f"{code}: instructor={instructor_name}, "
                f"students={student_count}"
            )

        heading("DEMONSTRATION FINISHED SUCCESSFULLY")


if __name__ == "__main__":
    main()
