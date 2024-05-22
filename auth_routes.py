from fastapi import HTTPException, APIRouter, status, Depends
from models import User
from database import session, engine
from schema import SigupModel, LoginModel
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

auth_router = APIRouter(
    prefix='/auth',
)


session = session(bind=engine)


@auth_router.get('/')
async def welcome():
    return {'message' :'This is page signup'}

@auth_router.post('/signup/', status_code=status.HTTP_200_OK)
async def singup(user: SigupModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User with email {user.email} already exists'
        )
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User with username {user.username} already exists'
        )
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )
    session.add(new_user)
    session.commit()
    data = {
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'is_staff': new_user.is_staff,
        'is_active': new_user.is_active,
    }
    response = {
        'success': True,
        'code': 200,
        'message': 'User successfully created',
        'data': data
    }
    return response

@auth_router.post('/login/', status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username and check_password_hash(db_username.password, user.password):
        access_token = Authorize.create_access_token(subject=db_username.username)
        refresh_token = Authorize.create_refresh_token(subject=db_username.username)
        return {
            'code': 200,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid username or password')
