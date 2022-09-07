
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '040223a0433bf68e93ab94f62dcaecf5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

#from app import db
#   db.create_all()
#   now our server is created
#   dp.drop_all() removes all the data

class User(db.Model):
    #   this id will be a unique id for the user
    id = db.Column(db.Integer, primary_key=True)
    #   username is string, max length 20, it is unique, and cannot be null
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #   profile picture, when image is hashed it will have max length 20, no need to be unique, cannot be null
    #   default.jpg is our default image_file
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    #   hashed password will have 60 max length
    password = db.Column(db.String(60), nullable=False)
    #   our posts attribute has a relation to Post, backref added a new column author,  lazy=True means
    #   that SQLAlchemy will load that related data
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #   user id of the author of this post object, foreignkey references to the name of the table/column
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"
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


if __name__ == '__main__':
    app.run(debug=True)