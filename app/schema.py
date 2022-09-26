from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
	id: int = None
	username: str
	email: str
	password: str = None
	blocked: bool = False
	is_admin: bool = False
	register_date: int
	last_visit: int

	class Config:
		orm_mode = True
