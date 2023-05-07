import datetime
import uuid

from conference.crud import conference_participant_crud
from models import Conference, ConferenceParticipant

creator_id = 1
not_creator_id = 2

conference = Conference(
    id=f'{uuid.uuid4()}{int(datetime.datetime.now().timestamp())}',
    creator_id=creator_id,
)


def test_create_participant():
    participant = ConferenceParticipant(conference_id=conference.id,
                                        user_id=creator_id)
    created_participant = conference_participant_crud.create(participant)
    assert not created_participant.is_banned
    assert created_participant.user_id == creator_id


def test_get_participant():
    participant = conference_participant_crud.read(conference.id, creator_id)
    assert participant.user_id == creator_id


def test_get_participants():
    participant = ConferenceParticipant(conference_id=conference.id,
                                        user_id=not_creator_id)
    created_participant = conference_participant_crud.create(participant)
    participants = conference_participant_crud.read_all(conference.id)
    assert len(participants) > 1


def test_update_participant():
    participant = conference_participant_crud.read(conference.id, creator_id)
    participant.is_banned = True
    updated_participant = conference_participant_crud.update(participant)
    assert updated_participant.is_banned
