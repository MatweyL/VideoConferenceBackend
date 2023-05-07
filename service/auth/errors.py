from exceptions import ServiceBaseException


class AuthBaseException(ServiceBaseException):
    pass


class UsernameAlreadyExistsError(AuthBaseException):
    def __init__(self, username: str):
        super(UsernameAlreadyExistsError, self).__init__(f"username '{username}' is already registered")


class UserNotExistingError(AuthBaseException):
    def __init__(self, username: str):
        super(UserNotExistingError, self).__init__(f"username '{username}' not existing")


class AuthenticationError(AuthBaseException):
    pass

