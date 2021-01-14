from unittest import TestCase

from app import app
from models import db, User

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
        db.session.add(user)
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

    # def test_user_info(self):
    #     with app.test_client() as client:
    #         resp = client.get("/users/1")
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('<p>First Name: TestFirstName</p>', html)

    # def test_new_user(self):
    #     with app.test_client() as client:
    #         d = {"first_name":"Test Person", "last_name":"LAST2TEST"}

    #         resp = client.post("/users/new", data=d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 302)
    #         self.assertIn('Test Person', html)
        
    def test_add_pet(self):
        with app.test_client() as client:
            d = {"id":7, "first_name": "TestDelete", "last_name": "DeleteLast", "image_url": "www.hello.com"}
            resp = client.post("/users/7/delete", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)