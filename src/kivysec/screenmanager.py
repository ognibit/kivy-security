"""The ScreenManager extension for enabling the secure mode"""

from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from .auth.user import anonymous_user
from .auth.errors import LoginError


class LoginScreen(Screen):
    """The dedicated screen for the login phase"""
    username = StringProperty()
    password = StringProperty()

    def __init__(self, screenmanager, **kwargs):
        """Docstring
        Parameters
        ----------
        screen_manager: SecureScreenManager
        Returns
        -------
        """
        super().__init__(**kwargs)
        self._screen_manager = screenmanager

    def login(self, to_screen):
        """Try the login with the username and password properties values.
        Parameters
        ----------
        to_screen: str
            the screen name to switch after a corrent login

        Returns
        -------
        login: callable
        """
        _login_screen = self

        def _login(self):
            _login_screen._screen_manager.login(_login_screen.username,
                                                _login_screen.password,
                                                to_screen)
            _login_screen.password = ''

        return _login


class AuthorizedScreen(Screen):
    """A Screen mixin to manage the user events"""

    user = ObjectProperty()

    def on_user(self, instance, value):
        self.update_user(value)

    def update_user(self, user):
        """Callback when the user change.
        Use this method to update all the fields containing
        user information, such as the name o the avatar.

        Parameters
        ----------
        user: KivyUser
            the new user
        """
        pass


class SecureScreenManager(ScreenManager):
    """The ScreenManager extension with the login screen
    and the user management"""

    user = ObjectProperty()

    def __init__(self, auth_service, *args, **kwargs):
        """The screen manager uses the auth_service to login/logut the
        user and check the user data.
        At the start time there's a single screen, the 'login' one.
        When the user has passed the authentication phase, the others
        screen are loaded.
        Parameters
        ----------
        auth_service: the authorization service
        """
        super().__init__(*args, **kwargs)
        self._auth_service = auth_service

        self.login_screen = LoginScreen(self, name='login')
        self.user = self._auth_service.current_session.user
        self.add_widget(self.login_screen)

    def on_current(self, instance, value):
        """Checks the user before change the current screen"""

        if value == 'logout':
            self._auth_service.logout()

        self.user = self._auth_service.current_session.user

        if value != 'login' and self.user is anonymous_user:
            self.current = 'login'
        else:
            super().on_current(instance, value)

    def login(self, username, password, to_screen):
        """Try the login with the username and password properties values.
        Returns
        -------
        user: KivyUser
        to_screen: str
            the screen name to switch after a corrent login
        """
        try:
            user = self._auth_service.login(username, password)
        except LoginError:
            # TODO handle the error showing a message
            user = anonymous_user
        else:
            self.current = to_screen
        finally:
            self.user = self._auth_service.current_session.user

        return user

    def on_user(self, instance, value):
        """Set the user information in all the screens"""
        for screen in self.screens:
            try:
                screen.user = value
            except Exception as e:
                print("An error occurs during the on_user event", e)
