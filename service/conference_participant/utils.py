from conference_participant.schemas import ConferenceParticipantDTO
from models import ConferenceParticipant


def convert_conference_participant_to_dto(participant: ConferenceParticipant) -> ConferenceParticipantDTO:
    return ConferenceParticipantDTO(
        conference_id=participant.conference_id,
        user_id=participant.user_id,
        is_banned=participant.is_banned,
        created=participant.created,
        role=participant.role
    )