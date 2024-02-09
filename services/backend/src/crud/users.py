"""
collection of user crud function. Meaning the focus is on the user
There are no HTTP exceptions and other checks here, this done in the router
The functions are not commented on as they are typed and relatively simple
"""


from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.core.models import SuperUser, UserModel
from src.core.security import get_password_hash

# from src.schemas.entries import EntryOutSchema, RegularEntryOutSchema
from src.schemas.users import (
    UpdateUser,
    UserDatabaseSchema,
    UserInSchema,
    UserOutSchema,
)


async def get_user_me(*, id: int) -> UserOutSchema:
    return await UserOutSchema.from_queryset_single(UserModel.get(id=id))


async def get_users() -> list[UserOutSchema]:
    return await UserOutSchema.from_queryset(UserModel.all())


# async def get_entries_user(username: str):
#     user = await UserDatabaseSchema.from_queryset_single(User.get(username=username))
#     return user.entry


# async def get_user_total(user_id: int):
#     entries = await EntryOutSchema.from_queryset(Entry.all())
#     sub1 = sum([e.amount for e in entries if e.author.id == user_id])
#     regulars = await RegularEntryOutSchema.from_queryset(RegularEntry.all())
#     sub2 = sum([r.amount for r in regulars if r.author.id == user_id])
#     return sub1 + sub2


async def create_user(user: UserInSchema) -> UserOutSchema:
    user.password = get_password_hash(user.password)

    try:
        user_obj = await UserModel.create(**user.model_dump(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(
            status_code=401, detail=f'Sorry, username {user.username} already exists.'
        )

    return await UserOutSchema.from_tortoise_orm(user_obj)


async def update_user(*, id: int, update: UpdateUser) -> UserOutSchema:
    update.password = get_password_hash(update.password)
    await UserModel.filter(id=id).update(**update.model_dump(exclude_unset=True))
    return await UserOutSchema.from_queryset_single(UserModel.get(id=id))


async def delete_user(user_id: int, current_user: UserModel) -> str:  # add current user
    try:
        db_user = await UserDatabaseSchema.from_queryset_single(
            UserModel.get(id=user_id)
        )
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f'User {user_id} not found')

    if db_user.id == current_user.id:
        del_user = await UserModel.filter(id=user_id).delete()
        if not del_user:
            raise HTTPException(status_code=404, detail=f'User {user_id} not found')
        return {'Deleted user': user_id}

    raise HTTPException(status_code=403, detail='Not authorized to delete')
