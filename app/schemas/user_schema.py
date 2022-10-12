from datetime import datetime

from .schema import BaseSchema, BaseOutSchema


class UserIn(BaseSchema):
	username: str
	email: str
	password: str = None
	blocked: bool = False
	is_admin: bool = False
	register_date: int = datetime.now().timestamp()
	last_visit: int = datetime.now().timestamp()


class UserOut(BaseOutSchema):
	id: int
	username: str
	email: str
	register_date: int
	last_visit: int
