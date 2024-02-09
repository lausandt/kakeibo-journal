from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.dependencies import get_current_user
from src.core.jwthandler import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from src.core.models import UserModel
from src.core.security import verify_password
from src.crud import users
from src.schemas.token import Token
from src.schemas.users import (
    UpdateUser,
    UserDatabaseSchema,
    UserInSchema,
    UserOutSchema,
)

router = APIRouter(
    prefix='/users',
    tags=['Users'],  # dependencies=[Depends(oauth2_scheme)]
)


@router.post('/register user', response_model=UserOutSchema)
async def create_user(user: UserInSchema):
    return await users.create_user(user)


@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await UserOutSchema.from_queryset_single(
        UserModel.get(username=form_data.username)
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    db_user = await UserDatabaseSchema.from_queryset_single(
        UserModel.get(username=form_data.username)
    )
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': db_user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')


@router.get('/', response_model=list[UserOutSchema])
async def get_users():
    return await users.get_users()


@router.get('/me', response_model=UserOutSchema)
async def get_user_me(current_user: Annotated[UserModel, Depends(get_current_user)]):
    return await users.get_user_me(id=current_user.id)


@router.patch('/update user', response_model=UserOutSchema)
async def update_user(
    id: int,
    update: UpdateUser,
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    if id == current_user.id:
        return await users.update_user(id=id, update=update)
    raise HTTPException(status_code=403, detail='Forbidden')
