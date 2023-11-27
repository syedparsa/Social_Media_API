from datetime import datetime, timedelta
from jose import  JWTError, jwt
from . import schemas
from .schemas import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer



#secret_key
#Algorith
#Expiration Time


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encode_jwt


def verify_access_toke(token:str,credentials_Exceptions):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get('user_id')
        if id is None:
            raise credentials_Exceptions
        Token_data = TokenData(id= str (id))
    except JWTError:
        raise credentials_Exceptions

    return Token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_Exceptions = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'could not validate the credentials', headers={'ww.Authenticate':'Bearer'})

    return verify_access_toke(token,credentials_Exceptions)



