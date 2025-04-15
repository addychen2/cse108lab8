from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField
from flask_login import current_user
from models import User, Course, Enrollment
from flask import current_app



class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'


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

# Custom view for Enrollment with dynamic foreign key dropdowns
class EnrollmentModelView(AdminModelView):
    form_columns = ['student_id', 'course_id', 'grade']

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.student_id.choices = [
            (str(student.id), student.name)
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
            (str(student.id), student.name)
            for student in User.query.filter_by(role='student').all()
        ]
        form.course_id.choices = [
            (str(course.id), course.name)
            for course in Course.query.all()
        ]
        return form

    def scaffold_form(self):
        form_class = super().scaffold_form()
        form_class.student_id = SelectField('Student', coerce=str)
        form_class.course_id = SelectField('Course', coerce=str)
        return form_class

    def on_model_change(self, form, model, is_created):
        model.student_id = int(form.student_id.data)
        model.course_id = int(form.course_id.data)

def init_admin(app, db):
    # Initialize the admin interface
    admin = Admin(app, name='ACME University Admin', template_mode='bootstrap3')

    # Add the custom Course view
    admin.add_view(CourseAdminView(Course, db.session))
    admin.add_view(EnrollmentModelView(Enrollment, db.session))

    # admin.add_view(AdminModelView(User, db.session))
    # admin.add_view(AdminModelView(Enrollment, db.session))


