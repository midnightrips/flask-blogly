"""Blogly application."""

from flask import Flask, render_template, redirect, request, session, flash
from models import db, connect_db, User, Post, Tag, PostTag
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
db.drop_all()
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
        flash("Please provide both first and last names.") # incorporate flash message into html
        return redirect('/users/new')

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        image=image
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """Show user details."""
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["GET"])
def edit_user(user_id):
    """Show form form for user details."""
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Update user details."""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form.get('first-name')
    user.last_name = request.form.get('last-name')
    user.image = request.form.get('image')

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user from db."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Show form for adding a post."""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('add_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_post(user_id):
    """Create a new post."""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(id.split('_')[1]) for id in request.form.getlist("tags") if id.startswith('tag_')]    
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
        title=request.form.get('title'),
        content=request.form.get('content'),
        user=user,
        tags=tags
    )

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show post."""
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show page for editing a post."""
    post = Post.query.get_or_404(post_id)
    tag_ids = [int(id.split('_')[1]) for id in request.form.getlist("tags") if id.startswith('tag_')]    
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    """Update post."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form.get('title')
    post.content = request.form.get('content')

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete post from db."""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def show_tags():
    """List all tags."""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Show detail about a tag."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_detail.html', tag=tag)

@app.route('/tags/new', methods=['GET'])
def show_new_tag_form():
    """Show form for creating new tag."""
    return render_template('tag_form.html')

@app.route('/tags/new', methods=['POST'])
def add_tag():
    """Create a tag."""
    
    new_tag = Tag(
        name = request.form.get('name')
    )

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit', methods=['GET'])
def show_edit_tag(tag_id):
    """Show form for editing tag."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):
    """Update a tag."""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form.get('name')

    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete a tag from db."""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')