from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.dependencies import get_current_user
from src.core.jwthandler import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from src.core.models import User
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


@router.post('/register', response_model=UserOutSchema)
async def create_user(user: UserInSchema):  # type: ignore
    return await users.create_user(user)


@router.get('/', response_model=list[UserOutSchema])
async def get_users():
    return await users.get_users()


@router.get('/me', response_model=UserOutSchema)
async def get_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    return await users.get_user(id=current_user.id)


@router.get('/user by id/{id}', response_model=UserOutSchema)
async def get_user_by_id(
    id: int, current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.superuser:
        return await users.get_user(id=id)
    raise HTTPException(status_code=403, detail='Not authorized')


@router.patch('/update me', response_model=UserOutSchema)
async def update_user(
    update: UpdateUser,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await users.update_user(id=current_user.id, update=update)


@router.delete(
    '/remove user/{id}',
    response_model=dict[str, int],
)
async def remove_user(
    id: int, current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.superuser:
        db_user = await users.get_user(id=id)
        if db_user:
            return await users.delete_user(id)
        raise HTTPException(status_code=404, detail=f'User {id} not found')
    raise HTTPException(status_code=403, detail='Not authorized to delete')


@router.post('/token')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await UserOutSchema.from_queryset_single(
        User.get(username=form_data.username)
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    db_user = await UserDatabaseSchema.from_queryset_single(
        User.get(username=form_data.username)
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
