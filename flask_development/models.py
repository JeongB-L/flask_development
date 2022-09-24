from datetime import datetime
import jwt
from flask_development import db, login_manager, app
from flask_login import UserMixin


#   extension to get a user by ID from database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
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

    def get_reset_token(self, expiration_sec=1800):
        #   token expires after 30 minutes.
        reset_token = jwt.encode({"user_id": self.id}, app.config['SECRET_KEY'], algorithm="HS256")
        return reset_token

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
        except:
            return None
        return User.query.get(user_id)

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
        return f"Post('{self.title}', '{self.date_posted}')"
