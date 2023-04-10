

class UsernameAlreadyExistsError(Exception):
    def __init__(self, username: str):
        super(UsernameAlreadyExistsError, self).__init__(f"username '{username}' is already registered")


class UserNotExistingError(Exception):
    def __init__(self, username: str):
        super(UserNotExistingError, self).__init__(f"username '{username}' not existing")