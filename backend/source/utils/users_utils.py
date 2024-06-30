from typing import Union, List

from common.libs import db_connection
from common.models.user_models import UserSafe, User
from app.app import app_config

USERS_DATABASE_NAME = app_config.database_name
USERS_COLLECTION_NAME = "users"

async def get_users():
	users = await db_connection.get_many(USERS_DATABASE_NAME, USERS_COLLECTION_NAME)
	return users

async def get_user(id: str) -> Union[UserSafe, bool]:
	query_dict = {'id': id}
	obj = await db_connection.get(USERS_DATABASE_NAME, USERS_COLLECTION_NAME, **query_dict)
	if obj:
		return UserSafe(**obj)

	return False

async def get_user_by_email(email: str) -> Union[UserSafe, bool]:
	query_dict = {'email': email}
	obj = await db_connection.get(USERS_DATABASE_NAME, USERS_COLLECTION_NAME, **query_dict)
	if obj:
		return UserSafe(**obj)

	return False


async def create_user(user: User) -> Union[UserSafe, bool]:
	obj = await db_connection.create(USERS_DATABASE_NAME, USERS_COLLECTION_NAME, user.model_dump(mode="json"))
	if obj:
		# Send user creation email here
		return UserSafe(**obj)

	return False

async def delete_user(id: str) -> bool:
	obj = await db_connection.delete(USERS_DATABASE_NAME, USERS_COLLECTION_NAME, **{"id": id})
	if obj:
		return True
	return False

async def update_user(id: str, updated_user: Union[User, UserSafe]) -> Union[UserSafe, bool]:
	obj = await db_connection.update(USERS_DATABASE_NAME, USERS_COLLECTION_NAME, id, updated_user.model_dump(mode="json"))

	if obj:
		return UserSafe(**obj)

	return False