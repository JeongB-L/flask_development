import secrets
import os
from PIL import Image
from flask_development.models import User, Post
from flask import render_template, url_for, flash, redirect, request
from flask_development import app, db, bcrypt
from flask_development.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required

#from app import db
#   db.create_all()
#   now our server is created
#   dp.drop_all() removes all the data

posts = [
    {
        'author': 'JBL',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'need tacobell',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    #   if the submitted username, email, password, and confirm-password are written and follows the given standard
    #   flashes the message, sends ''success' and it is a bootstrap class that is a category
    #   files have access to it, and redirects to home.html
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #   create a user with hashed password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #   add user to our database
        db.session.add(user)
        db.session.commit()
        flash('Your account is now created! You may  now log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #   login_user literally logs the user in
            login_user(user, remember=form.remember.data)
            #   the original page that the unlogged in user wanted to get in
            next_page = request.args.get('next')
            #flash('Login Success', 'success')
            #   redirects to next page if next_page exists. Else, redirects to /home
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Failed. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    #   returns the filename without extension and the file with extension
    #   just filename will not be used
    _, f_ext = os.path.splitext(form_picture.filename)
    #   concat hexed picture data with its extension
    picture_fn = random_hex + f_ext
    #   joining the path for the picture file; concatination
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    #   resize the picture using pillow
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    #   save the image
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)