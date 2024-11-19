"""Blogly application."""  # Short description of the application.

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Post, db, connect_db
# Import necessary modules and classes:
# - `Flask`: used to create the web application.
# - `redirect`: used to send the user to a different route.
# - `render_template`: renders HTML templates for the user.
# - `request`: handles incoming HTTP request data (e.g., form submissions).
# - `DebugToolbarExtension`: adds debugging features to the Flask app.
# - `User`: the database model for users.
# - `db`: the SQLAlchemy database instance.
# - `connect_db`: a helper function to set up the database connection.




app = Flask(__name__)  # Create an instance of the Flask application.



# Configuration for the SQLAlchemy database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'  # Database connection string.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disables a feature that unnecessarily tracks object changes (not needed, saves resources).
app.config['SQLALCHEMY_ECHO'] = True  # Logs all SQL queries to the console (useful for debugging).
app.config["SECRET_KEY"] = "practice"  # Secret key used for session management and security.
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False  # Prevents Debug Toolbar from intercepting redirects.
debug = DebugToolbarExtension(app)  # Attach the Debug Toolbar to the application.




with app.app_context():
    connect_db(app)  # Establishes the connection between the app and the database.
    db.create_all()  # Creates all database tables defined in the `models.py` file.








# Define application routes below.

@app.route("/", methods=["GET"])  # Route for the homepage.
def home():
    """Redirects to the user list page."""
    return redirect("/users")  # Automatically send users to the `/users` route.








@app.route("/users", methods=["GET"])  # Route to display all users.
def get_all_users():
    """Fetches all users from the database and displays them."""
    users = User.query.all()  # Retrieve all users from the database.
    return render_template("user-list.html", users=users)  # Render the user list template with the retrieved users.








@app.route("/users/new", methods=["GET"])  # Route to show the "Create New User" form.
def show_user_create_form():
    """Displays a form to create a new user."""
    return render_template("new-user-form.html")  # Render the form template.








@app.route("/users/new", methods=["POST"])  # Route to handle the submission of the "Create New User" form.
def submit_new_user_form():
    """Processes the form submission and adds a new user to the database."""
    first_name = request.form.get("first-name")  # Extract the first name from the form.
    last_name = request.form.get("last-name")  # Extract the last name from the form.
    image_url = request.form.get("image-url")  # Extract the image URL from the form.
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)  # Create a new User instance.
    db.session.add(user)  # Add the new user to the database session.
    db.session.commit()  # Commit the changes to save the new user.
    return redirect("/")  # Redirect to the homepage.








@app.route("/users/<int:user_id>/edit", methods=["GET"])  # Route to show the "Edit User" form.
def show_user_edit_form(user_id):
    """Displays a form to edit an existing user's information."""
    user = User.query.get_or_404(user_id)  # Fetch the user by ID or return a 404 error if not found.
    return render_template("edit-user.html", user=user)  # Render the form template with the user's data.








@app.route("/users/<int:user_id>/edit", methods=["POST"])  # Route to handle the submission of the "Edit User" form.
def submit_user_edit_form(user_id):
    """Processes the form submission and updates an existing user's information."""
    first_name = request.form.get("first-name")  # Extract the updated first name from the form.
    last_name = request.form.get("last-name")  # Extract the updated last name from the form.
    image_url = request.form.get("image-url")  # Extract the updated image URL from the form.
    user = User.query.get_or_404(user_id)  # Fetch the user by ID or return a 404 error if not found.
    user.first_name = first_name  # Update the user's first name.
    user.last_name = last_name  # Update the user's last name.
    user.image_url = image_url  # Update the user's image URL.
    db.session.add(user)  # Add the updated user to the database session.
    db.session.commit()  # Commit the changes to save the updated user.
    return redirect("/")  # Redirect to the homepage.







@app.route("/users/<int:user_id>/delete", methods=["POST"])  # Route to handle deleting a user.
def delete_user(user_id):
    """Deletes a user by their ID."""
    user = User.query.get_or_404(user_id)  # Fetch the user by ID or return a 404 error if not found.
    db.session.delete(user)  # Delete the user from the database session.
    db.session.commit()  # Commit the changes to remove the user from the database.
    return redirect("/users")  # Redirect to the user list page.








@app.route("/users/<int:user_id>", methods=["GET"])  # Route to show details for a single user.
def show_user_details(user_id):
    """Displays details about a single user, with options to edit or delete."""
    user = User.query.get_or_404(user_id)  # Fetch the user by ID or return a 404 error if not found.
    return render_template("user-detail.html", user=user)  # Render the user details template with the user's data.








@app.route("/users/<int:user_id>/posts/new", methods=["GET"])  # Route to show the "new post" form.
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    """Displays a form to create a new post."""
    return render_template("new-post-form.html", user=user)  # Render the form template.







@app.route("/users/<int:user_id>/posts/new", methods=["POST"])  # Handles form submission for adding a new post.
def submit_post_form(user_id):
    """Processes the form submission and adds a new post for a user."""
    user = User.query.get_or_404(user_id)  # Fetch the user or return a 404 error if not found.

    # Extract data from the form
    title = request.form.get("title")  # Get the post's title from the form.
    content = request.form.get("content")  # Get the post's content from the form.

    # Create and save the new post
    new_post = Post(title=title, content=content, user=user)  # Create a new Post instance.
    db.session.add(new_post)  # Add the new post to the database session.
    db.session.commit()  # Commit the changes to save the post.

    return redirect(f"/users/{user_id}")  # Redirect to the user's detail page.








@app.route("/posts/<int:post_id>", methods=["GET"])  # Route to display a single post's details.
def show_post(post_id):
    """Displays details about a specific post."""
    post = Post.query.get_or_404(post_id)  # Fetch the post by ID or return a 404 error if not found.
    return render_template("post-detail.html", post=post)  # Render the post details template.









@app.route("/posts/<int:post_id>/edit", methods=["GET"])  # Route to show the "Edit Post" form.
def show_edit_post_form(post_id):
    """Displays a form to edit a post."""
    post = Post.query.get_or_404(post_id)  # Fetch the post by ID or return a 404 error if not found.
    return render_template("edit-post-form.html", post=post)  # Render the edit post form template.

@app.route("/posts/<int:post_id>/edit", methods=["POST"])  # Route to handle editing a post.
def submit_edit_post_form(post_id):
    """Processes the form submission and updates a post."""
    post = Post.query.get_or_404(post_id)  # Fetch the post by ID or return a 404 error if not found.

    # Update the post's data with form input
    post.title = request.form.get("title")  # Update the post's title.
    post.content = request.form.get("content")  # Update the post's content.

    db.session.add(post)  # Add the updated post to the database session.
    db.session.commit()  # Commit the changes to save the updated post.

    return redirect(f"/posts/{post.id}")  # Redirect to the post's detail page.







@app.route("/posts/<int:post_id>/delete", methods=["POST"])  # Route to handle deleting a post.
def delete_post(post_id):
    """Deletes a post by its ID."""
    post = Post.query.get_or_404(post_id)  # Fetch the post by ID or return a 404 error if not found.
    db.session.delete(post)  # Delete the post from the database session.
    db.session.commit()  # Commit the changes to remove the post from the database.
    return redirect(f"/users/{post.user_id}")  # Redirect to the user's detail page.



