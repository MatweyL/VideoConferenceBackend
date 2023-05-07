from crud import AbstractCRUD
from database import get_session
from models import Conference


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
