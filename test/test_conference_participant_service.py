import pprint
from typing import List

from conference.crud import conference_participant_crud
from conference.errors import UserNotConferenceCreatorError, ConferenceNotExistedError, \
    ConferenceParticipantBannedError, JoiningToConferenceNotAllowedError
from conference.schemas import ConferenceParticipantDTO
from conference.service import create_conference, get_conference, prohibit_joining_to_conference, \
    allow_joining_to_conference, finish_conference, enter_to_conference, remove_user_from_conference
from models import ConferenceParticipant

creator_id = 1
participants_ids = [creator_id, 2, 3, 4]
not_participant_id_1 = 5
not_participant_id_2 = 6
conference = create_conference(creator_id)

conference_participants = [conference_participant_crud.create(
    ConferenceParticipant(conference_id=conference.id,
                          user_id=user_id))
    for user_id in participants_ids]


def is_user_participant(participant: ConferenceParticipantDTO, participants: List[ConferenceParticipant]) -> bool:
    for conference_participant in participants:
        if conference_participant.user_id == participant.user_id:
            return True
    return False


def test_enter_to_conference():
    participant = enter_to_conference(conference.id, not_participant_id_1)
    updated_conference_participants = conference_participant_crud.read_all(conference.id)
    is_participant_added = is_user_participant(participant, updated_conference_participants)
    assert is_participant_added
    updated_conference_participant = conference_participant_crud.read(conference.id, participant.user_id)
    assert updated_conference_participant.user_id == participant.user_id


def test_enter_to_not_existing_conference():
    try:
        participant = enter_to_conference('not existed id', not_participant_id_1)
        raise ValueError("This conference not exists")
    except ConferenceNotExistedError:
        pass


def test_ban_conference_participant():
    removed_participant = remove_user_from_conference(conference.id, creator_id, not_participant_id_1)
    assert removed_participant.is_banned
    assert removed_participant.user_id == not_participant_id_1
    try:
        participant = enter_to_conference(conference.id, not_participant_id_1)
        raise ValueError("This participant must be removed from conference")
    except ConferenceParticipantBannedError:
        pass


def test_allowing_prohibiting_joining_to_conference():
    conference_prohibited = prohibit_joining_to_conference(conference.id, creator_id)
    assert not conference_prohibited.is_joining_allowed
    already_joined_participant = enter_to_conference(conference.id, participants_ids[-1])
    print('help', already_joined_participant)
    try:
        participant = enter_to_conference(conference.id, not_participant_id_2)
        raise ValueError("This conference is prohibited from joining")
    except JoiningToConferenceNotAllowedError:
        pass
    conference_allowed = allow_joining_to_conference(conference.id, creator_id)
    assert conference_allowed.is_joining_allowed
    participant = enter_to_conference(conference.id, not_participant_id_2)
    updated_conference_participants = conference_participant_crud.read_all(conference.id)
    assert is_user_participant(participant, updated_conference_participants)
