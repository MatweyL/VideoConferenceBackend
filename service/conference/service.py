import datetime
from functools import wraps

from conference.crud import conference_crud
from conference.errors import UserNotConferenceCreatorError
from conference.schemas import ConferenceDTO
from conference.utils import convert_conference_to_conference_dto, generate_conference_id
from models import Conference


def get_conference(conference_id: str) -> ConferenceDTO:
    conference = conference_crud.read(conference_id)
    return convert_conference_to_conference_dto(conference)


def check_is_current_user_conference_creator(func):
    @wraps(func)
    def inner(conference_id: str, user_id: int, *args, **kwargs):
        conference = conference_crud.read(conference_id)
        if conference.creator_id != user_id:
            raise UserNotConferenceCreatorError(user_id)
        return func(conference_id, user_id, *args, **kwargs)

    return inner


def create_conference(creator_id: int) -> ConferenceDTO:
    conference = Conference(
        id=generate_conference_id(),
        creator_id=creator_id
    )
    created_conference = conference_crud.create(conference)
    return convert_conference_to_conference_dto(created_conference)


@check_is_current_user_conference_creator
def finish_conference(conference_id: str, user_id: int) -> ConferenceDTO:
    conference = conference_crud.read(conference_id)
    conference.is_finished = True
    conference.finished = datetime.datetime.now()
    finished_conference = conference_crud.update(conference)
    return convert_conference_to_conference_dto(finished_conference)


def enter_to_conference(conference_id: str, user_id):
    pass


def leave_from_conference(conference_id: str, user_id: int):
    pass


@check_is_current_user_conference_creator
def remove_user_from_conference(conference_id: str, user_id: int):
    pass


@check_is_current_user_conference_creator
def prohibit_joining_to_conference(conference_id: str, user_id: int) -> ConferenceDTO:
    conference = conference_crud.read(conference_id)
    conference.is_joining_allowed = False
    updated_conference = conference_crud.update(conference)
    return convert_conference_to_conference_dto(updated_conference)


@check_is_current_user_conference_creator
def allow_joining_to_conference(conference_id: str, user_id: int) -> ConferenceDTO:
    conference = conference_crud.read(conference_id)
    conference.is_joining_allowed = True
    updated_conference = conference_crud.update(conference)
    return convert_conference_to_conference_dto(updated_conference)
