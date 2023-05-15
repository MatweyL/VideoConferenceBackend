from schemas import BaseDTOEntity


class ConferenceParticipantDTO(BaseDTOEntity):
    conference_id: str
    user_id: int
    is_banned: bool
    role: str
