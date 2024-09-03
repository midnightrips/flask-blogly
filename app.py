"""Blogly application."""

from flask import Flask, render_template, redirect, request, session, flash
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '12345'
app.config['DEBUG_TB_INTEREPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app_context = app.app_context()
app_context.push()
connect_db(app)
db.create_all()

@app.route('/')
def user_listing():
    """Redirects to list of users in db."""
    return redirect('/users')

@app.route('/users')
def show_users():
    """Shows all users in db."""
    # make each user a link to view the detail page fo the user lcicked on
    # have a link to the add-user form
    users = User.query.all()
    return render_template('/user_listing.html', users=users)

@app.route('/users/new', methods=['GET'])
def show_form():
    """Show form for adding a user to the db."""

    return render_template('new_user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Add user to db."""
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    image = request.form.get('image') or None

    if not first_name or not last_name:
        # Handle the case where required data is missing
        flash("Please provide both first and last names.")
        return redirect('/users/new')

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        image=image
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>')
def show_user_info(id):
    """Show user details."""
    user = User.query.get_or_404(id)
    return render_template('user_detail.html', user=user)

@app.route('/users/<int:id>/edit', methods=["GET"])
def edit_user(id):
    """Show form form for user details."""
    user = User.query.get_or_404(id)
    return render_template('user_edit.html', user=user)

@app.route('/users/<int:id>/edit', methods=['POST'])
def update_user(id):
    """Update user details."""
    user = User.query.get_or_404(id)
    user.first_name = request.form.get('first-name')
    user.last_name = request.form.get('last-name')
    user.image = request.form.get('image')

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>/delete')
def delete_user(id):
    """Delete user from db."""
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')