from errors import ServiceBaseError


class UserNotConferenceCreatorError(ServiceBaseError):
    def __init__(self, user_id: int):
        super(UserNotConferenceCreatorError, self).__init__(f'the user (id: {user_id}) is not the creator of the conference')
