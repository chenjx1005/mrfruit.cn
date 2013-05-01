#!/usr/bin/env python
#coding=utf-8
import sys
import copy
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import fruit
import unittest
import tempfile

class fruitTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, fruit.app.config['DATABASE'] = tempfile.mkstemp()
        fruit.app.config['TESTING'] = True
        self.app = fruit.app.test_client()
        fruit.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(fruit.app.config['DATABASE'])
	
	def test_empty_db(self):
		rv = self.app.get('/log')
		assert '登陆！我要吃水果' in rv.data
				
	def login(self, username, password):
		return self.app.post('/log', data=dict(
			phone=username,
			stuid=password
		), follow_redirects=True)
	def test_login_logout(self):
		rv = self.login('admin', 'default')
		assert 'register before login~' in rv.data
if __name__ == '__main__':
    unittest.main()