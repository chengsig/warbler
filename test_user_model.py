"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase, main

from models import db, User, Message, FollowersFollowee
from sqlalchemy.exc import IntegrityError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        FollowersFollowee.query.delete()
        #the following is only related to routes, not for model tests
        #self.client = app.test_client()

        #set up a user at setup so it can be used to other tests
        u = User(
                    email="test@test.com",
                    username="testuser",
                    password="HASHED_PASSWORD",
                    id=99999,
                )
        db.session.add(u)
        u2 = User(
                    email="test2@test.com",
                    username='testuser2',
                    password="HASHED_PASSWORD2",
                    id=88888
        )

        db.session.add(u2)
        db.session.commit()

    def test_user_model(self):
        """Does basic model work?"""
        u = User.query.get(99999)
        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        #the repr method should produce <User #301: hongshaorou, gaochengsi@wustl.edu>
        self.assertEqual(repr(u), f'<User #99999: testuser, test@test.com>')

    def test_is_following(self):
        """Does the is_following work for the user model"""
        u = User.query.get(99999)
        u2 = User.query.get(88888)

        #testing false for is following relationship
        self.assertEqual(u.is_following(u2), False)

    def test_is_following_false(self):
        """Does the is_following work for the user model"""
        u = User.query.get(99999)
        u2 = User.query.get(88888)

        #setting up u99999 to follow u288888:
        ff = FollowersFollowee(followee_id=99999, follower_id=88888)
        db.session.add(ff)
        db.session.commit()
        self.assertEqual(u.is_following(u2), True)

    def test_if_followed_by(self):
        """Does the is_followed_by work for the user model"""
        u = User.query.get(99999)
        u2 = User.query.get(88888)

        #testing should be false before any following happens
        self.assertEqual(u.is_followed_by(u2), False)

    def test_is_followed_by_false(self):
        """Does the is_followed_by work for the user model"""
        u = User.query.get(99999)
        u2 = User.query.get(88888)

        #setting up u99999 to follow u288888:
        ff = FollowersFollowee(followee_id=99999, follower_id=88888)
        db.session.add(ff)
        db.session.commit()
        self.assertEqual(u2.is_followed_by(u), True)
    
    def test_create_returns_valid_vals(self):
        """Does the User.create successfully create a new user given valid credentials?"""

        username = "testuser3"
        email = "test3@test.com"
        password = "HASHED_PASS"
        image_url = "https://i.gifer.com/WyD2.gif"

        User.signup(username, email, password, image_url)
        db.session.commit()

        self.assertEqual(len(User.query.all()), 3)

    def test_create_returns_valid_vals(self):
        """Does the User.create successfully create a new user given valid credentials?"""

        username = "testuser2"
        email = "test3@test.com"
        password = "HASHED_PASS"
        image_url = "https://i.gifer.com/WyD2.gif"

        User.signup(username, email, password, image_url)

        self.assertRaises(IntegrityError, db.session.commit)
    
    # @classmethod
    # def signup(cls, username, email, password, image_url):
    #     """Sign up user.

    #     Hashes password and adds user to system.
    #     """

    #     hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

    #     user = User(
    #         username=username,
    #         email=email,
    #         password=hashed_pwd,
    #         image_url=image_url,
    #     )

    #     db.session.add(user)
    #     return user