from flask_development.models import User, Post
from flask import render_template, url_for, flash, redirect
from flask_development import app
from flask_development.forms import RegistrationForm, LoginForm

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
    form = RegistrationForm()
    #   if the submitted username, email, password, and confirm-password are written and follows the given standard
    #   flashes the message, sends ''success' and it is a bootstrap class that is a category
    #   files have access to it, and redirects to home.html
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
