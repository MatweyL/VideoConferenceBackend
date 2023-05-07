from conference.errors import UserNotConferenceCreatorError
from conference.service import create_conference, get_conference, prohibit_joining_to_conference, \
    allow_joining_to_conference, finish_conference

creator_id = 1
not_creator_id = 2
conference = create_conference(creator_id)


def test_get_conference():
    fetched_conference = get_conference(conference.id)
    assert fetched_conference.id == conference.id


def test_prohibit_joining_to_conference():
    updated_conference = prohibit_joining_to_conference(conference.id, creator_id)
    assert not updated_conference.is_joining_allowed
    try:
        updated_conference = prohibit_joining_to_conference(conference.id, not_creator_id)
    except UserNotConferenceCreatorError:
        pass


def test_allow_joining_to_conference():
    updated_conference = allow_joining_to_conference(conference.id, creator_id)
    assert updated_conference.is_joining_allowed
    try:
        updated_conference = allow_joining_to_conference(conference.id, not_creator_id)
    except UserNotConferenceCreatorError:
        pass


def test_finish_conference():
    try:
        updated_conference = finish_conference(conference.id, not_creator_id)
    except UserNotConferenceCreatorError:
        pass
    finished_conference = finish_conference(conference.id, creator_id)
    assert finished_conference.is_finished
