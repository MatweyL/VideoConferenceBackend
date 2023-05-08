from errors import ServiceBaseError


class UserNotConferenceCreatorError(ServiceBaseError):
    def __init__(self, user_id: int):
        super(UserNotConferenceCreatorError, self).__init__(f'the user (id: {user_id}) is not the creator of the conference')


class JoiningToConferenceNotAllowedError(ServiceBaseError):
    def __init__(self):
        super(JoiningToConferenceNotAllowedError, self).__init__('joining to this conference is prohibited')


class ConferenceParticipantBannedError(ServiceBaseError):
    def __init__(self, user_id: str):
        super(ConferenceParticipantBannedError, self).__init__(f'user with={user_id} banned in this conference')


class ConferenceNotExistedError(ServiceBaseError):
    def __init__(self, conference_id: str):
        super(ConferenceNotExistedError, self).__init__(f'conference with id={conference_id} does not exists')

