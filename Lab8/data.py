from werkzeug.security import generate_password_hash
from models import db, User, Course, Enrollment

def create_initial_data():
    db.create_all()
    
    if User.query.count() == 0:
        admin = User(
            username='admin', 
            password=generate_password_hash('password'), 
            role='admin',
            name='Admin User'
        )
        
        teacher1 = User(
            username='ahepworth', 
            password=generate_password_hash('password'), 
            role='teacher',
            name='Dr Hepworth'
        )
        
        teacher2 = User(
            username='swalker', 
            password=generate_password_hash('password'), 
            role='teacher',
            name='Susan Walker'
        )
        
        teacher3 = User(
            username='rjenkins', 
            password=generate_password_hash('password'), 
            role='teacher',
            name='Ralph Jenkins'
        )
        
        student1 = User(
            username='cnorris', 
            password=generate_password_hash('password'), 
            role='student',
            name='Chuck'
        )
        
        student2 = User(
            username='mwright', 
            password=generate_password_hash('password'), 
            role='student',
            name='Mindy'
        )
        
        student3 = User(
            username='aranganath', 
            password=generate_password_hash('password'), 
            role='student',
            name='Aditya Ranganath'
        )
        
        student4 = User(
            username='nlittle', 
            password=generate_password_hash('password'), 
            role='student',
            name='Nancy Little'
        )
        
        student5 = User(
            username='ywchen', 
            password=generate_password_hash('password'), 
            role='student',
            name='Yi Wen Chen'
        )
        
        student6 = User(
            username='jstuart', 
            password=generate_password_hash('password'), 
            role='student',
            name='John Stuart'
        )
        
        db.session.add_all([
            admin, teacher1, teacher2, teacher3, 
            student1, student2, student3, student4, student5, student6
        ])
        db.session.commit()
        
        course1 = Course(
            name='Physics 121', 
            teacher_id=teacher2.id, 
            time='TR 11:00-11:50 AM', 
            capacity=10
        )
        
        course2 = Course(
            name='CS 106', 
            teacher_id=teacher1.id, 
            time='MWF 2:00-2:50 PM', 
            capacity=10
        )
        
        course3 = Course(
            name='Math 101', 
            teacher_id=teacher3.id, 
            time='MWF 10:00-10:50 AM', 
            capacity=8
        )
        
        course4 = Course(
            name='CS 162', 
            teacher_id=teacher1.id, 
            time='TR 3:00-3:50 PM', 
            capacity=4
        )
        
        db.session.add_all([course1, course2, course3, course4])
        db.session.commit()
        
        enrollments = [
            Enrollment(student_id=student1.id, course_id=course1.id),
            Enrollment(student_id=student1.id, course_id=course2.id),
            
            Enrollment(student_id=student3.id, course_id=course4.id, grade=92),
            Enrollment(student_id=student4.id, course_id=course4.id, grade=78),
            Enrollment(student_id=student5.id, course_id=course4.id, grade=95),
            Enrollment(student_id=student6.id, course_id=course4.id, grade=76),
            
            Enrollment(student_id=student3.id, course_id=course1.id),
            Enrollment(student_id=student4.id, course_id=course1.id),
            Enrollment(student_id=student5.id, course_id=course1.id),
            Enrollment(student_id=student6.id, course_id=course1.id),
            
            Enrollment(student_id=student3.id, course_id=course2.id),
            Enrollment(student_id=student4.id, course_id=course2.id),
            Enrollment(student_id=student5.id, course_id=course2.id),
            
            Enrollment(student_id=student3.id, course_id=course3.id),
            Enrollment(student_id=student4.id, course_id=course3.id),
            Enrollment(student_id=student5.id, course_id=course3.id),
            Enrollment(student_id=student6.id, course_id=course3.id),
        ]
        
        db.session.add_all(enrollments)
        db.session.commit()