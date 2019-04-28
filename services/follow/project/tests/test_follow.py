import json
import unittest

from project import db
from project.api.models import Follower
from project.tests.base import BaseTestCase


def add_follow(follower_id, followee_id):
    follow = Follower(follower_id=follower_id, followee_id=followee_id)
    db.session.add(follow)
    db.session.commit()
    return follow


class TestFollowService(BaseTestCase):
    """Tests for the Follow Service."""

    def test_add_follow(self):
        """Ensure a new follow can be added to the database."""
        with self.client:
            response = self.client.post(
                '/follow',
                data=json.dumps({
                    'follower_id': 0,
                    'followee_id': 1
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])

    def test_delete_follow(self):
        """Ensure a follower-followee relation can be deleted"""
        add_follow(0, 1)
        with self.client:
            response = self.client.delete(
                f'/follow/0/1',
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(Follower.query.filter_by(follower_id=0).all()), 0)

    def test_get_followers(self):
        add_follow(0, 1)
        with self.client:
            response = self.client.get(
                '/follow/followers/1'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['followers'], [0])

    def test_get_followees(self):
        add_follow(0, 1)
        with self.client:
            response = self.client.get(
                '/follow/followees/0'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['followees'], [1])


if __name__ == '__main__':
    unittest.main()
