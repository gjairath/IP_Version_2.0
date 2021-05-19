# -*- coding: utf-8 -*-
"""
Created on Mon May 17 23:07:50 2021

@author: garvi
"""
import unittest
from ip_app import app, db
from ip_app.models import User

class Test(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hash(self):
        u = User(username='mias sister')
        u.set_password('Cats')
        self.assertFalse(u.check_password('shark'))
        self.assertTrue(u.check_password('Cats'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
