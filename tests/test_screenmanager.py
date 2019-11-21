import unittest

from kivysec.screenmanager import SecureScreenManager, LoginScreen
from kivysec.auth.plain import PlainAuthService
from kivysec.auth.user import anonymous_user
from kivy.uix.screenmanager import ScreenManager, Screen


class SecureScreenTest(unittest.TestCase):

    def setUp(self):
        self.auth_service = PlainAuthService()
        self.sm = SecureScreenManager(self.auth_service)

        self.auth_service.useradd('user', 'pwd', {'name': 'John'})

    def test_type(self):
        self.assertTrue(isinstance(self.sm, ScreenManager))

    def test_login_screen(self):
        self.assertEqual(self.sm.current, 'login')
        self.assertTrue(isinstance(self.sm.current_screen, LoginScreen))

    def test_change_screen(self):
        """Wihout the login, you cannot change the screen"""
        self.sm.add_widget(Screen(name='screen1'))
        self.sm.current = 'screen1'
        self.assertEqual(self.sm.current, 'login')
        self.assertTrue(isinstance(self.sm.current_screen, LoginScreen))

    def test_login_success_backend(self):
        self.sm.add_widget(Screen(name='screen1'))
        self.auth_service.login('user', 'pwd')
        self.sm.current = 'screen1'
        self.assertEqual(self.sm.current, 'screen1')
        self.assertFalse(isinstance(self.sm.current_screen, LoginScreen))

    def test_login_success_frontend(self):
        self.sm.add_widget(Screen(name='screen1'))
        login = self.sm.get_screen('login')
        login.username = 'user'
        login.password = 'pwd'
        login.login(to_screen='screen1')(login)

        self.assertEqual(self.sm.current, 'screen1')
        self.assertFalse(isinstance(self.sm.current_screen, LoginScreen))
        self.assertEqual('', login.password)

    def test_login_fail_frontend(self):
        self.sm.add_widget(Screen(name='screen1'))
        login = self.sm.get_screen('login')
        login.username = 'user'
        login.password = 'wrong'
        login.login(to_screen='screen1')(login)

        self.assertEqual(self.sm.current, 'login')
        self.assertTrue(isinstance(self.sm.current_screen, LoginScreen))
        self.assertEqual('', login.password)

    def test_logout(self):
        self.sm.add_widget(Screen(name='screen1'))
        login = self.sm.get_screen('login')
        login.username = 'user'
        login.password = 'pwd'
        login.login(to_screen='screen1')(login)

        self.sm.current = 'logout'
        self.assertTrue(self.auth_service.current_session.user is
                        anonymous_user)
        self.assertEqual(self.sm.current, 'login')
        self.assertEqual(self.sm.user.username, '')

    def test_user(self):
        screen = Screen(name='screen1')
        self.sm.add_widget(screen)
        login = self.sm.get_screen('login')
        login.username = 'user'
        login.password = 'pwd'
        login.login(to_screen='screen1')(login)

        self.assertEqual(self.sm.user.name, 'John')
        self.assertEqual(screen.user.name, 'John')
