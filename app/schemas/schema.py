from pydantic import BaseModel


class BaseSchema(BaseModel):
	class Config:
		orm_mode = True


class BaseOutSchema(BaseSchema):
	id: int
