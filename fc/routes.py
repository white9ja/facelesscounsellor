import os
import random
import secrets
from datetime import datetime
from datetime import date
from flask import render_template, request, session, logging, url_for, redirect, flash, request
from fc import app, db, bcrypt
from fc.forms import UserRegForm,FcRegForm, LoginForm,BioForm, ChangeAvatarForm, EditBioForm, UpdateEducationForm, UpdateLanguageForm, SpecializationForm,EditSpecForm, PostForm, EditPostForm,ChangePostImageForm
from flask_login import login_user, current_user, logout_user, login_required
from fc.models import User, Worker, Specialization, Posts





  # this is a function to upload the user ID Card
def save_app_file(filee):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(filee.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path, 'static/user_uploads', picture_fn)
  filee.save(picture_path)
  return picture_fn
  

# this is a function to upload the user Prfile Picture 
def save_image(fc_image):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(fc_image.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path, 'static/user_uploads', picture_fn)
  fc_image.save(picture_path)
  return picture_fn

#This is the function to post image in the post field
def post_image(post_img):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(post_img.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path, 'static/user_uploads', picture_fn)
  post_img.save(picture_path)
  return picture_fn



#This is the function to calculate age
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))




# This is the route for the defaault or welcome page  
@app.route('/')
def index():
 if current_user.is_authenticated:

  return redirect(url_for('fields'))
 return render_template('/index.html')




#This is the route to login to the system
@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('fields'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user)
      next_page = request.args.get('next')
      return redirect (next_page) if next_page else redirect (url_for('home'))
    else:
         flash(f'Incorrect or wrong Email / Password Combination! ', 'danger')
  return render_template('/login.html',title='Login', form=form)



        
# This is the route to add new user 
@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('fields'))
  form = UserRegForm()
  if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      user = User(username=form.username.data, email=form.email.data, password=hashed_password )
      db.session.add(user)
      db.session.commit()
      # flash(f'Account Created for {form.username.data} Successfully !', 'success')
      login_user(user)
      return redirect (url_for('home'))
  return render_template('register.html', title = 'Register', form=form)




#This is the route for thee Counsellors registration
@app.route('/register_fc', methods=['GET', 'POST'])
def register_fc():
    form = FcRegForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, name=form.name.data, email=form.email.data, password=hashed_password, phone=form.phone.data, gender=form.gender.data)
        db.session.add(user)
        db.session.commit()
        # flash(f'Account Created for {form.username.data} Successfully !', 'success')
        login_user(user)
        return redirect ('home')
    return render_template('register_fc.html', title = 'Register', form=form)




#This the route for the home page
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
  # page = request.args.get('page', 1, type=int)
  page = request.args.get('page', 1, type=int)
  workers = Worker.query.order_by(Worker.completed_at.desc()).paginate(page = page,  per_page=3)
  return render_template('/home.html', title='home', workers = workers)

#This the route for the home page
@app.route('/verified_worker', methods=['GET', 'POST'])
@login_required
def verified_worker():
  # page = request.args.get('page', 1, type=int)
  page = request.args.get('page', 1, type=int)
  workers = Worker.query.order_by(Worker.completed_at.desc()).paginate(page = page,  per_page=3)
  return render_template('/verified_worker.html', title='Verified_worker', workers = workers)



#This is the route to access the field page 
@app.route('/field', methods=['GET', 'POST'])
@login_required
def field():
  page = request.args.get('page', 1, type=int)
  page1 = request.args.get('page', 1, type=int)
  posts = Posts.query.order_by(Posts.posted_date.desc()).paginate(page = page,  per_page=2)
  workers = Worker.query.order_by(Worker.completed_at.desc())
  return render_template('/field.html', title='field', workers = workers, posts = posts)


@app.route('/fields', methods=['GET', 'POST'])
@login_required
def fields():
  page = request.args.get('page', 1, type=int)
  page1 = request.args.get('page', 1, type=int)
  posts = Posts.query.order_by(Posts.posted_date.desc()).paginate(page = page,  per_page=4)
  workers = Worker.query.order_by(Worker.completed_at.desc())
  return render_template('/fields.html', title='field', workers = workers, posts = posts)


