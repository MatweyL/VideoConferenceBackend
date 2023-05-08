import datetime
import uuid

from conference.schemas import ConferenceDTO, ConferenceParticipantDTO
from models import Conference, ConferenceParticipant


def convert_conference_to_dto(conference: Conference) -> ConferenceDTO:
    return ConferenceDTO(
        id=conference.id,
        creator_id=conference.creator_id,
        is_finished=conference.is_finished,
        is_joining_allowed=conference.is_joining_allowed,
        created=conference.created,
        finished=conference.finished
    )


def convert_conference_participant_to_dto(participant: ConferenceParticipant) -> ConferenceParticipantDTO:
    return ConferenceParticipantDTO(
        conference_id=participant.conference_id,
        user_id=participant.user_id,
        is_banned=participant.is_banned,
        created=participant.created,
        role=participant.role
    )


def generate_conference_id() -> str:
    return f'{uuid.uuid4()}{int(datetime.datetime.now().timestamp())}'
