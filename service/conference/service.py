import datetime
from functools import wraps
from typing import List

from conference.crud import conference_crud, conference_participant_crud
from conference.errors import UserNotConferenceCreatorError, ConferenceNotExistedError, \
    JoiningToConferenceNotAllowedError, ConferenceParticipantBannedError, ConferenceAlreadyFinishedError
from conference.schemas import ConferenceDTO, ConferenceParticipantDTO, ConferenceFullDTO
from conference.utils import convert_conference_to_dto, generate_conference_id, convert_conference_participant_to_dto, \
    convert_to_full_conference_dto
from models import Conference, ConferenceParticipant


def get_conference(conference_id: str) -> ConferenceDTO:
    conference = conference_crud.read(conference_id)
    return convert_conference_to_dto(conference)


def get_all_user_conferences(user_id) -> List[ConferenceFullDTO]:
    user_conferences_full = []
    conferences_ids = conference_participant_crud.read_user_conferences(user_id)
    if not conferences_ids:
        conferences = conference_crud.read_all_by_creator_id(user_id)
        return [convert_to_full_conference_dto(conference, []) for conference in conferences]
    for conference_id in conferences_ids:
        conference = conference_crud.read(conference_id)
        participants = conference_participant_crud.read_all(conference_id)
        user_conferences_full.append(convert_to_full_conference_dto(
            conference, participants
        ))
    return user_conferences_full


def check_is_current_user_conference_creator(func):
    @wraps(func)
    def inner(conference_id: str, user_id: int, *args, **kwargs):
        conference = conference_crud.read(conference_id)
        if not conference or conference.creator_id != user_id:
            raise UserNotConferenceCreatorError(user_id)
        return func(conference_id, user_id, *args, **kwargs)

    return inner


def create_conference(creator_id: int) -> ConferenceDTO:
    conference = Conference(
        id=generate_conference_id(),
        creator_id=creator_id,
        created=datetime.datetime.now()
    )
    created_conference = conference_crud.create(conference)
    return convert_conference_to_dto(created_conference)


@check_is_current_user_conference_creator
def finish_conference(conference_id: str, user_id: int) -> ConferenceDTO:
    conference = conference_crud.read(conference_id)
    conference.is_finished = True
    conference.finished = datetime.datetime.now()
    finished_conference = conference_crud.update(conference)
    return convert_conference_to_dto(finished_conference)


def enter_to_conference(conference_id: str, user_id) -> ConferenceParticipantDTO:
    conference = conference_crud.read(conference_id)
    if not conference:
        raise ConferenceNotExistedError(conference_id)
    if conference.is_finished:
        raise ConferenceAlreadyFinishedError(conference_id)

    conference_participant = conference_participant_crud.read(conference_id, user_id)

    if not conference_participant and (conference.is_joining_allowed or conference.creator_id == user_id):
        role = "creator" if conference.creator_id == user_id else "user"
        created_conference_participant = conference_participant_crud.create(ConferenceParticipant(
            conference_id=conference_id,
            user_id=user_id,
            role=role
        ))
        return convert_conference_participant_to_dto(created_conference_participant)
    elif conference_participant and not conference_participant.is_banned:
        return convert_conference_participant_to_dto(conference_participant)
    else:
        if conference_participant and conference_participant.is_banned:
            raise ConferenceParticipantBannedError(user_id)
        raise JoiningToConferenceNotAllowedError()


def leave_from_conference(conference_id: str, user_id: int):
    pass


@check_is_current_user_conference_creator
def remove_user_from_conference(conference_id: str, user_id: int, user_to_remove_id: int) -> ConferenceParticipantDTO:
    conference_participant = conference_participant_crud.read(conference_id, user_to_remove_id)
    conference_participant.is_banned = True
    banned_conference_participant = conference_participant_crud.update(conference_participant)
    return convert_conference_participant_to_dto(banned_conference_participant)


@check_is_current_user_conference_creator
def prohibit_joining_to_conference(conference_id: str, user_id: int) -> ConferenceDTO:
    conference = conference_crud.read(conference_id)
    conference.is_joining_allowed = False
    updated_conference = conference_crud.update(conference)
    return convert_conference_to_dto(updated_conference)


@check_is_current_user_conference_creator
def allow_joining_to_conference(conference_id: str, user_id: int) -> ConferenceDTO:
    conference = conference_crud.read(conference_id)
    conference.is_joining_allowed = True
    updated_conference = conference_crud.update(conference)
    return convert_conference_to_dto(updated_conference)
