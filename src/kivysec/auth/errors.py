"""The excetions that can occure during the authentication phase"""


class LoginError(Exception):
    """Wrong Username or password"""
    pass


class AuthenticationRequiredError(Exception):
    """The user need to login"""
    pass
