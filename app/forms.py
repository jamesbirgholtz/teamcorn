from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email')
    password = PasswordField('Password', validators=[DataRequired()])
    role = RadioField(choices=[(0, 'Customer'), (1, 'Staff'), (2, 'Admin')], default=0, validators=[DataRequired()])
    dept = RadioField(choices=[(0, 'Unsure'), (1, 'HR'), (2, 'Marketing'), (3, 'R&D'), (4, 'Development')], default=0, validators=[DataRequired()])
    submit = SubmitField('Register')


class TicketForm(FlaskForm):
    created_by = StringField('Created by', validators=[DataRequired()])
    dept = StringField('Department', validators=[DataRequired()])
    title = StringField('Title: ', validators=[DataRequired()])
    description = StringField('Description')
    location = StringField('Location')
    attachment = StringField('Attachment(s)')
    submit = SubmitField('Submit Ticket')
