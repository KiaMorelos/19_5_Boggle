from unittest import TestCase
from app import app, boggle_game
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
   def setUp(self):
      self.client = app.test_client()
      app.config['TESTING'] = True

   def test_game_view(self):
      """Test that scores and plays are in the session, and expected content is on page"""
      with self.client:
         res = self.client.get('/')
         self.assertIn('board', session)
         self.assertIn(b'Time Remaining', res.data)
         self.assertIn(b'Current Score', res.data)
         self.assertIsNone(session.get('bestscore'))
         self.assertIsNone(session.get('plays'))

   def test_word_not_in_dict(self):
      """Test if word is invalid"""
      self.client.get('/')
      res = self.client.get('/is-word-valid?guess=zodisevil')
      self.assertEqual(res.json['result'], 'not-word')

   def test_is_not_on_board(self):
      """Test if word is not on the board"""
      self.client.get('/')
      res = self.client.get('/is-word-valid?guess=piano')
      self.assertEqual(res.json['result'], 'not-on-board')

   def test_is_word(self):
      """Test that word is valid and on board"""
      with self.client as client:
         with client.session_transaction() as session:
            session['board'] =[
               ["H", "E", "Y", "E", "S" ],
               ["H", "E", "Y", "E", "S" ],
               ["H", "E", "Y", "E", "S" ],
               ["H", "E", "Y", "E", "S" ],
               ["H", "E", "Y", "E", "S" ]
            ]
      res = self.client.get('/is-word-valid?guess=yes')
      self.assertEqual(res.json['result'], 'ok')

   def test_already_played(self):
      """Test if word was already played"""
      with self.client as client:
          with client.session_transaction() as session:
            session['board'] =[
               ["H", "E", "Y", "A", "Y" ],
               ["H", "E", "Y", "A", "Y" ],
               ["H", "E", "Y", "A", "Y" ],
               ["H", "E", "Y", "A", "Y" ],
               ["H", "E", "Y", "A", "Y" ]
            ]
      boggle_game.words_played.append("hey")
      res = self.client.get('/is-word-valid?guess=hey')
      self.assertEqual(res.json['result'], 'already-played')
