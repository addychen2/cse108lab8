from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.form import converts
from flask_admin.menu import MenuLink
from flask_login import current_user
from wtforms import Form, SelectField, PasswordField, StringField
from flask import request, flash
from models import User, Course, Enrollment
from werkzeug.security import generate_password_hash

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

class UserForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')
    name = StringField('Name')
    role = SelectField('Role', choices=[
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student')
    ], coerce=str)

class UserModelView(AdminModelView):
    column_list = ['id', 'username', 'name', 'role', 'password']
    column_searchable_list = ['username', 'name']
    column_filters = ['role']
    
    def create_form(self, obj=None):
        return UserForm(request.form)
    
    def edit_form(self, obj=None):
        # Don't clear password if the form was submitted
        if request.method == 'GET':
            form = UserForm(obj=obj)
            form.password.data = ''  # Clear password field in edit form for GET requests only
        else:
            form = UserForm(request.form, obj=obj)
        return form
    
    def on_model_change(self, form, model, is_created):
        # Handle password only if it's provided
        if form.password.data:  # Only update password if field is not empty
            model.password = generate_password_hash(form.password.data)
    
    def update_model(self, form, model):
        # Store the original password in case we need to restore it
        original_password = model.password
        
        try:
            # First update all fields except password
            form.populate_obj(model)
            
            # Then handle password separately
            if form.password.data:
                model.password = generate_password_hash(form.password.data)
                flash('Password updated successfully', 'success')
            else:
                # If password wasn't changed, restore the original
                model.password = original_password
            
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash('Failed to update. %s' % str(ex), 'error')
                return False
            return False
        
        return True
        
    def on_model_delete(self, model):
        # Delete all enrollments associated with this user first
        Enrollment.query.filter_by(student_id=model.id).delete()
        
    def delete_model(self, model):
        """
        Delete model.

        :param model: Model to delete
        """
        try:
            # Execute the on_model_delete hook
            self.on_model_delete(model)
            
            # Delete the model
            self.session.delete(model)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(f'Failed to delete record. {str(ex)}', 'error')
                self.session.rollback()
                return False
            
        return True

class CourseAdminView(AdminModelView):
    def _get_teacher_choices(self):
        return [(user.id, user.username) for user in User.query.all()]

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.teacher_id.choices = self._get_teacher_choices()
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.teacher_id.choices = self._get_teacher_choices()
        return form

    def scaffold_form(self):
        form_class = super().scaffold_form()
        form_class.teacher_id = SelectField('Teacher', coerce=int, choices=[])
        return form_class

    def on_model_delete(self, model):
        # Delete all enrollments associated with this course first
        Enrollment.query.filter_by(course_id=model.id).delete()
        # No need to commit here, Flask-Admin will handle it

class EnrollmentModelView(AdminModelView):
    form_columns = ['student_id', 'course_id', 'grade']
    column_list = ['id', 'student.username', 'student.name', 'course.name', 'grade']
    column_labels = {
        'student.username': 'Student Username',
        'student.name': 'Student Name',
        'course.name': 'Course Name'
    }
    column_searchable_list = ['student.username', 'student.name', 'course.name']
    column_filters = ['grade']
    
    def scaffold_form(self):
        form_class = super().scaffold_form()
        form_class.student_id = SelectField('Student', coerce=str)
        form_class.course_id = SelectField('Course', coerce=str)
        return form_class
    
    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.student_id.choices = [
            (str(student.id), f"{student.username} - {student.name}")
            for student in User.query.filter_by(role='student').all()
        ]
        form.course_id.choices = [
            (str(course.id), course.name)
            for course in Course.query.all()
        ]
        return form
    
    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.student_id.choices = [
            (str(student.id), f"{student.username} - {student.name}")
            for student in User.query.filter_by(role='student').all()
        ]
        form.course_id.choices = [
            (str(course.id), course.name)
            for course in Course.query.all()
        ]
        return form
    
    def on_model_change(self, form, model, is_created):
        model.student_id = int(form.student_id.data)
        model.course_id = int(form.course_id.data)
    
    def delete_model(self, model):
        """
        Delete model.

        :param model: Model to delete
        """
        try:
            self.on_model_delete(model)
            self.session.delete(model)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(f'Failed to delete record. {str(ex)}', 'error')
                self.session.rollback()
                return False
            
        return True
    
    def on_model_delete(self, model):
        # This is a hook method that can be used for additional actions
        # before deleting the model. By default, it does nothing.
        pass

class CustomAdminIndexView(AdminIndexView):
    def is_visible(self):
        return False

def init_admin(app, db):
    admin = Admin(app, name='ACME University Admin', template_mode='bootstrap3', index_view=CustomAdminIndexView())
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CourseAdminView(Course, db.session))
    admin.add_view(EnrollmentModelView(Enrollment, db.session))
    admin.add_link(MenuLink(name='Sign Out', url='/logout'))