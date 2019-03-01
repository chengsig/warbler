"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase, main

from models import db, User, Message, FollowersFollowee, Like
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
bcrypt = Bcrypt()

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        FollowersFollowee.query.delete()
        #the following is only related to routes, not for model tests
        #self.client = app.test_client()
        hashed_pwd = bcrypt.generate_password_hash("HASHED-PASSWORD").decode('UTF-8')
        #set up a user at setup so it can be used to other tests
        u = User(
                    email="test@test.com",
                    username="testuser",
                    password=hashed_pwd,
                    id=99999,
        )

        u2 = User(
                    email="test2@test.com",
                    username='testuser2',
                    password="HASHED_PASSWORD2",
                    id=88888
        )

        m1 = Message(
                    id=99999,
                    text="Hello",
                    user_id=99999,
        )
        
        m2 = Message(
                    id=88888,
                    text="Goodbye",
                    user_id=88888,
        )

        db.session.add(u)
        db.session.add(u2)
        db.session.add(m1)
        db.session.add(m2)
        db.session.commit()

    def test_message_model(self):
        """Does basic model work?"""
        u = User.query.get(99999)
        m = Message.query.get(99999)
        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 1)
        #the repr method should produce <User #301: hongshaorou, gaochengsi@wustl.edu>
        self.assertEqual(repr(m), f'<Message #99999: Hello, Owner: 99999>')

    def test_is_liked_by_false(self):
        """Does the is_liked_by work for the message model"""
        m1 = Message.query.get(99999)
        u1 = User.query.get(99999)

        #testing false for is following relationship
        self.assertEqual(m1.is_liked_by(u1), False)

    def test_is_liked_by_true(self):
        """Does the is_liked_by work for the message model"""
        m1 = Message.query.get(99999)
        u2 = User.query.get(88888)

        # setting up u2 to like m1:
        like = Like(user_id=88888, mes_id=99999)
        db.session.add(like)
        db.session.commit()
        self.assertEqual(m1.is_liked_by(u2), True)