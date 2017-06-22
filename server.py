"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route('/login')
def send_to_login():
    """Sends user to login form """

    return render_template("login_form.html")


@app.route('/process_login_form', methods=["POST"])
def process_login_form():
    """Determines if user/password exists in database."""

    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()


    if user.password == password:
        session['user_id'] = user.user_id
        flash("You're now logged in.")

    else:
        flash("Incorrect login information. Please try again or register.")
    
    return redirect("/")
       

@app.route('/register', methods=["GET"])
def show_register_form():
    """Takes user's info and sends to registration form."""


    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def process_register_form():
    """Receives user's info and redirects to the homepage. """

    email = request.form.get("email")
    password = request.form.get("password")

    if (User.query.filter_by(email=email).first()) is None:
        # check if they exist already. If not, then register them.
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
    else:
        # put up a flash message that tells them they exist and to login
        flash("You're already a user. Please login.")
        # redirect to login

    return redirect("/")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/logout")
def log_user_out():
    """Logs the user out and returns them to homepage"""

    session.clear()
    flash("You're logged out.")
    return redirect("/")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
