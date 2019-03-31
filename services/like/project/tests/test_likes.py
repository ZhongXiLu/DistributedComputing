

import json
import unittest

from project import db
from project.api.models import Like
from project.tests.base import BaseTestCase


def add_like(post_id, user_id):
    like = Like(post_id=post_id, user_id=user_id)
    db.session.add(like)
    db.session.commit()
    return like


class TestLikeService(BaseTestCase):
    """Tests for the Like Service."""

    def test_add_like(self):
        """Ensure a new like can be added to the database."""
        with self.client:
            response = self.client.post(
                '/likes',
                data=json.dumps({
                    'post_id': '0',
                    'user_id': '0'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])

    def test_add_like_invalid_json(self):
        """Ensure error is thrown if the JSON object is invalid."""
        invalid_jsons = [
            {},
            {'post_id': '7kbe9d'},
            {'post_id': '0'},
            {'user_id': '0'},
            {'post_id': '0', 'user_id': 'a'}
        ]
        for invalid_json in invalid_jsons:
            response = self.client.post(
                '/likes',
                data=json.dumps(invalid_json),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_delete_like(self):
        """Ensure a like can get deleted"""
        postId = 0
        userId = 0
        add_like(postId, userId)

        with self.client:
            # Check if like got added
            response = self.client.get(f'/likes/posts/{postId}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(userId in [like['user_id'] for like in data['data']['likes']])

            # Delete like
            response = self.client.delete(
                f'/likes/posts/{postId}',
                data=json.dumps({'user_id': userId}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('like was successfully removed', data['message'])

            # Check if like got deleted:
            response = self.client.get(f'/likes/posts/{postId}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEquals(len(data['data']['likes']), 0)    # post has no likes now

    def test_get_likes_of_post(self):
        """Ensure get all likes of a post behaves correctly."""
        post_id = 0
        other_post_id = 1
        for user_id in range(10):
            add_like(other_post_id, user_id)
            add_like(post_id, user_id)

        with self.client:
            response = self.client.get(f'/likes/posts/{post_id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            likes = data['data']['likes']
            self.assertEqual(len(likes), 10)

            for user_id in range(10):
                self.assertEqual(post_id, likes[user_id]['post_id'])
                self.assertEqual(user_id, likes[user_id]['user_id'])

            # Make sure there are no tags on a non-existing post
            response = self.client.get(f'/likes/posts/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            likes = data['data']['likes']
            self.assertEqual(0, len(likes))


if __name__ == '__main__':
    unittest.main()
