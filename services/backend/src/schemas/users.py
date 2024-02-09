"""
Tortoise comes with a pydantic model creating function
which creates the pydantic models for you:
1 - User/SuperInSchema for creating new users
2 - User/SuperOutSchema, user objects for use outside the application
3 - User/SuperDatabaseSchema, user object for use within the application for most for validation
4 - UserUpdate to update a user
"""
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.core.models import SuperUser, UserModel

UserInSchema = pydantic_model_creator(UserModel, name='UserIn', exclude_readonly=True)

UserOutSchema = pydantic_model_creator(
    UserModel,
    name='UserOut',
    exclude=['password', 'active'],
)

UserDatabaseSchema = pydantic_model_creator(UserModel, name='User')


class UpdateUser(BaseModel):
    username: str | None
    full_name: str | None
    password: str | None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'username': 'agent@provocateur.com',
                    'full_name': 'Agent Provocateur',
                    'password': 'string',
                }
            ]
        }
    }


SuperInSchema = pydantic_model_creator(SuperUser, name='SuperIn', exclude_readonly=True)

SuperOutSchema = pydantic_model_creator(
    SuperUser,
    name='SuperOut',
    exclude=['password', 'active'],
)

SuperDatabaseSchema = pydantic_model_creator(SuperUser, name='Superuser')