#This is the route to access the field post detail 
@app.route('/post_detail/<int:post_id>')
@login_required
def post_detail(post_id):
  # page = request.args.get('page', 1, type=int)
  page = request.args.get('page', 1, type=int)
  post= Posts.query.get(post_id)
  posts = Posts.query.filter_by(post_id= post.post_id)
  workers = Worker.query.order_by(Worker.completed_at.desc()).paginate(page = page,  per_page=2)
  # image = url_for('static', filename='user_uploads/' + str(worker.fc_image))
  return render_template('/post_detail.html',  posts = posts, workers=workers)




#This is the route to access the user profile from the field page
@app.route('/user_pro/<email>')
@login_required
def user_pro(email):
  user= User.query.get(email)
 
  users= User.query.filter_by(email = user.email)
  image = url_for('static', filename='user_uploads/' + str(user.fc_image))
  return render_template('/details.html',  users = users, preposts= preposts, image = image)




#This is the route to access the counsellor profile from the field page
@app.route('/fc_pro/<int:fc_id>')
@login_required
def fc_pro(fc_id):
  worker= Worker.query.get(fc_id)
  specials = Specialization.query.filter_by(email= worker.email).order_by(Specialization.completed_at.desc())
  workers= Worker.query.filter_by(email = worker.email)
  image = url_for('static', filename='user_uploads/' + str(worker.fc_image))
  return render_template('/fc_pro.html',  workers = workers, specials = specials, image = image)



#This is the route to access the counsellor details from the recently verified counellor page
@app.route('/details/<int:fc_id>')
@login_required
def detail(fc_id):
  worker= Worker.query.get(fc_id)
  specials = Specialization.query.filter_by(email= worker.email).order_by(Specialization.completed_at.desc())
  workers= Worker.query.filter_by(email = worker.email)
  image = url_for('static', filename='user_uploads/' + str(worker.fc_image))
  return render_template('/details.html',  workers = workers, specials = specials, image = image)



#Thi is the route to access the field poster detail from field page
@app.route('/user_detail/<email>')
@login_required
def user_detail(email):
  users= User.query.filter_by(email = email).first()
  if users.gender != None:
    worker= Worker.query.filter_by(email= users.email).first()
    preposts = Posts.query.filter_by(poster_email= users.email).order_by(Posts.posted_date.desc())
    specials = Specialization.query.filter_by(email= worker.email).order_by(Specialization.completed_at.desc())
    workers= Worker.query.filter_by(email = worker.email)
    image = url_for('static', filename='user_uploads/' + str(worker.fc_image))
    return render_template('/fc_pro.html',  workers = workers, preposts=preposts, specials = specials, image = image)   
  else:
    preposts = Posts.query.filter_by(poster_email= users.email).order_by(Posts.posted_date.desc())
    image = url_for('static', filename='user_uploads/' + str(users.fc_image))
    users= User.query.filter_by(email = users.email) 
    return render_template('/user_pro.html', preposts=preposts, users = users, image = image)



#This is the route to create a post
@app.route('/post',methods=['GET', 'POST'])
@login_required
def post():
  form = PostForm()
  if form.validate_on_submit():
    post_file = post_image(form.post_img.data)
    post = Posts(poster_email=current_user.email, poster_username=current_user.username, poster_img=current_user.fc_image,post_id=random.randint(0,999),post_title= form.title.data, post_desc= form.description.data,post_img= post_file)
    db.session.add(post)
    db.session.commit()
    return redirect (url_for('fields'))
  return render_template('/post.html', title = 'post', form = form)



#This is the route to view your previous post
@app.route('/my_posts')
@login_required
def my_post():
  posts = Posts.query.filter_by(poster_email= current_user.email).order_by(Posts.posted_date.desc())
  return render_template('/my_posts.html', title='My Posts', posts = posts)




