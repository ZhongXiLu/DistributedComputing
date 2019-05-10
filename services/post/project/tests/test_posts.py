

import json
import unittest
import requests
from datetime import date

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
                    # 'tags': ['0', '1', '2']
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])

    def test_add_post_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object is invalid."""
        invalid_jsons = [
            {},
            {'creator': 'abc'},
            {'creator': '0'},
            {'content': 'Hello World!'}
        ]
        for invalid_json in invalid_jsons:
            response = self.client.post(
                '/posts',
                data=json.dumps(invalid_json),
                content_type='application/json'
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

    def test_delete_post(self):
        """Ensure a post can get deleted"""
        postToBeDeleted = add_post(0, 'Post to be deleted')

        with self.client:
            # Check if message got added
            response = self.client.get(f'/posts/{postToBeDeleted.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['data']['id'], postToBeDeleted.id)

            # Delete message
            response = self.client.delete(f'/posts/{postToBeDeleted.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])

            # Check if message got deleted
            response = self.client.get(f'/posts/{postToBeDeleted.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Post does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_post_stats(self):
        """Test the post statistics"""
        user_id = 0
        posts = ['Hello World!', 'I love Flask!', 'Some other very interesting post']
        for post in posts:
            add_post(user_id, post)

        with self.client:
            response = self.client.get(f'/posts/stats')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            today = date.today().strftime("%d/%-m/%Y")
            self.assertEqual(data['data']['stats'][today], len(posts))


if __name__ == '__main__':
    unittest.main()
