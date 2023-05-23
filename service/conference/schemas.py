import datetime
from typing import Optional, List

from schemas import BaseDTOEntity, UserVerboseInfoDTO


class MinConferenceDTO(BaseDTOEntity):
    id: str


class ConferenceToCreateDTO(BaseDTOEntity):
    name: Optional[str]


class ConferenceDTO(BaseDTOEntity):
    id: str
    name: Optional[str]
    creator_id: int
    is_finished: bool
    is_joining_allowed: bool
    finished: Optional[datetime.datetime]


class ConferenceParticipantDTO(BaseDTOEntity):
    conference_id: str
    user_id: int
    is_banned: bool
    role: str
    conference: Optional[ConferenceDTO]
    user_verbose: Optional[UserVerboseInfoDTO]


class ConferenceFullDTO(BaseDTOEntity):
    conference: ConferenceDTO
    participants: List[ConferenceParticipantDTO]
