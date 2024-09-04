from unittest import TestCase
from app import app
from flask import session
from models import db, User, Post

class FlaskTests(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()

    def test_homepage(self):
        with app.test_client() as client:
            
            res = client.get('/')

            self.assertEqual(res.status_code, 302)

    def test_show_users(self):
        with app.test_client() as client:

            res = client.get('/users')

            self.assertEqual(res.status_code, 200)

    def test_new_user_form(self):
        with app.test_client() as client:

            res = client.get('/users/new')

            self.assertEqual(res.status_code, 200)

    def test_add_user(self):
        """Test adding a user to the database."""
        with self.client as client:
            res = client.post('/users/new', data={
                'first-name': 'John',
                'last-name': 'Doe',
                'image': 'http://example.com/image.jpg'
            })
            self.assertEqual(res.status_code, 302)
            self.assertEqual(User.query.count(), 1)
            user = User.query.first()
            self.assertEqual(user.first_name, 'John')
            self.assertEqual(user.last_name, 'Doe')
            self.assertEqual(user.image, 'http://example.com/image.jpg')

    def test_find_user(self):
        """Test searching for a nonexistent user."""
        with self.client as client:
            res = client.get('/users/1')

            self.assertEqual(res.status_code, 404)

    def test_delete_user(self):
        """Test deleting a user from the database."""
        with self.client as client:
            res = client.post('/users/new', data={
                'first-name': 'John',
                'last-name': 'Doe',
                'image': 'http://example.com/image.jpg'
            })
            res = client.post('/users/1/delete')
            self.assertEqual(res.status_code, 302)
            self.assertEqual(User.query.get(1), None)

    def test_show_post_form(self):
        """Test accessing the form to add a new post."""
        with self.client as client:
            res = client.post('/users/new', data={
                'first-name': 'John',
                'last-name': 'Doe',
                'image': 'http://example.com/image.jpg'
            })
            res = self.client.get(f'/users/1/posts/new')
            self.assertEqual(res.status_code, 200)
    