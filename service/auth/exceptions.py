from exceptions import ServiceBaseException


class UsernameAlreadyExistsError(ServiceBaseException):
    def __init__(self, username: str):
        super(UsernameAlreadyExistsError, self).__init__(f"username '{username}' is already registered")


class UserNotExistingError(ServiceBaseException):
    def __init__(self, username: str):
        super(UserNotExistingError, self).__init__(f"username '{username}' not existing")


class AuthenticationError(ServiceBaseException):
    pass

