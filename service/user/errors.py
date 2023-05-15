from errors import ServiceBaseError


class AuthBaseError(ServiceBaseError):
    pass


class BaseUserError(ServiceBaseError):
    pass


class UsernameAlreadyExistsError(BaseUserError):
    def __init__(self, username: str):
        super(UsernameAlreadyExistsError, self).__init__(f"username '{username}' is already registered")


class UserNotExistingError(BaseUserError):
    def __init__(self, username: str):
        super(UserNotExistingError, self).__init__(f"username '{username}' not existing")


class AuthenticationError(AuthBaseError):
    pass

