from errors import ServiceBaseError


class UserNotExistingError(ServiceBaseError):
    def __init__(self, username: str):
        super(UserNotExistingError, self).__init__(f"User with username={username} does not exists")
