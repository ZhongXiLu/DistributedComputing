

import json
import unittest
import requests
import io

from project import db
from project.api.models import Ad
from project.tests.base import BaseTestCase


class TestAdService(BaseTestCase):
    """Tests for the Ad Service."""

    def test_add_ad(self):
        """Ensure a new ad can be added to the database."""
        with self.client:
            data = {'category': 'food'}
            data = {key: str(value) for key, value in data.items()}
            data['image'] = (io.BytesIO(b"ad.png"), 'ad.png')
            response = self.client.post(
                '/ads',
                data=data,
                content_type='multipart/form-data'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('Ad was successfully added', data['message'])

    def test_get_ads(self):
        """Ensure get ad from filename behaves correctly"""
        ads = ['ad.png', 'ad2.png', 'ad3.png']
        with self.client:
            for ad in ads:
                data = {'category': 'food'}
                data = {key: str(value) for key, value in data.items()}
                data['image'] = (io.BytesIO(b"ad.png"), ad)
                response = self.client.post(
                    '/ads',
                    data=data,
                    content_type='multipart/form-data'
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)
                self.assertIn('success', data['status'])
                self.assertIn('Ad was successfully added', data['message'])

                response = self.client.get(f'/ads/{ad}')
                self.assertEqual(response.status_code, 200)

    def test_personalized_ads(self):
        """Test personalized ads for a specific user"""
        user_id = 0
        sentence = "Today we went to a Chinese food restaurant, 10/10!"
        with self.client:
            # Add categories
            for category in [{'category': 'sport'}, {'category': 'food'}, {'category': 'games'}]:
                data = category
                data = {key: str(value) for key, value in data.items()}
                data['image'] = (io.BytesIO(b"ad.png"), f"ad_{category['category']}.png")
                response = self.client.post(
                    '/ads',
                    data=data,
                    content_type='multipart/form-data'
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)
                self.assertIn('success', data['status'])
                self.assertIn('Ad was successfully added', data['message'])

            # User posts about 'food'
            response = self.client.post(
                f'/ads/user/{user_id}',
                data=json.dumps({'sentence': sentence}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])

            # Check if user has 'food' category after he posts about 'food'
            response = self.client.get(
                f'/ads/user/{user_id}',
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            ads = data['data']['ads']
            self.assertEqual(len(ads), 1)
            self.assertEqual(ads[0]['category'], "food")   # only food ad(s)


if __name__ == '__main__':
    unittest.main()
