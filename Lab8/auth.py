from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'student':
            return redirect(url_for('student_bp.dashboard'))
        elif current_user.role == 'teacher':
            return redirect(url_for('teacher_bp.dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin.index'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in, redirect to appropriate dashboard
    if current_user.is_authenticated:
        if current_user.role == 'student':
            return redirect(url_for('student_bp.dashboard'))
        elif current_user.role == 'teacher':
            return redirect(url_for('teacher_bp.dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin.index'))
            
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'student':
                return redirect(url_for('student_bp.dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('teacher_bp.dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin.index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully')
    return redirect(url_for('auth.login'))