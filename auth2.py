from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from model_req import UserInDB, User, TokenData, Token

# secret key generation command:
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# user database simulation
fake_users_db = {
    "tharushi": {
        "username": "tharushi",
        "full_name": "tharushi dasanayake",
        "email": "tharushi@example.com",
        "hashed_password": "$2b$12$/SbipQ2lPVzBdd/jZnrutucfP4gqY3bWr.wz/7eulsYJGwfXaTPgq",
        "disabled": False,
    }
}

# to hash a password: $2b$12$/SbipQ2lPVzBdd/jZnrutucfP4gqY3bWr.wz/7eulsYJGwfXaTPgq
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# password verification and hashing
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# generate hashed password
def get_password_hash(password):
    return pwd_context.hash(password)

# get user from db
def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)

# authenticate user
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user

# create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credential_exception

    return user

# get current active user
async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


# print(get_password_hash("tharushi123"))  # Example to hash a password