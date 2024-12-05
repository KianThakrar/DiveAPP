from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  # Email validation included
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])  # Email validation included
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')  # No need for the `message` if you're okay with the default
    ])
    submit = SubmitField('Register')



class AddDiveForm(FlaskForm):
    site_id = SelectField('Dive Site', coerce=int, validators=[DataRequired()])
    date = StringField('Dive Date and Time', validators=[DataRequired()])  # StringField to accept datetime-local
    submit = SubmitField('Add Dive')
    




class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField(
        'New Password',
        validators=[
            DataRequired(),
            Length(min=6, message="Password must be at least 8 characters."),
        ],
    )
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(),
            EqualTo('new_password', message="Passwords must match."),
        ],
    )
    submit = SubmitField('Change Password')
