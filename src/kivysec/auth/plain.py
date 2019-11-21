from .user import KivyUser, KivyUserSession, anonymous_user
from .errors import LoginError


class PlainAuthService():
    """The simplest authentication service.

    How to use:

    >>> from kivysec.auth.plain import PlainAuthService
    >>> service = PlainAuthService()
    >>> service
    PlainAuthService()
    >>> service.useradd('user1', 'password1', {'name': 'Real Name'})
    KivyUser('user1', {'name': 'Real Name'})
    >>> service.login('user1', 'password1')
    KivyUser('user1', {'name': 'Real Name'})
    >>> service.current_session.user
    KivyUser('user1', {'name': 'Real Name'})
    >>> service.logout()
    KivyUser('', {'is_anonymous': True})
    >>> service.current_session.user
    KivyUser('', {'is_anonymous': True})
    """

    def __init__(self, *args, **kwargs):
        """Set an empty set of users and starts a anonymous session.
        Parameters
        ----------
        Returns
        -------
        """
        self.passwd = dict()
        self.users = dict()
        self.current_session = KivyUserSession(anonymous_user)

    def __repr__(self):
        class_name = type(self).__name__
        return '{}()'.format(class_name)

    def useradd(self, username, password, userdata=None):
        """Configure the credentials for the user to login.

        Parameters
        ----------
        username: str
            the user identifier
        password: str
            the password for the user (plain text)
        userdata: dict , optional
            a set of attribute to apply to the user, application specific.

        Returns
        -------
        user: KivyUser
        """
        username = str(username)
        password = str(password)
        user = KivyUser(username, userdata)

        self.passwd[username] = password
        self.users[username] = user

        return user

    def login(self, username, password):
        """Match the username and the password and return the KivyUser.

        Parameters
        ----------
        username: str
            the user identifier
        password: str
            the password of the user to check

        Returns
        -------
        user: KivyUser

        Raises
        ------
        LoginError
        """

        # check the input data
        username = str(username)
        password = str(password)

        if username not in self.passwd.keys():
            raise LoginError()

        if password != self.passwd[username]:
            raise LoginError()

        # login ok, get the user
        user = self.users[username]
        # start the session
        self.current_session.close()
        self.current_session = KivyUserSession(user)

        return user

    def logout(self, *args, **kwargs):
        """Close the current session and start a new anonymous session.

        Parameters
        ----------

        Returns
        -------
        anonymous_user: KivyUser
        """
        self.current_session.close()
        self.current_session = KivyUserSession(anonymous_user)

        return self.current_session.user
