from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Course, Enrollment, db

teacher_bp = Blueprint('teacher_bp', __name__)

@teacher_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'teacher':
        return redirect(url_for('auth.login'))
    
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    
    for course in courses:
        course.enrolled = Enrollment.query.filter_by(course_id=course.id).count()
    
    return render_template('teacher_dashboard.html', 
                          user=current_user, 
                          courses=courses)

@teacher_bp.route('/course/<int:course_id>')
@login_required
def course_details(course_id):
    if current_user.role != 'teacher':
        return redirect(url_for('auth.login'))
    
    course = Course.query.get(course_id)
    if not course or course.teacher_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('teacher_bp.dashboard'))
    
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    
    return render_template('course_details.html', 
                          user=current_user, 
                          course=course, 
                          enrollments=enrollments)

@teacher_bp.route('/update_grade', methods=['POST'])
@login_required
def update_grade():
    if current_user.role != 'teacher':
        return redirect(url_for('auth.login'))
    
    enrollment_id = request.form.get('enrollment_id')
    new_grade = request.form.get('grade')
    course_id = request.form.get('course_id')
    
    enrollment = Enrollment.query.get(enrollment_id)
    
    if not enrollment or enrollment.course.teacher_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('teacher_bp.dashboard'))
    
    enrollment.grade = new_grade
    db.session.commit()
    
    flash('Grade updated successfully')
    return redirect(url_for('teacher_bp.course_details', course_id=course_id))