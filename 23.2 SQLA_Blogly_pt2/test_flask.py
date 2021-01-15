from unittest import TestCase
from app import app
from models import db, User
import pdb

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UsersViewsTestCase(TestCase):

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="TestFirstName", last_name="TESTLastName", image_url="www.google.com")
        user1 = User(first_name="TestFirstName1", last_name="TESTLastName1", image_url="www.google.com")
        db.session.add(user)
        db.session.add(user1)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    """Test views for Users."""
    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstName', html)

    def test_user_info(self):
        with app.test_client() as client:
            resp = client.get("/users/6")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>First Name: TestFirstName</p>', html)

    def test_new_user(self):
        with app.test_client() as client:
            test_d = {"first_name":"Test Person", "last_name":"LAST2TEST", "image_url":"test.com"}
            # breakpoint()
            resp = client.post("/users/new", data=test_d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Person', html)
        
    def test_del_user(self):
        with app.test_client() as client:
            resp = client.post("/users/7/delete", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)