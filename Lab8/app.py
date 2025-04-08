from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enrollment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teacher = db.relationship('User', backref=db.backref('courses', lazy=True))
    time = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Course {self.name}>'

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    grade = db.Column(db.Integer, nullable=True)
    student = db.relationship('User', backref=db.backref('enrollments', lazy=True))
    course = db.relationship('Course', backref=db.backref('enrollments', lazy=True))
    
    def __repr__(self):
        return f'<Enrollment {self.student_id} in {self.course_id}>'

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

admin = Admin(app, name='ACME University Admin', template_mode='bootstrap3')
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Course, db.session))
admin.add_view(AdminModelView(Enrollment, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin.index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        return redirect(url_for('login'))
    
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    enrolled_courses = [enrollment.course for enrollment in enrollments]
    
    return render_template('student_dashboard.html', 
                          user=current_user, 
                          enrolled_courses=enrolled_courses)

@app.route('/student/courses')
@login_required
def all_courses():
    if current_user.role != 'student':
        return redirect(url_for('login'))
    
    courses = Course.query.all()
    
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    enrolled_course_ids = [enrollment.course_id for enrollment in enrollments]
    
    for course in courses:
        course.enrolled = Enrollment.query.filter_by(course_id=course.id).count()
    
    return render_template('all_courses.html', 
                          user=current_user, 
                          courses=courses, 
                          enrolled_course_ids=enrolled_course_ids)

@app.route('/student/enroll/<int:course_id>')
@login_required
def enroll_course(course_id):
    if current_user.role != 'student':
        return redirect(url_for('login'))
    
    existing_enrollment = Enrollment.query.filter_by(
        student_id=current_user.id, course_id=course_id).first()
    
    if existing_enrollment:
        flash('You are already enrolled in this course')
        return redirect(url_for('all_courses'))
    
    course = Course.query.get(course_id)
    enrollment_count = Enrollment.query.filter_by(course_id=course_id).count()
    
    if enrollment_count >= course.capacity:
        flash('This course has reached its capacity')
        return redirect(url_for('all_courses'))
    
    new_enrollment = Enrollment(student_id=current_user.id, course_id=course_id)
    db.session.add(new_enrollment)
    db.session.commit()
    
    flash(f'Successfully enrolled in {course.name}')
    return redirect(url_for('all_courses'))

@app.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
    if current_user.role != 'teacher':
        return redirect(url_for('login'))
    
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    
    for course in courses:
        course.enrolled = Enrollment.query.filter_by(course_id=course.id).count()
    
    return render_template('teacher_dashboard.html', 
                          user=current_user, 
                          courses=courses)

@app.route('/teacher/course/<int:course_id>')
@login_required
def course_details(course_id):
    if current_user.role != 'teacher':
        return redirect(url_for('login'))
    
    course = Course.query.get(course_id)
    if not course or course.teacher_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('teacher_dashboard'))
    
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    
    return render_template('course_details.html', 
                          user=current_user, 
                          course=course, 
                          enrollments=enrollments)

@app.route('/teacher/update_grade', methods=['POST'])
@login_required
def update_grade():
    if current_user.role != 'teacher':
        return redirect(url_for('login'))
    
    enrollment_id = request.form.get('enrollment_id')
    new_grade = request.form.get('grade')
    course_id = request.form.get('course_id')
    
    enrollment = Enrollment.query.get(enrollment_id)
    
    if not enrollment or enrollment.course.teacher_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('teacher_dashboard'))
    
    enrollment.grade = new_grade
    db.session.commit()
    
    flash('Grade updated successfully')
    return redirect(url_for('course_details', course_id=course_id))

if __name__ == '__main__':
    with app.app_context():
        create_initial_data()
    app.run(debug=True)