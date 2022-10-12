from datetime import datetime
from pydantic import UUID4, BaseModel, Field, validator
from typing import Optional

from .schema import BaseSchema, BaseOutSchema


class TokenBase(BaseModel):
	token: UUID4 = Field(alias="access_token")
	expires: datetime
	token_type: Optional[str] = "bearer"
	
	class Config:
		allow_population_by_field_name = True
		json_encoders = {
			datetime: lambda x: x.timestamp()
		}
	
	@validator("token")
	def hexlify_token(cls, value):
		return value.hex


class UserIn(BaseSchema):
	username: str
	email: str
	password: str = None
	blocked: bool = False
	is_admin: bool = False
	register_date: int = datetime.now().timestamp()
	last_visit: int = datetime.now().timestamp()


class UserUpdate(BaseSchema):
	email: str
	password: str


class UserOut(BaseOutSchema):
	username: str
	email: str
	register_date: int
	last_visit: int
	is_admin: bool


class UserDetailed(UserOut):
	token: TokenBase = {}
