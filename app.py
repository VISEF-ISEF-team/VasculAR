# Machine Learning libs
import tensorflow as tf

# Flask Backend Framework
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_from_directory, current_app
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime

# From backup
from form_backup import Registration

# ----------- Keys and Global Variables -----------
app = Flask(__name__)
app.config["SECRET_KEY"] = "isef" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ----------- Database -----------
class Organizations(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email =  db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(120), nullable=False)
    administrator = db.Column(db.String(120), nullable=False)
    administrator_contact = db.Column(db.String(120), nullable=False)
    verify_code = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(200))
    
    @property
    def password():
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify(self, password):
        return check_password_hash(self.password_hash, password)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/registration", methods=["GET", "POST"]) 
def registration():
    name = None
    form = Registration()
    if form.validate_on_submit():
        org = Organizations.query.filter_by(email=form.email.data).first()
        if org is None: 
            hased_pw = generate_password_hash(form.password_hash.data, "sha256")
            org = Organizations(name=form.name.data, email=form.email.data, phone=form.phone.data, administrator=form.administrator.data, administrator_contact=form.administrator_contact.data, password_hash=hased_pw)
            db.session.add(org)
            db.session.commit()

        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        form.phone.data = ""
        form.administrator.data = ""
        form.administrator_contact.data = ""
        form.password_hash.data = ""
        return redirect(url_for('login'))
    
    all_orgs = Organizations.query.order_by(Organizations.date_added)
    return render_template("registration.html", form=form, name=name, all_orgs=all_orgs)



@app.route("/login")
def login():
    return render_template("login.html")


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)