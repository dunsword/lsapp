# coding=utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from base.models import User

class SimpleTest(TestCase):
    def test_user_crud(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        
        user = User.objects.create_user('田伯光的刀', 'user2@163.com', 'password')
        self.assertIsNotNone(user, 'user create failed')
        
        u=User.objects.getByEmail(email='user2@163.com')
        self.assertIsNotNone(u, 'user get by email failed')
        self.assertEqual('user2@163.com', u.email, 'wrong email')
        self.assertEqual('田伯光的刀',u.username,'wrong username')
     
    def test_update_user(self):
        user = User.objects.create_user('user12', 'user2@163.com', 'password')
        self.assertIsNotNone(user, 'user create failed')
