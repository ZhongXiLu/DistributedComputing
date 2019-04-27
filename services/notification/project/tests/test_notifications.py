

import json
import unittest

from project import db
from project.api.models import Notification
from project.tests.base import BaseTestCase


def add_notification(content, recipient):
    notification = Notification(content=content, recipient=recipient)
    db.session.add(notification)
    db.session.commit()
    return notification


class TestNotificationService(BaseTestCase):
    """Tests for the Notification Service."""

    def test_add_notification(self):
        """Ensure a new notification can be added to the database."""
        with self.client:
            response = self.client.post(
                '/notifications',
                data=json.dumps({
                    'content': 'Hello World!',
                    'recipients': [0, 1, 2]
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('Notifications were successfully created', data['message'])

    def test_add_notification_invalid_json(self):
        """Ensure error is thrown if the JSON object is invalid."""
        invalid_jsons = [
            {},
        ]
        for invalid_json in invalid_jsons:
            response = self.client.post(
                '/notifications',
                data=json.dumps(invalid_json),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_notification(self):
        """Ensure get single notification behaves correctly."""
        notification = add_notification('Hello World!', 0)
        with self.client:
            response = self.client.get(f'/notifications/{notification.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(notification.id, data['data']['id'])
            self.assertIn('Hello World!', data['data']['content'])
            self.assertEqual(0, data['data']['recipient'])
            self.assertIn('success', data['status'])

    def test_single_notification_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        invalid_ids = ['999', 'blah']
        with self.client:
            for invalid_id in invalid_ids:
                response = self.client.get(f'/notifications/{invalid_id}')
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 404)
                self.assertIn('Notification does not exist', data['message'])
                self.assertIn('fail', data['status'])

    def test_delete_comment(self):
        """Ensure a notification can be marked as read"""
        content = "Hello World!"
        recipient = 0
        notification = add_notification(content, recipient)

        with self.client:
            # Check if notification got added
            response = self.client.get(f'/notifications/{notification.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertFalse(data['data']['is_read'])

            # Mark notification as read
            response = self.client.put(f'/notifications/{notification.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('Notification was successfully marked as read', data['message'])

            # Check if notification is read now
            response = self.client.get(f'/notifications/{notification.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['data']['is_read'])    # notification is read

    def test_get_unread_notifications_user(self):
        """Ensure get all unread notifications of a user behaves correctly."""
        recipient = 0
        other_recipient = 1
        contents = ['Hello World!', 'I love Flask!', 'Some other very interesting comment']
        for content in contents:
            add_notification(content, recipient)
            add_notification(content, other_recipient)

        with self.client:
            response = self.client.get(f'/notifications/user/{recipient}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            received_notifications = data['data']['notifications']
            self.assertEqual(len(contents), len(received_notifications))

            for index, content in enumerate(contents):
                self.assertEqual(recipient, received_notifications[index]['recipient'])
                self.assertEqual(content, received_notifications[index]['content'])
                self.assertFalse(received_notifications[index]['is_read'])

                # Mark first notification as read
                if index == 0:
                    self.client.put(f'/notifications/{received_notifications[index]["id"]}')

            response = self.client.get(f'/notifications/user/{recipient}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            received_notifications = data['data']['notifications']
            self.assertEqual(len(contents)-1, len(received_notifications))  # one less notification


if __name__ == '__main__':
    unittest.main()
