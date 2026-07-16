PS C:\Users\aidar\Downloads\задача> python -m venv .venv
PS C:\Users\aidar\Downloads\задача> .\.venv\Scripts\Activate.ps1
(.venv) PS C:\Users\aidar\Downloads\задача> python -m pip install -r requirements.txt
Collecting SQLAlchemy==2.0.36 (from -r requirements.txt (line 1))
  Using cached SQLAlchemy-2.0.36-cp313-cp313-win_amd64.whl.metadata (9.9 kB)
Collecting typing-extensions>=4.6.0 (from SQLAlchemy==2.0.36->-r requirements.txt (line 1))
  Using cached typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
Using cached SQLAlchemy-2.0.36-cp313-cp313-win_amd64.whl (2.1 MB)
Using cached typing_extensions-4.16.0-py3-none-any.whl (45 kB)
Installing collected packages: typing-extensions, SQLAlchemy
Successfully installed SQLAlchemy-2.0.36 typing-extensions-4.16.0
(.venv) PS C:\Users\aidar\Downloads\задача> python demo.py

========================================================================
DATABASE CREATED AND REALISTIC DATA INSERTED
========================================================================
Users and profiles: 5
Courses: 3
Enrollment links: 6

========================================================================
CRUD FOR THE MAIN ENTITY: USER
========================================================================
CREATE: User(id=6, username='nurai.kasymova', email='nurai.kasymova@student.edu', full_name='Nurai Kasymova', role='student')
READ BY ID: User(id=6, username='nurai.kasymova', email='nurai.kasymova@student.edu', full_name='Nurai Kasymova', role='student')
READ BY EMAIL: User(id=6, username='nurai.kasymova', email='nurai.kasymova@student.edu', full_name='Nurai Kasymova', role='student')
UPDATE: User(id=6, username='nurai.kasymova', email='nurai.kasymova@student.edu', full_name='Nurai A. Kasymova', role='student')
UPDATED PROFILE: Profile(id=6, user_id=6, city='Bishkek', website='https://portfolio.example/nurai')
DELETE: True
READ AFTER DELETE: None

========================================================================
QUERY: ALL COURSES OF ONE INSTRUCTOR (1:N)
========================================================================
Course(id=1, code='DB101', title='Database Systems', instructor_id=1)
Course(id=2, code='OOP110', title='Object-Oriented Programming', instructor_id=1)

========================================================================
QUERY: ALL STUDENTS OF ONE COURSE (N:N)
========================================================================
User(id=3, username='aidar.niyazov', email='aidar.niyazov@student.edu', full_name='Aidar Niyazov', role='student')
User(id=4, username='dana.karimova', email='dana.karimova@student.edu', full_name='Dana Karimova', role='student')

========================================================================
QUERY: ALL COURSES OF ONE STUDENT (N:N)
========================================================================
Course(id=1, code='DB101', title='Database Systems', instructor_id=1)
Course(id=3, code='PY201', title='Python Backend Development', instructor_id=2)

========================================================================
FILTER THROUGH RELATIONSHIP: COURSE TITLE
========================================================================
User(id=3, username='aidar.niyazov', email='aidar.niyazov@student.edu', full_name='Aidar Niyazov', role='student')
User(id=5, username='emil.tursunov', email='emil.tursunov@student.edu', full_name='Emil Tursunov', role='student')

========================================================================
FILTER THROUGH ONE-TO-ONE PROFILE: CITY
========================================================================
User(id=3, username='aidar.niyazov', email='aidar.niyazov@student.edu', full_name='Aidar Niyazov', role='student') -> Profile(id=3, user_id=3, city='Bishkek', website=None)
User(id=1, username='amina.sadykova', email='amina.sadykova@academy.edu', full_name='Amina Sadykova', role='instructor') -> Profile(id=1, user_id=1, city='Bishkek', website='https://academy.example/amina')
User(id=5, username='emil.tursunov', email='emil.tursunov@student.edu', full_name='Emil Tursunov', role='student') -> Profile(id=5, user_id=5, city='Bishkek', website=None)

========================================================================
BONUS: GET OR CREATE
========================================================================
RESULT: User(id=3, username='aidar.niyazov', email='aidar.niyazov@student.edu', full_name='Aidar Niyazov', role='student')
WAS CREATED: False

========================================================================
BONUS: COMPLEX JOIN AND GROUPING
========================================================================
DB101: instructor=Amina Sadykova, students=2
OOP110: instructor=Amina Sadykova, students=2
PY201: instructor=Timur Bekov, students=2

========================================================================
DEMONSTRATION FINISHED SUCCESSFULLY
========================================================================
