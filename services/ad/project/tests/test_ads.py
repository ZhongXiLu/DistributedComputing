

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

                response = self.client.get(f'/ads/{ad}')
                self.assertEqual(response.status_code, 200)

    # def test_personalized_ads(self):
    #     """Test personalized ads for a specific user"""


if __name__ == '__main__':
    unittest.main()
