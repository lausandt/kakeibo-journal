from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.jwthandler import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from src.core.models import User
from src.core.security import verify_password
from src.schemas.token import Token
from src.schemas.users import (
    UserDatabaseSchema,
    UserOutSchema,
)

router = APIRouter(tags=['login'])


@router.post('/token')
async def login_for_access_token(
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
