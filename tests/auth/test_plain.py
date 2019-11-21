import unittest

from kivysec.auth.plain import PlainAuthService
from kivysec.auth.errors import LoginError
from kivysec.auth.user import anonymous_user


class PlainAuthServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.service = PlainAuthService()

        self.service.useradd('user1', 'password1', {'name': 'John Doe'})
        self.service.useradd('user2', 'password2')
        self.service.useradd('user3', 'password3')

    def test_login(self):
        user = self.service.login('user1', 'password1')
        self.assertEqual(user.username, 'user1')
        self.assertEqual(user.name, 'John Doe')

    def test_login_fail_pass(self):
        with self.assertRaises(LoginError):
            self.service.login('user1', 'wrong')

    def test_login_fail_user(self):
        with self.assertRaises(LoginError):
            self.service.login('user', 'wrong')

    def test_anonymous(self):
        self.assertEqual(anonymous_user, self.service.current_session.user)

    def test_login_session(self):
        user = self.service.login('user1', 'password1')
        self.assertEqual(user, self.service.current_session.user)

    def test_logout(self):
        self.service.login('user1', 'password1')
        user = self.service.logout()
        self.assertEqual(anonymous_user, user)
        self.assertEqual(anonymous_user, self.service.current_session.user)

# TODO add tests for start_at and live_for???
