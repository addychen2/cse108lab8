# Student Enrollment Web App

This is a Flask application for managing student enrollment at ACME University, created as per the Lab 8 specifications.

## Features

### Student Role
- Log in/out of application
- View enrolled classes
- Browse all classes offered by the university
- See enrollment numbers for each class
- Register for new classes (if capacity hasn't been reached)

### Teacher Role
- Log in/out of application
- View classes they teach
- See all students enrolled in each class and their grades
- Edit grades for students

### Admin Role
- Create, read, update, delete all data in the database
- Access admin panel powered by Flask-Admin

## Installation

1. Make sure you have Python 3.7+ installed

2. Clone this repository or download the files

3. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

4. Install the required packages:
   ```
   pip install Flask Flask-SQLAlchemy Flask-Login Flask-Admin
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Open your browser and go to: http://127.0.0.1:5000/

## Default Users

The application is pre-populated with the following users:

### Admin
- Username: admin
- Password: password

### Teachers
- Username: liz
- Password: password
- Name: Dr Ramos

- Username: addy
- Password: password
- Name: Dr Ramos

- Username: luis
- Password: password
- Name: Dr Garibay

### Students
- Username: javi
- Password: password
- Name: Dr Javier Gomez y Llagaria

- Username: evan
- Password: password
- Name: Even A

- Username: daniel
- Password: password
- Name: Daniel Nestares

- Username: TJkeny
- Password: password
- Name: TJ Keny

- Username: bighead
- Password: password
- Name: Ryan Most

- Username: jcm
- Password: password
- Name: Julio Casal Monserrat
