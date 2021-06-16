# -*- coding: utf-8 -*-
"""
Created on Mon May 17 23:07:50 2021

@author: garvi
"""
import unittest
from ip_app import app, db
from ip_app.models import User, Project, Task

from hashlib import md5

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
        u = User(username='something69thatdoesntexist69', email='something69thatdoesntexist69@gmail.com')
        hash_these = md5(u.email.encode('utf-8'))
        
        # God wtf is this?
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/{}?d=identicon&s=128'.format(hash_these.hexdigest())))
    
    def test_user_project_rship(self):
        u = User(username = "Jesus Christ", email = "I_will_be_back_baby@gmail.com")
        
        p = Project(project_name = "Clean my dishes",
                    project_desc = "God also cleans things")
        
        p.author = u
        p.id = u.id
        
        self.assertTrue(p.author.username == u.username and p.author.email == u.email)
        
    def test_project_task_rship(self):
        
        p = Project(project_name = "Clean my dishes",
                    project_desc = "God also cleans things")
        
        
        t = Task(task_name = "Pick up the dishes",
                 assigned_to = "Jesus Christ")
                
        t.project_created_by = p
        p.id = t.id
        
        print ("\n\\n\n\n\n\n")
        print (t)
        
        self.assertTrue(p.project_sub_tasks[0].task_name == t.task_name and p.project_sub_tasks[0].assigned_to == t.assigned_to)
    
if __name__ == '__main__':
    unittest.main(verbosity=2)
    
    
    t = Test()
    t.test_project_task_rship()
