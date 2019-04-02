

import json
import unittest

from project import db
from project.api.models import Comment
from project.tests.base import BaseTestCase


def add_comment(post_id, user_id, content):
    comment = Comment(post_id=post_id, creator=user_id, content=content)
    db.session.add(comment)
    db.session.commit()
    return comment


class TestCommentService(BaseTestCase):
    """Tests for the Comment Service."""

    def test_add_comment(self):
        """Ensure a new comment can be added to the database."""
        with self.client:
            response = self.client.post(
                '/comments',
                data=json.dumps({
                    'post_id': '0',
                    'user_id': '0',
                    'content': 'Hello World!'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])

    def test_add_comment_invalid_json(self):
        """Ensure error is thrown if the JSON object is invalid."""
        invalid_jsons = [
            {},
            {'post_id': '7kbe9d'},
            {'post_id': '0'},
            {'user_id': '0'},
            {'content': 'Hello World!'},
            {'post_id': '0', 'user_id': 'a'}
        ]
        for invalid_json in invalid_jsons:
            response = self.client.post(
                '/comments',
                data=json.dumps(invalid_json),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_comment(self):
        """Ensure get single comment behaves correctly."""
        comment = add_comment(0, 0, 'Hello World!')
        with self.client:
            response = self.client.get(f'/comments/{comment.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(comment.id, data['data']['id'])
            self.assertEqual(0, data['data']['post_id'])
            self.assertEqual(0, data['data']['creator'])
            self.assertIn('Hello World!', data['data']['content'])
            self.assertIn('success', data['status'])

    def test_single_comment_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        invalid_ids = ['999', 'blah']
        with self.client:
            for invalid_id in invalid_ids:
                response = self.client.get(f'/comments/{invalid_id}')
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 404)
                self.assertIn('Comment does not exist', data['message'])
                self.assertIn('fail', data['status'])

    def test_delete_comment(self):
        """Ensure a comment can get deleted"""
        postId = 0
        userId = 0
        content = "Hello World!"
        comment = add_comment(postId, userId, content)

        with self.client:
            # Check if comment got added
            response = self.client.get(f'/comments/posts/{postId}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(userId in [comment['creator'] for comment in data['data']['comments']])
            self.assertTrue(content in [comment['content'] for comment in data['data']['comments']])

            # Delete comment
            response = self.client.delete(f'/comments/{comment.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('comment was successfully deleted', data['message'])

            # Check if comment got deleted:
            response = self.client.get(f'/comments/posts/{postId}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEquals(len(data['data']['comments']), 0)    # post has no comments now

    def test_get_comments_of_post(self):
        """Ensure get all comments of a post behaves correctly."""
        user_id = 0
        post_id = 0
        other_post_id = 1
        comments = ['Hello World!', 'I love Flask!', 'Some other very interesting comment']
        for comment in comments:
            add_comment(other_post_id, user_id, comment)
            add_comment(post_id, user_id, comment)

        with self.client:
            response = self.client.get(f'/comments/posts/{post_id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            received_comments = data['data']['comments']
            self.assertEqual(len(comments), len(received_comments))

            for index, comment in enumerate(comments):
                self.assertEqual(post_id, received_comments[index]['post_id'])
                self.assertEqual(user_id, received_comments[index]['creator'])
                self.assertEqual(comment, received_comments[index]['content'])

            # Check if no posts are returned for a user who hasn't posted yet
            response = self.client.get(f'/comments/posts/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            received_comments = data['data']['comments']
            self.assertEqual(0, len(received_comments))


if __name__ == '__main__':
    unittest.main()
