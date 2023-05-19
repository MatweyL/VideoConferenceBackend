import datetime
import uuid
from typing import List

from conference.schemas import ConferenceDTO, ConferenceParticipantDTO, ConferenceFullDTO
from models import Conference, ConferenceParticipant


def convert_conference_to_dto(conference: Conference) -> ConferenceDTO:
    return ConferenceDTO(
        id=conference.id,
        name=conference.name,
        creator_id=conference.creator_id,
        is_finished=conference.is_finished,
        is_joining_allowed=conference.is_joining_allowed,
        created=conference.created,
        finished=conference.finished
    )


def convert_conference_participant_to_dto(participant: ConferenceParticipant, conference: Conference = None) -> ConferenceParticipantDTO:
    conference_dto = convert_conference_to_dto(conference) if conference else None
    return ConferenceParticipantDTO(
        conference_id=participant.conference_id,
        user_id=participant.user_id,
        is_banned=participant.is_banned,
        created=participant.created,
        role=participant.role,
        conference=conference_dto
    )


def convert_to_full_conference_dto(conference: Conference, participants: List[ConferenceParticipant]) -> ConferenceFullDTO:
    return ConferenceFullDTO(
        conference=convert_conference_to_dto(conference),
        participants=[convert_conference_participant_to_dto(participant) for participant in participants]
    )


def generate_conference_id() -> str:
    return f'{uuid.uuid4()}{int(datetime.datetime.now().timestamp())}'
