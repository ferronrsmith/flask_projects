import os
import unittest
import tempfile
import sys

# hack for getting directory path
sys.path.append(os.getcwd())
import dbapp


class DBTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, dbapp.app.config['DATABASE'] = tempfile.mkstemp()
        dbapp.app.config['TESTING'] = True
        self.app = dbapp.app.test_client()
        dbapp.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(dbapp.app.config['DATABASE'])


    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far' in rv.data

    def login (self, username, password):
        return self.app.post('/login', data=dict(username=username, password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin','password')
        assert 'Invalid username' in rv.data
        rv = self.logout()

    if __name__ == '__main__':
        unittest.main()
