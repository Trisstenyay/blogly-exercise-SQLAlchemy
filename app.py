"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "practice"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()





@app.route("/", methods=["GET"])
def home():
    return redirect("/users")


@app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return render_template("user-list.html", users=users)


@app.route("/users/new", methods=["GET"])
def show_user_create_form():
    return render_template("new-user-form.html")


@app.route("/users/new", methods=["POST"])
def submit_new_user_form():
   first_name = request.form.get("first-name")
   last_name = request.form.get("last-name")
   image_url = request.form.get("image-url")
   user = User(first_name = first_name, last_name = last_name, image_url = image_url)
   db.session.add(user)
   db.session.commit()
   return redirect("/")


@app.route("/users/<int:user_id>/edit", methods=["GET"])
def show_user_edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def submit_user_edit_form(user_id):
   print("------------------------------------------------",user_id)
   first_name = request.form.get("first-name")
   last_name = request.form.get("last-name")
   image_url = request.form.get("image-url")
   user = User.query.get_or_404(user_id)
   print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", user)
   user.first_name = first_name
   user.last_name = last_name
   user.image_url = image_url
   db.session.add(user)
   db.session.commit()
   return redirect("/")



@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete a user by their ID."""
    user = User.query.get_or_404(user_id)  # Find user by ID or return a 404 if not found
    db.session.delete(user)                # Delete the user
    db.session.commit()                    # Commit the deletion
    return redirect("/users")              # Redirect to the list of users after deletion


# Show details about a single user
@app.route("/users/<int:user_id>", methods=["GET"])
def show_user_details(user_id):
    """Display details for a single user, with edit and delete options."""
    user = User.query.get_or_404(user_id)
    return render_template("user-detail.html", user=user)




