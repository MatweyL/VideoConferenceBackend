import datetime
import uuid

from conference.schemas import ConferenceDTO
from models import Conference


def convert_conference_to_conference_dto(conference: Conference) -> ConferenceDTO:
    return ConferenceDTO(
        id=conference.id,
        creator_id=conference.creator_id,
        is_finished=conference.is_finished,
        is_joining_allowed=conference.is_joining_allowed,
        created=conference.created,
        finished=conference.finished
    )


def generate_conference_id() -> str:
    return f'{uuid.uuid4()}{int(datetime.datetime.now().timestamp())}'
