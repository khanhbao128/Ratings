"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
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

@app.route('/register', methods=["GET"])
def register_form():
    """Ask user to register"""

    return render_template('register_form.html')

@app.route('/register', methods=["POST"])
def register_process():
    """Proceess the registration form"""

    email = request.form.get('email')
    password = request.form.get('password')
    user_email=User.query.filter(User.email == email).first()

    if user_email:
        flash('User exists')
        return redirect('/')

    else:
        new_user=User(email=email,
                        password=password)
        db.session.add(new_user)
        db.session.commit()
        flash(' New User added')
        return redirect("/")

@app.route('/login')
def login_form():
    """Show log in form"""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def allow_login():
    """Check to see if the user exists"""
    email = request.form.get('email')
    password = request.form.get('password')

    user=User.query.filter(User.email == email).first()
    user_pword=user.password
    if password == user_pword:
        flash("You are Logged in")
        user_id=user.user_id
        session['user_id']=user_id
        return redirect('/users/<user_id>')
    else:
        flash('Password incorrect')
        return redirect('/login')


@app.route('/logout')
def log_out():
    """Logout the user"""

    session.clear()
    flash("Logged out")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/users/<user_id>')
def user_detail(user_id):
    """Show details of particular User"""

    user = User.query.get(user_id)
    
    return render_template("user.html", user=user)
                                        # score=score)     
@app.route('/movies')
def movie_list():
    """Show list of users."""


    movie = Movie.query.order_by(Movie.title).all()


    return render_template("movie_list.html", movie=movie)

@app.route('/movies/<movie_id>')
def movie_detail(movie_id):
    """Show list of movies"""
    movie = Movie.query.get(movie_id)
    return render_template("movie.html", movie=movie)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
