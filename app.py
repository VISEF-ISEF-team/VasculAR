# Flask Backend Framework
from flask import *
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
import os

#  ----------- Form Backup -----------
from form_backup import Registration, Login

#  ----------- 3D rendering -----------
from render_3D import rendering

# ----------- Keys and Global Variables -----------
app = Flask(__name__)
app.config["SECRET_KEY"] = "isef" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] =  'static/data'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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
    patients = db.relationship('Patients', backref='org')
    
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

class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    age = db.Column(db.String(255), nullable=False)
    pre_disease = db.Column(db.String(255), nullable=False)
    note = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

@app.route("/")
def home():
    all_orgs = Organizations.query.order_by(Organizations.date_added)
    return render_template("home.html", all_orgs=all_orgs)


# A function to check if the file extension is allowed
ALLOWED_EXTENSIONS = set(['nii.gz', 'dcm', 'vtk', 'nii'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route("/upload", methods=["POST"]) 
def uploader(): 
    imagefile = request.files['imagefile'] 
    if imagefile.filename == '': 
        return render_template('twoDseg.html', progress_bar_animated=False, not_file=True)
    if imagefile: 
        filename = secure_filename(imagefile.filename) 
        image_path = "static/data/" + imagefile.filename 
        imagefile.save(os.path.join(app.config['UPLOAD_FOLDER'], 'input.nii.gz')) 
        session['image_path'] = image_path 
        return redirect(url_for('twoDseg')) 
    else: 
        return "File not allowed"
    
    
@app.route("/rendering", methods=["GET", "POST"]) 
def render():
    render_obj = rendering("static/data/output.nii.gz")
    # render_obj.show_mesh()
    render_obj.segmented_reconstruction()
    return redirect(url_for('twoDseg'))

@app.route("/registration", methods=["GET", "POST"]) 
def registration():
    name = None
    form = Registration()
    if form.validate_on_submit():
        org = Organizations.query.filter_by(email=form.email.data).first()
        if org is None: 
            hased_pw = generate_password_hash(form.password_hash.data, "sha256")
            org = Organizations(name=form.name.data, email=form.email.data, phone=form.phone.data, verify_code=form.verify_code.data, administrator=form.administrator.data, administrator_contact=form.administrator_contact.data, password_hash=hased_pw)
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

@login_manager.user_loader
def load_user(user_id):
    return Organizations.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    print('in the form submit')
    form = Login()
    if form.validate_on_submit():
        
        org = Organizations.query.filter_by(email=form.email.data).first()
        if org:
            if check_password_hash(org.password_hash, form.password_hash.data):
                login_user(org)
                return redirect(url_for('home'))
            else:
                flash('Wrong password. Please try again')
        else:
            flash('User does not exist. Please sign up to create an account')
    return render_template("login.html", form=form)

@app.route("/twoDseg")
def twoDseg():
    return render_template("twoDseg.html")


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