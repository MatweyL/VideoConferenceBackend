import datetime
import uuid

from conference.crud import conference_crud
from models import Conference

conference = Conference(
    id=f'{uuid.uuid4()}{int(datetime.datetime.now().timestamp())}',
    creator_id=1,
)


class TestUserCRUD:
    """ test case for conference crud operations """
    def test_create_conference(self):
        created_conference = conference_crud.create(conference)
        assert not created_conference.is_finished
        assert created_conference.is_joining_allowed
        assert created_conference.id == conference.id

    def test_update_conference(self):
        conference.is_joining_allowed = False
        updated_conference = conference_crud.update(conference)
        assert not updated_conference.is_joining_allowed
        conference.is_finished = True
        conference.finished = datetime.datetime.now().now()
        updated_conference = conference_crud.update(conference)
        assert not updated_conference.is_joining_allowed
        assert updated_conference.is_finished
        assert updated_conference.finished
