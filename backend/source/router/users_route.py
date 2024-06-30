
from fastapi import APIRouter, Depends, HTTPException, status, Security, Response
from typing import Annotated, List, Union

from common.models.user_models import User, UserSafe

from utils.auth_utils import get_current_active_user


from utils.auth_utils import get_password_hash
from utils.users_utils import (get_users,
							   get_user,
							   create_user,
							   delete_user,
							   update_user)


router = APIRouter(
	tags=["Users Management"]
)

@router.get("/healthz")
async def healthz():
	return {"ok": "ok"}

# 1 - Get Many Users. Scope [infrastructure:read]
@router.get('/', response_model=list[UserSafe])
async def get_users_handler(current_user: Annotated[UserSafe, Security(get_current_active_user, scopes=['infrastructure:users:list'])]):
	return await get_users()


@router.get('/{id}', response_model=UserSafe)
async def get_user_by_id_handler(id: str, current_user: Annotated[UserSafe, Security(get_current_active_user, scopes=['users:read'])]):
	user = await get_user(id)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"Unable to retrieve user: {id}"
		)

	return user

@router.post('/', response_model=UserSafe)
async def create_user_handler(
	  user: User, current_user: Annotated[User, Security(get_current_active_user, scopes=["users:create"])]
):
	user.password = get_password_hash(user.password)

	created_user = await create_user(user)

	if not created_user:
		raise HTTPException(
			status_code= status.HTTP_400_BAD_REQUEST,
			detail=f"Unable to create user."
		)

	return created_user

@router.put('/{id}', response_model=UserSafe) # Union must be written in this order because UserSafe is subset of User
async def update_user_handler(id: str,
							  updated_user: Union[User, UserSafe],
							  current_user: Annotated[User, Security(get_current_active_user, scopes=['users:edit'])],
							  ):
	if id != str(updated_user.id):
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f"IDs do not match. Aborting."
		)
	if isinstance(updated_user, User):
		updated_user.password = get_password_hash(updated_user.password)

	org = await get_organization(id=str(updated_user.organization_id))
	if not org:
		raise HTTPException(
			status_code= status.HTTP_404_NOT_FOUND,
			detail=f"Organization ID: {str(updated_user.organization_id)} does not exists."
		)

	_updated_user = await update_user(id, updated_user)

	if not _updated_user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"Unable to update user: {id}"
		)

	return _updated_user

@router.delete('/{id}')
async def delete_user_handler(id: str,
							  current_user: Annotated[UserSafe, Security(get_current_active_user, scopes=["users:delete"])],
							  ):
	if not (await delete_user(id)):
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f"Unable to delete user: {id}"
		)

	return Response(status_code=status.HTTP_204_NO_CONTENT)