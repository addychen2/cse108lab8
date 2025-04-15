from flask import Flask
from flask_login import LoginManager
import os
from datetime import datetime

from models import db, User
from auth import auth_bp
from admin import init_admin
from student_routes import student_bp
from teacher_routes import teacher_bp
from data import create_initial_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enrollment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='')
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(teacher_bp, url_prefix='/teacher')

# Initialize admin
init_admin(app, db)

if __name__ == '__main__':
    with app.app_context():
        create_initial_data()
    app.run(debug=True)