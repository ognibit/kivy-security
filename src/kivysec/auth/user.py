"""The user for the kivysec module"""
# from datetime import datetime as dt


class KivyUser():
    """User for Kivy purpose"""

    def __init__(self, username, userdata=None):
        """Create a User for the KivySec management.

        Parameters
        ----------
        username: str
            the unique identifier of the user.
        userdata: dict, Optional
            all the user specific data like real name, avatar, etc...
        """
        self.username = username
        userdata = dict(userdata) if userdata else dict()
        for key in userdata:
            setattr(self, key, userdata[key])

        self._userdata = userdata

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name,
                                       self.username,
                                       self._userdata)

    def __str__(self):
        return f"User: {self.username}"

    def __eq__(self, other):
        try:
            return self.username == other.username
        except Exception:
            return False


# the user when there are no user
anonymous_user = KivyUser('', {'is_anonymous': True})


class KivyUserSession():
    """The session started with a login and ended with a logout"""

    def __init__(self, user, start_at=None, live_for=None):
        """

        Parameters
        ----------
        user: KivyUser
        start_at: datetime, optional
            When the session is started. If None, it's now()
        live_for: int, optional
            The number of minutes the session remain alive. None is infinite.
        """
        self.user = user
        # TODO enable the session management
        # start_at = start_at if start_at else dt.now()
        # self.start_at = start_at

    def close(self):
        """End the session and remove the user"""
        self.user = None
