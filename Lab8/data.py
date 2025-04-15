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
            username='addy', 
            password=generate_password_hash('password'), 
            role='teacher',
            name='Dr Chen'
        )
        
        teacher2 = User(
            username='liz', 
            password=generate_password_hash('password'), 
            role='teacher',
            name='Dr Ramos'
        )
        
        teacher3 = User(
            username='luis', 
            password=generate_password_hash('password'), 
            role='teacher',
            name='Dr Garibay'
        )
        
        student1 = User(
            username='javi', 
            password=generate_password_hash('password'), 
            role='student',
            name='Dr Gomez y Llagaria'
        )
        
        student2 = User(
            username='evan', 
            password=generate_password_hash('password'), 
            role='student',
            name='Evan A'
        )
        
        student3 = User(
            username='daniel', 
            password=generate_password_hash('password'), 
            role='student',
            name='Daniel Nestares'
        )
        
        student4 = User(
            username='TJkeny', 
            password=generate_password_hash('password'), 
            role='student',
            name='TJ Keny'
        )
        
        student5 = User(
            username='bighead', 
            password=generate_password_hash('password'), 
            role='student',
            name='Ryan Most'
        )
        
        student6 = User(
            username='jcm', 
            password=generate_password_hash('password'), 
            role='student',
            name='Julio Casal Monserrat'
        )
        
        db.session.add_all([
            admin, teacher1, teacher2, teacher3, 
            student1, student2, student3, student4, student5, student6
        ])
        db.session.commit()
        
        course1 = Course(
            name='CSE 120', 
            teacher_id=teacher2.id, 
            time='Monday 9:00-10:00 AM', 
            capacity=10
        )
        
        course2 = Course(
            name='CSE 150', 
            teacher_id=teacher1.id, 
            time='Friday 2:00-4:00 PM', 
            capacity=10
        )
        
        course3 = Course(
            name='CSE 277', 
            teacher_id=teacher3.id, 
            time='MWF 7:00-11:00 AM', 
            capacity=8
        )
        
        course4 = Course(
            name='CSE 108', 
            teacher_id=teacher1.id, 
            time='MF 8:00-11:00 PM', 
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
