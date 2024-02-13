"""
collection of user crud function. Meaning the focus is on the user
There are no HTTP exceptions and other checks here, this done in the router
The functions are not commented on as they are typed and relatively simple
"""


from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.core.models import User
from src.core.security import get_password_hash

# from src.schemas.entries import EntryOutSchema, RegularEntryOutSchema
from src.schemas.users import (
    UpdateUser,
    UserDatabaseSchema,
    UserInSchema,
    UserOutSchema,
)


async def get_user(id: int) -> UserOutSchema:  # type: ignore
    try: 
        return await UserOutSchema.from_queryset_single(User.get(id=id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f'there is no user with id {id}') 


async def get_users() -> list[UserOutSchema]:  # type: ignore
    return await UserOutSchema.from_queryset(User.all())


# async def get_entries_user(username: str):
#     user = await UserDatabaseSchema.from_queryset_single(User.get(username=username))
#     return user.entry


# async def get_user_total(user_id: int):
#     entries = await EntryOutSchema.from_queryset(Entry.all())
#     sub1 = sum([e.amount for e in entries if e.author.id == user_id])
#     regulars = await RegularEntryOutSchema.from_queryset(RegularEntry.all())
#     sub2 = sum([r.amount for r in regulars if r.author.id == user_id])
#     return sub1 + sub2


async def create_user(user: UserInSchema) -> UserOutSchema:  # type: ignore
    user.password = get_password_hash(user.password)

    try:
        user_obj = await User.create(**user.model_dump(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(
            status_code=401, detail=f'Sorry, username {user.username} already exists.'
        )

    return await UserOutSchema.from_tortoise_orm(user_obj)


async def update_user(*, id: int, update: UpdateUser) -> UserOutSchema:  # type: ignore
    if update.password:
        update.password = get_password_hash(update.password)
    await User.filter(id=id).update(**update.model_dump(exclude_unset=True))
    return await UserOutSchema.from_queryset_single(User.get(id=id))


async def delete_user(id: int) -> dict[str, int]:
    await User.filter(id=id).delete()
    return {'Deleted user': id}
