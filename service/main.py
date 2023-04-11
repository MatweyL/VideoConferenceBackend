from fastapi import FastAPI, HTTPException

from service.crud import CRUDFacade
from service.exceptions import UsernameAlreadyExistsError
from service.models import User

app = FastAPI()
crud = CRUDFacade()


@app.get('/ping')
async def ping():
    return {'message': 'pong'}


@app.post('/users/register', status_code=201, response_model=User)
async def register(user: User):
    try:
        crud_user = crud.crud(User).create(user)
    except UsernameAlreadyExistsError:
        raise HTTPException(status_code=409, detail=f"Username {user.username} already registered")
    else:
        return crud_user

def main():
    pass


if __name__ == "__main__":
    main()
