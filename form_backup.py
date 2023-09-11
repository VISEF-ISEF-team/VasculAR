from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, EqualTo, Length


class Registration(FlaskForm):
    name = StringField("Organization name", validators=[DataRequired()])
    email = StringField("Email address", validators=[DataRequired()])
    phone = StringField("Phone number", validators=[DataRequired()])
    verify_code = StringField("Verify code", validators=[DataRequired()])
    administrator = StringField("Administrator name", validators=[DataRequired()])
    administrator_contact = StringField("Administrator phone", validators=[DataRequired()])
    password_hash = PasswordField("Enter password", validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match')])
    password_hash2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Register now")