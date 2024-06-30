from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from typing import Optional
import uuid

class MongoModel(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime  = Field(default_factory=datetime.now)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            # ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }

class IdentityMongoModel(MongoModel):
    created_by: Optional[UUID4]
    updated_by: Optional[UUID4]

class PasswordField(BaseModel):
    password: str = Field(...)