from datetime import datetime
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from fc import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
  return User.query.filter_by(id=user_id).first()   


class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    secret_key = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.String(255), nullable=True)
    state_of_origin = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    date_of_birth =db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True, default='default.jpg')
    fc_image = db.Column(db.String(255), nullable=True, default='default.jpg')
    pro_status = db.Column(db.String(255), nullable=True, default= 0)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())


class Worker(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    fc_id = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    date_of_birth =db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    age = db.Column(db.String(255), nullable=True)
    about = db.Column(db.String(255), nullable=True)
    id_card = db.Column(db.String(255), nullable=True)
    marrital_status = db.Column(db.String(255), nullable=True)
    education = db.Column(db.String(255), nullable=True)
    religion = db.Column(db.String(255), nullable=True)
    languages = db.Column(db.String(255), nullable=True)
    hobbies = db.Column(db.String(255), nullable=True)
    number_of_jobs = db.Column(db.String(255), nullable=True)
    stars = db.Column(db.String(255), nullable=True)
    fc_image = db.Column(db.String(255), nullable=True, default='default.jpg')
    image = db.Column(db.String(255), nullable=True, default='default.jpg')
    completed_at = db.Column(db.DateTime(), default=datetime.utcnow)
    status = db.Column(db.String(255), nullable=True, default= 0)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime()) 


class Specialization(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    fc_id = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=False)
    spec = db.Column(db.String(255),  nullable=False)
    spec_status = db.Column(db.String(255), nullable=True, default= 0)
    completed_at = db.Column(db.DateTime(), default=datetime.utcnow)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())






class Posts(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    poster_username = db.Column(db.String(255), nullable=False)
    poster_email = db.Column(db.String(255), nullable=False)
    poster_img = db.Column(db.String(255), nullable=False)
    post_id = db.Column(db.String(255), nullable=True)
    post_title = db.Column(db.String(255), nullable=True)
    post_desc = db.Column(db.String(255), nullable=True)
    post_img = db.Column(db.String(255), nullable=True)
    post_like = db.Column(db.String(255), nullable=True)
    post_relate = db.Column(db.String(255), nullable=True)
    post_message = db.Column(db.String(255), nullable=True)
    post_trend = db.Column(db.String(255), nullable=True)
    posted_date = db.Column(db.DateTime(), default=datetime.utcnow)
    post_status = db.Column(db.String(255), nullable=True, default= 0)
    completed_at = db.Column(db.DateTime(), default=datetime.utcnow)
    status = db.Column(db.String(255), nullable=True, default= 0)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime()) 



# class Post(db.Model, UserMixin):


#     id = db.Column(db.Integer, primary_key=True)
#     poster = db.Column(db.String(255), nullable=False)
#     post_id = db.Column(db.String(255), nullable=False)
#     title = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.String(255), unique=True, nullable=False)
#     filee = db.Column(db.String(255), nullable=True)
#     screenshot = db.Column(db.String(255), nullable=True)
#     completed_at = db.Column(db.DateTime(), default=datetime.utcnow)
#     status = db.Column(db.String(255), nullable=True, default= 0)
#     active = db.Column(db.Boolean())
#     confirmed_at = db.Column(db.DateTime())  



