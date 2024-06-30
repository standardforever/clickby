from pydantic import EmailStr, Field, UUID4, BaseModel, validator
from typing import List, Optional
from enum import Enum
from datetime import datetime

try:
	from common.models.mongo_models import MongoModel, PasswordField
except:
	from .mongo_models import MongoModel, PasswordField



class UserSafe(MongoModel):
	username: str = Field(...)
	email: EmailStr = Field(...)
	disabled: bool = False
	is_verified: bool = False
	scopes: List[str] = ["me:read"]

class User(UserSafe, PasswordField):
	pass
	
class ResetPasswordData(BaseModel):
	password: str
	reset_token: str

class ForgetPasswordData(BaseModel):
	email: EmailStr