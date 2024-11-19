"""Models for Blogly."""
# This is the docstring for the file, describing its purpose. This file contains the models used in the Blogly application, which represent the database schema.

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# Importing the SQLAlchemy class from Flask-SQLAlchemy, which is used to interact with a relational database in a Flask application.



db = SQLAlchemy()
# Creating an instance of the SQLAlchemy class. This object will be used to define the models and handle database interactions.


def connect_db(app):
    # This function is used to connect the Flask app to the database.
    db.app = app
    # Attaching the Flask app instance to the SQLAlchemy object so it knows which app to interact with.
    db.init_app(app)
    # Initializing the app with the SQLAlchemy object. This links the app and the database, enabling them to work together.




# MODELS GO BELOW!
# This is a comment indicating that the database models (representing tables in the database) will be defined below.

class User(db.Model):
    # This is a model class named 'User', which inherits from 'db.Model', the base class for all models in SQLAlchemy.
    __tablename__ = "users"
    # Specifies the name of the database table associated with this model. The table will be named "users".



    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Defines a column named 'id' in the 'users' table.
    # - 'db.Integer': Specifies that this column will store integers.
    # - 'primary_key=True': Sets this column as the primary key, uniquely identifying each record in the table.
    # - 'autoincrement=True': Automatically increases the value of the 'id' for each new record.



    first_name = db.Column(db.String(50), nullable=False)
    # Defines a column named 'first_name' in the 'users' table.
    # - 'db.String(50)': Specifies that this column will store strings up to 50 characters.
    # - 'nullable=False': Ensures this column cannot be empty; a value must be provided for every record.



    last_name = db.Column(db.String(50), nullable=False)
    # Defines a column named 'last_name' in the 'users' table.
    # - Similar to 'first_name', it stores strings up to 50 characters and is required (cannot be null).



    image_url = db.Column(db.String(255), nullable=True)
    # Defines a column named 'image_url' in the 'users' table.
    # - 'db.String(255)': Specifies that this column will store strings up to 255 characters.
    # - 'nullable=True': This column is optional, so it can store NULL values if no image URL is provided.


    posts = db.relationship("Post", back_populates="user") # One-to-many relationship; one user can have many posts


class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)

    title = db.Column(db.String(200), nullable=False)

    content = db.Column(db.Text())

    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


# Relationship to User model
    user = db.relationship('User', back_populates='posts')
