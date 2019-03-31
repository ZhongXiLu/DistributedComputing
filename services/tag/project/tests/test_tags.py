

import json
import unittest

from project import db
from project.api.models import Tag
from project.tests.base import BaseTestCase


def add_tag(post_id, user_id):
    tag = Tag(post_id=post_id, user_id=user_id)
    db.session.add(tag)
    db.session.commit()
    return tag


class TestTagService(BaseTestCase):
    """Tests for the Tag Service."""

    def test_add_tag(self):
        """Ensure a new tag can be added to the database."""
        with self.client:
            response = self.client.post(
                '/tags',
                data=json.dumps({
                    'post_id': '0',
                    'user_ids': ['0', '1', '2']
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])

    def test_add_tag_invalid_json(self):
        """Ensure error is thrown if the JSON object is invalid."""
        invalid_jsons = [
            {},
            {'post_id': '7kbe9d'},
            {'post_id': '0'},
            {'post_id': '0', 'user_ids': ['a', 'b', 'c']}
        ]
        for invalid_json in invalid_jsons:
            response = self.client.post(
                '/tags',
                data=json.dumps(invalid_json),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_tags_of_post(self):
        """Ensure get all tags of a post behaves correctly."""
        post_id = 0
        other_post_id = 1
        for user_id in range(10):
            add_tag(other_post_id, user_id)
            add_tag(post_id, user_id)

        with self.client:
            response = self.client.get(f'/tags/posts/{post_id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            tags = data['data']['tags']
            self.assertEqual(len(tags), 10)

            for user_id in range(10):
                self.assertEqual(post_id, tags[user_id]['post_id'])
                self.assertEqual(user_id, tags[user_id]['user_id'])

            # Make sure there are no tags on a non-existing post
            response = self.client.get(f'/tags/posts/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            tags = data['data']['tags']
            self.assertEqual(0, len(tags))


if __name__ == '__main__':
    unittest.main()
