from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True


class FlaskTests(TestCase):

    def test_index(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form action="/board" id="board-size-form">', html)

    def test_board(self):
        with app.test_client() as client:
            resp = client.get('/board?size=5')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form action="" id="guess-word-form">', html)
            self.assertEqual(session['size'], 5)
            self.assertIn('board', session)

    def test_process_guess(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['size'] = 5
                sess['board'] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]

            resp = client.get('/process-guess?guess=cat')

            self.assertEqual(resp.json['result'], 'ok')

    def test_update_score_1(self):
        with app.test_client() as client:
            resp = client.get('/update-high-score?highscore=50')

            self.assertEqual(resp.json['plays'], 1)
            self.assertEqual(resp.json['highscore'], 50)

    def test_update_score_2(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['plays'] = 20
                sess['highscore'] = 42

            resp = client.get('/update-high-score?highscore=30')

            self.assertEqual(resp.json['plays'], 21)
            self.assertEqual(resp.json['highscore'], 42)
