from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_moment import Moment
from fc.momentjs import momentjs



import datetime

today = datetime.datetime.now()


app= Flask(__name__)

app.config['SECRET_KEY'] = 'thisisforfc743gdg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/fc.db'
app.jinja_env.globals['momentjs'] = momentjs


db = SQLAlchemy(app)
db.init_app(app)

with app.app_context():
    db.create_all()
# db = SQLAlchemy(session_options={"autoflush": False})
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
moment = Moment(app)

from fc.models import User, Worker, Specialization, Posts

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))




from fc import routes




