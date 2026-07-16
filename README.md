# Learning Platform — SQLAlchemy ORM Homework

Backend data layer for a small online learning platform built with
**Python**, **SQLAlchemy ORM**, and **SQLite**.

The project demonstrates data modeling, all required relationship types,
CRUD operations, relationship-based queries, realistic seed data, data
validation, uniqueness constraints, `get_or_create`, and a JOIN report.

## Domain

The system represents an online learning platform:

- users can be students or instructors;
- every user has one profile;
- an instructor can teach several courses;
- students can enroll in several courses;
- every course can contain several students.

## Models

### `User`

Fields:

- `id`
- `username` — unique
- `email` — unique
- `full_name`
- `role` — `student` or `instructor`

### `Profile`

Fields:

- `id`
- `user_id` — unique foreign key
- `bio`
- `city`
- `website`

### `Course`

Fields:

- `id`
- `code` — unique
- `title`
- `description`
- `instructor_id`

### `enrollments`

Intermediate association table used for the many-to-many relationship
between students and courses.

## Relationships

### One-to-One: `User` ↔ `Profile`

`profiles.user_id` is both a foreign key and unique. Therefore, one user
cannot have more than one profile, and one profile belongs to one user.

### One-to-Many: `User` → `Course`

A user with the instructor role can teach many courses. Every course has
one instructor through `courses.instructor_id`.

### Many-to-Many: `User` ↔ `Course`

Students and courses are connected through the `enrollments` association
table. One student can enroll in multiple courses, and one course can have
multiple students.

## Project structure

```text
sqlalchemy-learning-platform/
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── queries.py
│   ├── seed.py
│   └── validation.py
├── demo.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Implemented requirements

### Data modeling

- one-to-one relationship;
- one-to-many relationship;
- many-to-many relationship with a real intermediate table;
- meaningful table and field names.

### CRUD

The main entity is `User`.

- Create: `create_user`
- Read by ID: `get_user_by_id`
- Read by email: `get_user_by_email`
- Update: `update_user`
- Delete: `delete_user`

### Queries

- find a user by ID;
- find a user by email;
- get all courses taught by an instructor;
- get all students enrolled in a course;
- get all courses of a student;
- filter students through course title;
- filter users through profile city;
- generate an enrollment report using JOIN and GROUP BY.

### Data

The demonstration inserts:

- 5 users;
- 5 profiles;
- 3 courses;
- 6 enrollment links.

The records use realistic names, emails, cities, biographies and course
descriptions.

### Bonus features

- `get_or_create`;
- unique usernames, emails, course codes and profile user IDs;
- validation of usernames, emails, names, roles and course data;
- optional SQL logging;
- complex JOIN query with an enrollment count;
- duplicate enrollment prevention;
- SQLite foreign-key enforcement.

## Installation

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python demo.py
```

The script automatically:

1. recreates the SQLite database;
2. inserts realistic data;
3. demonstrates Create, Read, Update and Delete;
4. executes all required relationship queries;
5. demonstrates the bonus features.

The SQLite file `learning_platform.db` is created automatically and is
excluded from Git.

## Enable SQL query logging

### Windows PowerShell

```powershell
$env:SQL_ECHO="1"
python demo.py
```

### macOS/Linux

```bash
SQL_ECHO=1 python demo.py
```

## Submission

The assignment accepts only a public GitHub repository link.

Example:

```text
https://github.com/YOUR_USERNAME/sqlalchemy-learning-platform
```
