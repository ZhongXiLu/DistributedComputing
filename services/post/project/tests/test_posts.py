

import json
import unittest

from project import db
from project.api.models import Post
from project.tests.base import BaseTestCase


def add_post(creator, content):
    post = Post(creator=creator, content=content)
    db.session.add(post)
    db.session.commit()
    return post


class TestPostService(BaseTestCase):
    """Tests for the Post Service."""

    def test_add_post(self):
        """Ensure a new post can be added to the database."""
        with self.client:
            response = self.client.post(
                '/posts',
                data=json.dumps({
                    'creator': '0',
                    'content': 'Hello World!'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])

    def test_add_post_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/posts',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a creator key.
        """
        with self.client:
            response = self.client.post(
                '/posts',
                data=json.dumps({'content': 'Hello World!'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_post(self):
        """Ensure get single post behaves correctly."""
        post = add_post(0, 'Hello World!')
        with self.client:
            response = self.client.get(f'/posts/{post.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(post.id, data['data']['id'])
            self.assertEqual(0, data['data']['creator'])
            self.assertIn('Hello World!', data['data']['content'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/posts/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Post does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_post_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/posts/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Post does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_posts_of_user(self):
        """Ensure get all posts of user behaves correctly."""
        user_id = 0
        posts = ['Hello World!', 'I love Flask!', 'Some other very interesting post']
        for post in posts:
            add_post(user_id, post)
        add_post(1, 'Post from another person')

        with self.client:
            response = self.client.get(f'/posts/user/{user_id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            received_posts = data['data']['posts']
            self.assertEqual(len(posts), len(received_posts))

            for index, post in enumerate(posts):
                self.assertEqual(user_id, received_posts[index]['creator'])
                self.assertEqual(post, received_posts[index]['content'])

            # Check if no posts are returned for a user who hasn't posted yet
            response = self.client.get(f'/posts/user/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            received_posts = data['data']['posts']
            self.assertEqual(0, len(received_posts))

    # TODO: create tests for adding Tags to a post


if __name__ == '__main__':
    unittest.main()
