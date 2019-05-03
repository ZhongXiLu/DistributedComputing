import json
import unittest

from project import db
from project.api.models import Message
from project.tests.base import BaseTestCase


class TestMessageService(BaseTestCase):
    def test_add_message(self):
        """Ensure a new message can be added to the database"""
        with self.client:
            response = self.client.post(
                '/message',
                data=json.dumps({
                    'contents': 'message contents',
                    'sender_id': 1,
                    'receiver_id': 2,
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
#
#
# def add_friend(friend_initiator_id, friend_acceptor_id):
#     friend = Friend(friend_initiator_id=friend_initiator_id, friend_acceptor_id=friend_acceptor_id)
#     db.session.add(friend)
#     db.session.commit()
#     return friend
#
#
# def accept_friend(friend_initiator_id, friend_acceptor_id):
#     friend = Friend.query.filter_by(
#         friend_initiator_id=friend_initiator_id, friend_acceptor_id=friend_acceptor_id).first()
#     friend.is_accepted = True
#     db.session.commit()
#     return friend
#
#
# class TestFriendService(BaseTestCase):
#     """Tests for the Friend Service."""
#
#     def test_add_friend(self):
#         """Ensure a new friend request can be added to the database."""
#         with self.client:
#             response = self.client.post(
#                 '/friend/request',
#                 data=json.dumps({
#                     'friend_initiator_id': 0,
#                     'friend_acceptor_id': 1
#                 }),
#                 content_type='application/json',
#             )
#             data = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 201)
#             self.assertIn('success', data['status'])
#
#     def test_add_duplicate_friend(self):
#         """Ensure no duplicate friends can be added."""
#         add_friend(0, 1)
#         with self.client:
#             response = self.client.post(
#                 '/friend/request',
#                 data=json.dumps({
#                     'friend_initiator_id': 1,
#                     'friend_acceptor_id': 0
#                 }),
#                 content_type='application/json',
#             )
#             data = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 400)
#             self.assertIn('fail', data['status'])
#
#     def test_accept_friend(self):
#         """Ensure a friend request can be accepted."""
#         add_friend(0, 1)
#         with self.client:
#             response = self.client.put(
#                 '/friend/accept',
#                 data=json.dumps({
#                     'friend_initiator_id': 0,
#                     'friend_acceptor_id': 1
#                 }),
#                 content_type='application/json',
#             )
#             data = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 200)
#             self.assertIn('success', data['status'])
#             self.assertEqual(Friend.query.filter_by(is_accepted=True).count(), 1)
#
#     def test_delete_friend(self):
#         """Ensure a friend-friendee relation can be deleted"""
#         add_friend(0, 1)
#         with self.client:
#             response = self.client.delete(
#                 f'/friend/1/0',
#             )
#             self.assertEqual(response.status_code, 200)
#             self.assertEqual(Friend.query.filter_by(friend_initiator_id=0).count(), 0)
#
#     def test_get_friends(self):
#         add_friend(0, 1)
#         accept_friend(0, 1)
#         add_friend(0, 2)
#         accept_friend(0, 2)
#         add_friend(2, 1)
#         accept_friend(2, 1)
#         with self.client:
#             response = self.client.get(
#                 '/friend/1'
#             )
#             data = json.loads(response.data.decode())
#             print(data)
#             self.assertEqual(response.status_code, 200)
#             self.assertEqual(sorted(data['friends']), sorted([0, 2]))
#
#     def test_get_friends_not_accepted(self):
#         add_friend(0, 1)
#         with self.client:
#             response = self.client.get(
#                 '/friend/1'
#             )
#             data = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 200)
#             self.assertEqual(data['friends'], [])
#
#
# if __name__ == '__main__':
#     unittest.main()
