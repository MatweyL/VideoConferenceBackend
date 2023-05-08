from conference.crud import conference_participant_crud
from conference.errors import UserNotConferenceCreatorError, ConferenceNotExistedError, ConferenceParticipantBannedError
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


def test_enter_to_conference():
    participant = enter_to_conference(conference.id, not_participant_id_1)
    updated_conference_participants = conference_participant_crud.read_all(conference.id)
    is_participant_added = False
    for conference_participant in updated_conference_participants:
        if conference_participant.user_id == participant.user_id:
            is_participant_added = True
            break
    assert is_participant_added


def test_enter_to_not_existing_conference():
    try:
        participant = enter_to_conference('not existed id', not_participant_id_1)
        raise ValueError("This conference not exists")
    except ConferenceNotExistedError:
        pass


def test_ban_conference_participant():
    removed_participant = remove_user_from_conference(conference.id, creator_id, not_participant_id_1)
    assert removed_participant.is_banned
    try:
        participant = enter_to_conference(conference.id, not_participant_id_1)
        raise ValueError("This participant must be removed from conference")
    except ConferenceParticipantBannedError:
        pass
