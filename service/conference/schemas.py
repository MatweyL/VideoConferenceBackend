import datetime
from typing import Optional

from schemas import BaseDTOEntity


class ConferenceDTO(BaseDTOEntity):
    id: str
    creator_id: int
    is_finished: bool
    is_joining_allowed: bool
    finished: Optional[datetime.datetime]


class ConferenceParticipantDTO(BaseDTOEntity):
    conference_id: str
    user_id: int
    is_banned: bool
    role: str
