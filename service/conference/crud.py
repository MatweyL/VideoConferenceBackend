from typing import List

from crud import AbstractCRUD
from database import get_session
from models import Conference, ConferenceParticipant


class ConferenceCRUD(AbstractCRUD):
    def create(self, conference: Conference) -> Conference:
        with get_session() as session:
            session.add(conference)
            session.commit()
            return conference

    def read(self, conference_id: str, *args, **kwargs) -> Conference:
        with get_session() as session:
            conference = session.query(Conference).filter(Conference.id == conference_id).first()
            return conference

    def update(self, updated_conference: Conference, *args, **kwargs):
        with get_session() as session:
            conference = self.read(updated_conference.id)
            conference.is_joining_allowed = updated_conference.is_joining_allowed
            conference.is_finished = updated_conference.is_finished
            conference.finished = updated_conference.finished
            session.add(conference)
            session.commit()
            return conference

    def delete(self, pk, *args, **kwargs):
        pass


conference_crud = ConferenceCRUD()


class ConferenceParticipantCRUD(AbstractCRUD):
    def create(self, participant: ConferenceParticipant) -> ConferenceParticipant:
        with get_session() as session:
            session.add(participant)
            session.commit()
            return participant

    def read(self, conference_id: str, user_id: int, *args, **kwargs) -> ConferenceParticipant:
        with get_session() as session:
            participant = session.query(ConferenceParticipant).filter(
                ConferenceParticipant.conference_id == conference_id,
                ConferenceParticipant.user_id == user_id
            ).first()
            return participant

    def read_all(self, conference_id: str) -> List[ConferenceParticipant]:
        with get_session() as session:
            participants = session.query(ConferenceParticipant).filter(
                ConferenceParticipant.conference_id == conference_id
            ).all()
            return participants

    def update(self, updated_participant: ConferenceParticipant, *args, **kwargs) -> ConferenceParticipant:
        with get_session() as session:
            participant = self.read(updated_participant.conference_id, updated_participant.user_id)
            participant.is_banned = updated_participant.is_banned
            session.add(participant)
            session.commit()
            return participant

    def delete(self, pk, *args, **kwargs):
        pass


conference_participant_crud = ConferenceParticipantCRUD()
