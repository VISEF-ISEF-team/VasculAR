from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, EqualTo, Length


class Registration(FlaskForm):
    name = StringField("Tên cơ sở đăng ký sử dụng phần mềm", validators=[DataRequired()])
    email = StringField("Địa chỉ email", validators=[DataRequired()])
    phone = StringField("Số điện thoại", validators=[DataRequired()])
    verify_code = StringField("Mã xác thực", validators=[DataRequired()])
    administrator = StringField("Tên người chịu trách nhiệm", validators=[DataRequired()])
    administrator_contact = StringField("Số điện thoại liên lạc", validators=[DataRequired()])
    password_hash = PasswordField("Nhập mật khẩu", validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match')])
    password_hash2 = PasswordField("Nhập lại mật khẩu", validators=[DataRequired()])
    submit = SubmitField("Đăng ký ngay")
    
    
class Login(FlaskForm):
    email = StringField("Địa chỉ email", validators=[DataRequired()])
    password_hash = PasswordField("Nhập mật khẩu", validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match')])
    submit = SubmitField("Đăng nhập ngay")