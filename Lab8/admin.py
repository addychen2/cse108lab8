from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from models import User, Course, Enrollment

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

def init_admin(app, db):
    # Create admin interface
    admin = Admin(app, name='ACME University Admin', template_mode='bootstrap3')
    
    # Exclude User for now if it's causing issues
    # admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Course, db.session))
    admin.add_view(AdminModelView(Enrollment, db.session))