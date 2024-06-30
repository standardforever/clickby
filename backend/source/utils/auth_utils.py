from fastapi import HTTPException, status, Depends, Security
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt


from datetime import datetime, timedelta
from typing import Annotated, List

from common.models.user_models import User, UserSafe

from common.libs import db_connection
from common.models.auth_return_model import RpcFunctionReturnValue

from app.config import app_config

import json



oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/{app_config.environment}/api/v1/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


USER_DATABASE_NAME = app_config.database_name
USER_COLLECTION_NAME = "users"



def verify_password(plain_password, hashed_password):
	return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
	return pwd_context.hash(password)

async def get_user(email: str):
	user = await db_connection.get(database_name=USER_DATABASE_NAME, collection_name=USER_COLLECTION_NAME, email=email)
	if not user:
		return False

	user = User(**user)

	return user

async def authenticate_user(email: str, password: str, **kwargs):
	""" To authenticate users
	"""
	user = await get_user(email)

	if not user:
		return False

	if user.disabled:
		return False

	if not verify_password(password, user.password):
		return False

	return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
	""" To create access tokne
	"""
	access_data = data.copy()
	refresh_data = data.copy()

	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=15)
	access_data.update({"exp": expire, "type": 'access'})
	refresh_data.update({"exp": datetime.utcnow() + timedelta(hours=5), 'type': "refresh"})

	access_token = jwt.encode(access_data, app_config.jwt_secret_key, algorithm=app_config.jwt_algorithm)
	refresh_token = jwt.encode(refresh_data, app_config.jwt_secret_key, algorithm=app_config.jwt_algorithm)
	return {
		"access_token": access_token,
		"refresh_token": refresh_token,
		"token_type": "Bearer"
	}


def verify_access_token(token: str):
	""" To verify JWT access token
	"""
	try:
		jwt.decode(token, app_config.jwt_secret_key)
		return True
	except:
		return False


async def create_refresh_token(token: str):
	""" To create refresh token
	"""
	try:
		user_decode = jwt.decode(token, app_config.jwt_secret_key)
		if user_decode.get('type') != 'refresh':
			return {
				"success": False,
				"detail": "Invalid refresh token",
				"status_code": status.HTTP_401_UNAUTHORIZED
			}
		payload = {'scopes': user_decode.get('scopes'), 'sub': user_decode.get('sub')}

		response = create_access_token(payload)
		return {
			"success": True,
			"detail": response
			}

	except Exception as e:
		print(e)
		return {
			"success": False,
			"detail": "Invalid refresh token",
			"status_code": status.HTTP_401_UNAUTHORIZED
		}


async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
	""" Get current User
	"""
	response =  await verify_user_token(security_scopes=security_scopes.scopes, token=token)
	
	if response.success == False:
		raise HTTPException (
			status_code=response.error_code,
			detail=response.error_message,
		)

	return User(**response.return_value)


async def get_current_active_user(
	current_user: Annotated[UserSafe, Security(get_current_user, scopes=["me:read"])]
):
	if current_user.disabled:
		raise HTTPException(status_code=400, detail="Inactive user")

	return current_user



async def verify_user_token(security_scopes: List[str], token: str) -> RpcFunctionReturnValue:
	""" To get current Login user
	"""
	try:
		
		payload = jwt.decode(token, app_config.jwt_secret_key, algorithms=[app_config.jwt_algorithm])
		username: str = payload.get("sub", None)
		if username is None:
			raise JWTError("Could not validate credentials")

		user = await get_user(email=username)

		if not user or user.disabled:
			raise ValueError("Could not validate credentials")

		if not "*" in user.scopes:
			for scope in security_scopes:
				if scope not in user.scopes:
					raise ValueError("Not enough permission. Required scope(s): {}".format(";".join(security_scopes)))

		return RpcFunctionReturnValue(
			return_value=user.model_dump()
		)

	except (JWTError, ValueError) as e:
		return RpcFunctionReturnValue(
			success=False,
			error_code=401,
			error_message=str(e)
		)