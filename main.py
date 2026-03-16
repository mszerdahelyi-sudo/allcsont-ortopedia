from flask import Flask, render_template, request, redirect, url_for, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'allcsont-ortopedia-secret-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# MODELS
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clinic_name = db.Column(db.String(100), default='Allcsont Ortopédia')
    primary_color = db.Column(db.String(7), default='#006994')
    phone = db.Column(db.String(20), default='+36 20 123 4567')
    email = db.Column(db.String(100), default='info@allcsont-ortopedia.hu')
    address = db.Column(db.String(200), default='1122 Budapest, Városmajor u. 47/B.')
    hours = db.Column(db.String(100), default='Hétfő 8:00-12:00, Csütörtök 16:00-19:00')

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    title = db.Column(db.String(100))
    bio = db.Column(db.Text)
    image_url = db.Column(db.String(200))

# ADMIN
admin = Admin(app, name='Allcsont Admin')

class ProtectedModelView(ModelView):
    def is_accessible(self):
        return True  # open for now - change to current_user.is_authenticated later if you want

admin.add_view(ProtectedModelView(Doctor, db.session))
admin.add_view(ProtectedModelView(Setting, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ROUTES
@app.route('/')
def home():
    setting = Setting.query.first() or Setting()
    return render_template('index.html', setting=setting)

@app.route('/allcsont-ortopedia')
def about():
    setting = Setting.query.first() or Setting()
    return render_template('allcsont_ortopedia.html', setting=setting)

@app.route('/orvosaink')
def doctors():
    doctors_list = Doctor.query.all()
    setting = Setting.query.first() or Setting()
    return render_template('orvosaink.html', doctors=doctors_list, setting=setting)

@app.route('/kapcsolat', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Üzenet elküldve! Hamarosan jelentkezünk.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password_hash, request.form.get('password')):
            login_user(user)
            return redirect('/admin')
        flash('Hibás adatok', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

# INIT + HARD-CODED DEFAULTS
with app.app_context():
    db.create_all()
    if not User.query.first():
        u = User(username='admin')
        u.password_hash = generate_password_hash('change-this-123')
        db.session.add(u)
        db.session.commit()
    if not Setting.query.first():
        db.session.add(Setting())
        db.session.commit()
    if not Doctor.query.first():
        db.session.add(Doctor(name="Dr. Illés Emil", title="Fogszabályozó és állcsontortopéd szakorvos", bio="Dr. Illés Emil vagyok, a Heim Pál Országos Gyermekgyógyászati Intézet Állcsontortopédiai és Fogszabályozási Osztályának gyermek-dento-alveoláris sebésze...", image_url="/static/uploads/Emil profilfotó.jpg"))
        db.session.add(Doctor(name="Dr. Földesi Marcell", title="Fogszabályozó szakorvos", bio="Fogorvosi diplomámat a Semmelweis Egyetem Fogorvostudományi Karán szereztem...", image_url="/static/uploads/FM.png"))
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)