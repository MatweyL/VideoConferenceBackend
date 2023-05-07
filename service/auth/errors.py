from errors import ServiceBaseError


class AuthBaseError(ServiceBaseError):
    pass


class UsernameAlreadyExistsError(AuthBaseError):
    def __init__(self, username: str):
        super(UsernameAlreadyExistsError, self).__init__(f"username '{username}' is already registered")


class UserNotExistingError(AuthBaseError):
    def __init__(self, username: str):
        super(UserNotExistingError, self).__init__(f"username '{username}' not existing")


class AuthenticationError(AuthBaseError):
    pass

