

import json
import unittest
import requests

from project import db
from project.api.models import BadWord
from project.tests.base import BaseTestCase


def add_bad_word(word):
    bad_word = BadWord(word=word)
    db.session.add(bad_word)
    db.session.commit()
    return bad_word


class TestAntiCyberbullyingService(BaseTestCase):
    """Tests for the Anti Cyberbullying Service."""

    def test_add_bad_word(self):
        """Ensure a new bad word can be added to the database."""
        with self.client:
            response = self.client.post(
                '/anti_cyberbullying',
                data=json.dumps({
                    'words': ['badword']
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])

    def test_add_bad_word_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object is invalid."""
        invalid_jsons = [
            # TODO ?
        ]
        for invalid_json in invalid_jsons:
            response = self.client.post(
                '/anti_cyberbullying',
                data=json.dumps(invalid_json),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_bad_words(self):
        """Ensure get all bad words behaves correctly."""
        bad_words = ['badword', 'otherbadword', 'anotherbadword']
        for word in bad_words:
            add_bad_word(word)

        with self.client:
            response = self.client.get('/anti_cyberbullying')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            received_words = data['data']['words']
            self.assertEqual(len(bad_words), len(received_words))

            for index, word in enumerate(bad_words):
                self.assertEqual(word, received_words[index]['word'])

    def test_contains_bad_word(self):
        """Test sentences with/without bad words"""

        good_sentence = "Hello World!"
        bad_sentence = "This sentence contains a BADWORD"

        with self.client:
            for sentence in [good_sentence, bad_sentence]:
                response = self.client.post(
                    '/anti_cyberbullying/contains_bad_word',
                    data=json.dumps({'sentence': sentence}),
                    content_type='application/json'
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)
                self.assertFalse(data['result'])

            # Add new bad word to database
            add_bad_word('badword')

            response = self.client.get('/anti_cyberbullying')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            print(data['data']['words'])

            response = self.client.post(
                '/anti_cyberbullying/contains_bad_word',
                data=json.dumps({'sentence': good_sentence}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertFalse(data['result'])

            response = self.client.post(
                '/anti_cyberbullying/contains_bad_word',
                data=json.dumps({'sentence': bad_sentence}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['result'])     # sentence contains a bad word


if __name__ == '__main__':
    unittest.main()
