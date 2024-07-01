from fastapi import APIRouter, Depends, Security
from fastapi import HTTPException, status
from typing import Annotated
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm

from common.models.token_models import Token, TokenValidate
from common.models.user_models import User, UserSafe


from utils.auth_utils import (
	get_current_user, authenticate_user,
	create_access_token, verify_access_token,
	create_refresh_token, oauth2_scheme)

from app.config import app_config

router = APIRouter(
	tags=["Authentication"]
)


@router.get("/healthz")
async def auth_healthz():
	return {"ok": "ok"}

@router.post("/token", response_model=Token)
async def login_for_access_token(
	form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):

	user = await authenticate_user(form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	
	access_token_expires = timedelta(minutes=app_config.jwt_access_token_expire_minutes)
	access_token = create_access_token(
		data={"sub": user.email, "scopes": user.scopes},
		# expires_delta=access_token_expires
	)

	return access_token

@router.get("/me", response_model=UserSafe)
async def get_me(
	current_user: Annotated[User, Security(get_current_user, scopes=["me:read"])]
):
	return current_user

@router.post('/validate')
def validate(token: TokenValidate):
	if verify_access_token(token.token):
		return get_current_user

	raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Token is not valid",
			headers={"WWW-Authenticate": "Bearer"},
		)


@router.get("/token/refresh/")
async def refresh_token(refresh_token: Annotated[str, Depends(oauth2_scheme)]):
	""" Get refresh token for users
	"""
	# Verify the refresh token and get the user associated with it
	response =  await create_refresh_token(refresh_token)

	if response.get('success'):
		return response.get('detail')
	raise HTTPException(status_code=response.get('status_code'), detail=response.get('detail'))
