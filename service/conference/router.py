from fastapi import APIRouter, Depends, HTTPException

from auth.service import get_user_by_jwt_token
from conference.errors import ConferenceNotExistedError, ConferenceAlreadyFinishedError, \
    ConferenceParticipantBannedError, JoiningToConferenceNotAllowedError, UserNotConferenceCreatorError
from conference.schemas import ConferenceDTO, ConferenceParticipantDTO, MinConferenceDTO
import conference.service as conference_service
from models import User

router = APIRouter()


@router.get("/{conference_id}", response_model=ConferenceParticipantDTO, status_code=200)
async def enter_to_conference(conference_id: str, user: User = Depends(get_user_by_jwt_token)):
    try:
        conference_participant = conference_service.enter_to_conference(conference_id, user.id)
    except ConferenceNotExistedError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ConferenceAlreadyFinishedError as e:
        raise HTTPException(status_code=410, detail=str(e))
    except ConferenceParticipantBannedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except JoiningToConferenceNotAllowedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    else:
        return conference_participant


@router.patch("/finish", response_model=ConferenceDTO)
async def finish_conference(conference: MinConferenceDTO, user: User = Depends(get_user_by_jwt_token)):
    try:
        finished_conference = conference_service.finish_conference(conference.id, user.id)
    except UserNotConferenceCreatorError as e:
        return HTTPException(status_code=403, detail=str(e))
    else:
        return finished_conference


@router.patch("/allow_joining", response_model=ConferenceDTO)
async def allow_joining_to_conference(conference: MinConferenceDTO, user: User = Depends(get_user_by_jwt_token)):
    try:
        finished_conference = conference_service.allow_joining_to_conference(conference.id, user.id)
    except UserNotConferenceCreatorError as e:
        return HTTPException(status_code=403, detail=str(e))
    else:
        return finished_conference


@router.patch("/prohibit_joining", response_model=ConferenceDTO)
async def prohibit_joining_to_conference(conference: MinConferenceDTO, user: User = Depends(get_user_by_jwt_token)):
    try:
        finished_conference = conference_service.prohibit_joining_to_conference(conference.id, user.id)
    except UserNotConferenceCreatorError as e:
        return HTTPException(status_code=403, detail=str(e))
    else:
        return finished_conference


@router.post("/", response_model=ConferenceDTO)
async def create_conference(user: User = Depends(get_user_by_jwt_token)):
    conference = conference_service.create_conference(user.id)
    return conference
