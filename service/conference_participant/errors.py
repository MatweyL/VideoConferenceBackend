from errors import ServiceBaseError


class ConferenceParticipantBannedError(ServiceBaseError):
    def __init__(self, user_id: str):
        super(ConferenceParticipantBannedError, self).__init__(f'user with={user_id} banned in this conference')
