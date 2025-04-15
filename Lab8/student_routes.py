from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Course, Enrollment, db

student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        return redirect(url_for('auth.login'))
    
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    enrolled_courses = [enrollment.course for enrollment in enrollments]
    
    return render_template('student_dashboard.html', 
                          user=current_user, 
                          enrolled_courses=enrolled_courses)

@student_bp.route('/courses')
@login_required
def all_courses():
    if current_user.role != 'student':
        return redirect(url_for('auth.login'))
    
    courses = Course.query.all()
    
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    enrolled_course_ids = [enrollment.course_id for enrollment in enrollments]
    
    for course in courses:
        course.enrolled = Enrollment.query.filter_by(course_id=course.id).count()
    
    return render_template('all_courses.html', 
                          user=current_user, 
                          courses=courses, 
                          enrolled_course_ids=enrolled_course_ids)

@student_bp.route('/enroll/<int:course_id>')
@login_required
def enroll_course(course_id):
    if current_user.role != 'student':
        return redirect(url_for('auth.login'))
    
    existing_enrollment = Enrollment.query.filter_by(
        student_id=current_user.id, course_id=course_id).first()
    
    if existing_enrollment:
        flash('You are already enrolled in this course')
        return redirect(url_for('student_bp.all_courses'))
    
    course = Course.query.get(course_id)
    enrollment_count = Enrollment.query.filter_by(course_id=course_id).count()
    
    if enrollment_count >= course.capacity:
        flash('This course has reached its capacity')
        return redirect(url_for('student_bp.all_courses'))
    
    new_enrollment = Enrollment(student_id=current_user.id, course_id=course_id)
    db.session.add(new_enrollment)
    db.session.commit()
    
    flash(f'Successfully enrolled in {course.name}')
    return redirect(url_for('student_bp.all_courses'))