#This is the route to update the your post
@app.route('/post/<int:post_id>/update',methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
  form = EditPostForm()
  specials = Specialization.query.filter_by(email= current_user.email)
  posts = Posts.query.get(post_id)
  if form.validate_on_submit():
    # post_file = post_image(form.post_img.data)
    posts.post_title = form.title.data
    posts.post_desc = form.description.data
    db.session.commit()
    flash(f'Updated Successfully !', 'success')
    return redirect (url_for('my_post', post_id = posts.id))
  elif request.method == 'GET':
    form.title.data = posts.post_title
    form.description.data = posts.post_desc
  image = url_for('static', filename='user_uploads/' + str(current_user.fc_image))
  return render_template('editpost.html', title = 'Edit Post', image = image,  form=form,posts =posts, post_id = posts.id)




#This is the route to update  the post avartar /photo
@app.route('/post_avarter/<int:post_id>/update',methods=['GET', 'POST'])
@login_required
def post_avartar( post_id):
   form = ChangePostImageForm()
   if form.validate_on_submit():

    if form.post_img.data:
      picture_fil = save_image(form.post_img.data)  
      update_post = Posts.query.get(post_id)
    
      # update_image.fc_image = picture_fil
      update_post.post_img = picture_fil
      db.session.commit()
      #flash('Profile Image Updated Successfully!', 'success')
    return redirect (url_for('my_post'))
   else:

    image = url_for('static', filename='user_uploads/' + str(current_user.fc_image))
    return render_template('/post_avarter.html', title='Profile', form = form)




#This is the route to delete your previous post by id
@app.route('/posts/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def del_post(post_id):
  post = Posts.query.get(post_id)
  db.session.delete(post)
  db.session.commit()
  flash(f'Post Deleted Successfully !', 'success')
  return redirect (url_for('my_post'))



#This is the route to add your bio data or complete your registration
@app.route('/bio', methods=['GET', 'POST'])
@login_required
def bio():
  # workers = Worker.query.filter_by(email=current_user.email).first()
  form = BioForm()
  if form.validate_on_submit():

    picture_file = save_image(form.fc_image.data)
    current_user.fc_image = picture_file
    # picture_fill = save_id_card(form.id_card.data)
    current_user.pro_status = 1
    worke = Worker(name=current_user.name, email=current_user.email, phone= current_user.phone, gender=current_user.gender, role = 'Counsellor', date_of_birth=form.date_of_birth.data, country= form.country.data, city=form.city.data, about= form.about.data, marrital_status=form.marrital_status.data, education=form.education.data, religion= form.religion.data, languages=form.languages.data, fc_id = random.randint(0,999), number_of_jobs= 0, stars= 3, status= 1, fc_image = picture_file)
    db.session.add(worke)
    db.session.commit()
    flash(f'Your Bio is completed! Please proceed with Assesment', 'success')
    return redirect (url_for('profile'))
  image = url_for('static', filename='user_uploads/' + str(current_user.fc_image))
  return render_template('/bio.html', title='bio', image = image, form=form)




#This is the route to edit your profile
@app.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editpro():

  # worker = Workers.query.get(email= current_user.email)
  worker = Worker.query.filter_by(email=current_user.email).first()
  form = EditBioForm()
  if form.validate_on_submit():
    worker.email= current_user.email
    worker.about= form.about.data
    worker.marrital_status= form.marrital_status.data
    worker.country= form.country.data
    worker.city = form.city.data
    worker.date_of_birth = form.date_of_birth.data
    db.session.commit()
    flash('Profile Updated Successfully!', 'success')
    return redirect (url_for('profile'))
  elif request.method == 'GET':
    form.about.data = worker.about
    form.marrital_status.data = worker.marrital_status
    form.country.data = worker.country
    form.city.data = worker.city
    
  image = url_for('static', filename='user_uploads/' + str(current_user.fc_image))
  return render_template('/editprofile.html', title='Profile', image = image, form = form)



#This is the route to edit the Education
@app.route('/edu' , methods=['GET', 'POST'])
@login_required
def editedu():
  update_edu = Worker.query.filter_by(email=current_user.email).first()
  form = UpdateEducationForm()
  if form.validate_on_submit():
    
    update_edu.education = form.education.data
    db.session.commit()
    # flash('Education Updated Successfully!', 'success')
    return redirect (url_for('profile'))
  elif request.method == 'GET':
    form.education.data = update_edu.education

  image = url_for('static', filename='user_uploads/' + str(current_user.fc_image))
  return render_template('/editedu.html', title='Edit Education', image = image, form = form)




#This is the route to edit the Languages
@app.route('/language' , methods=['GET', 'POST'])
@login_required
def editlang():
  update_lang = Worker.query.filter_by(email=current_user.email).first()
  form = UpdateLanguageForm()
  if form.validate_on_submit():
    
    update_lang.languages = form.languages.data
    db.session.commit()
    # flash('Languages Updated Successfully!', 'success')
    return redirect (url_for('profile'))
  elif request.method == 'GET':
    form.languages.data = update_lang.languages

  image = url_for('static', filename='user_uploads/' + str(current_user.fc_image))
  return render_template('/editlang.html', title='Edit Education', image = image, form = form)




#This is the route to create Specialization
@app.route('/specialization', methods=['GET', 'POST'])
@login_required
def services():
    form = SpecializationForm()
    specials = Specialization.query.filter_by(email= current_user.email).order_by(Specialization.completed_at.desc())
    if form.validate_on_submit():
        spec = Specialization(email=current_user.email, spec=form.spec.data, spec_status=1 )
        db.session.add(spec)
        db.session.commit()
        flash(f'Specialization added Successfully !', 'success')
        return redirect (url_for('services'))
    image = url_for('static', filename='user_uploads/' + str(current_user.fc_image))
    return render_template('specialization.html', title = 'Add Specialization', image = image, specials = specials,  form=form)




#This is the route to edit services or Specialization
@app.route('/services/<int:spec_id>/update',methods=['GET', 'POST'])
@login_required
def edit_service(spec_id):
  form = EditSpecForm()
  specials = Specialization.query.filter_by(email= current_user.email)
  specs = Specialization.query.get(spec_id)
  if form.validate_on_submit():
    specs.spec = form.spec.data
    db.session.commit()
    flash(f'Updated Successfully !', 'success')
    return redirect (url_for('services', spec_id = specs.id))
  elif request.method == 'GET':
    form.spec.data = specs.spec
  image = url_for('static', filename='user_uploads/' + str(current_user.fc_image))
  return render_template('editspec.html', title = 'Add Specialization', image = image, specials = specials,  form=form, spec_id = specs.id)



# This is the route to delete services or specialization
@app.route('/services/<int:spec_id>/delete', methods=['GET', 'POST'])
@login_required
def del_service(spec_id):
  spec = Specialization.query.get(spec_id)
  db.session.delete(spec)
  db.session.commit()
  flash(f'Sevice Deleted Successfully !', 'success')
  return redirect (url_for('services'))


   
#This is the route to access the profile page
@app.route('/profile')
@login_required
def profile():
  specials = Specialization.query.filter_by(email= current_user.email).order_by(Specialization.completed_at.desc())
  workers = Worker.query.filter_by(email = current_user.email)
  users= User.query.filter_by(email = current_user.email)
  image = url_for('static', filename='user_uploads/' + str(current_user.fc_image))
  return render_template('/profile.html', title='Profile', image = image, workers = workers, users=users, specials = specials, datetime = datetime)



#This is the route to update the post Avartar or the the posted photo
@app.route('/avarter' , methods=['GET', 'POST'])
@login_required
def avartar():
   form = ChangeAvatarForm()
   if form.validate_on_submit():

    if form.fc_image.data:

      picture_fil = save_image(form.fc_image.data)
      current_user.fc_image = picture_fil
      update_image = Worker.query.filter_by(email=current_user.email).first()
      user_update= User.query.filter_by(email=current_user.email).first()
      post_update= Posts.query.filter_by(poster_email=current_user.email).first()
      if post_update :
        post_update.poster_img = picture_fil
    
      update_image.fc_image = picture_fil
      user_update.fc_image = picture_fil
      db.session.commit()
      flash('Profile Image Updated Successfully!', 'success')
    return redirect (url_for('profile'))
   else:

    image = url_for('static', filename='user_uploads/' + str(current_user.fc_image))
    return render_template('/avarter.html', title='Profile', image = image, form = form)



#This is the route to log out of the system
@app.route('/logout', methods=['GET', 'POST'])
def logout():
  logout_user()
  return redirect(url_for('index'))
   



# @app.route('/', methods=['GET', 'POST'])
# def index():
#  # if current_user.is_authenticated:
#  #    return redirect(url_for('home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#       user = User.query.filter_by(email=form.email.data).first()
#       if user and bcrypt.check_password_hash(user.password, form.password.data):
#         login_user(user)
#         next_page = request.args.get('next')
#         return redirect (next_page) if next_page else redirect (url_for('home'))
#       else:
#            flash(f'Incorrect or wrong Email / Password Combination! ', 'danger')
#     return render_template('/index.html',title='Login', form=form)


# #This is the route to access the welcome page
# @app.route('/welcome')
# def welcome():
#     return render_template('/welcome.html', title = 'welcome')