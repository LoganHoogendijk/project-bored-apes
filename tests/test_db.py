# test db.py

from cgi import test
import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

# use an in-memory SQLite database for tests
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        # create two timeline posts
        first_post = TimelinePost.create(
            name='John Doe', 
            email='john@example.com', 
            content='Hello world, I\'m John!'
            )
        assert first_post.id == 1
        first_post_actual = TimelinePost.get_by_id(1)
        assert first_post_actual.id == first_post.id
        assert first_post_actual.name == first_post.name
        assert first_post_actual.email == first_post.email
        assert first_post_actual.content == first_post.content
        assert first_post_actual.created_at == first_post.created_at

        second_post = TimelinePost.create(
            name='Jane Doe', 
            email='jane@example.com', 
            content='Hello world, I\'m Jane!'
            )
        assert second_post.id == 2
        second_post_actual = TimelinePost.get_by_id(2)
        assert second_post_actual.id == second_post.id
        assert second_post_actual.name == second_post.name
        assert second_post_actual.email == second_post.email
        assert second_post_actual.content == second_post.content
        assert second_post_actual.created_at == second_post.created_at
