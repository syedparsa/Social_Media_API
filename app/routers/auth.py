from fastapi import Depends,status, HTTPException, APIRouter , Response
from fastapi.security import OAuth2PasswordRequestForm

from app import utils

from .. import database, schemas, models,Oauth2
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token)
def user_login (user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'user provided credentails are not correct')

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid user provided credentails')

    access_token = Oauth2.create_access_token(data={'user_id': user.id})
    return {"access_token":access_token, 'token_type':'Bearer'}
