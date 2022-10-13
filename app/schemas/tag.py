from .schema import BaseSchema, BaseOutSchema


class TagIn(BaseSchema):
	title: str


class TagOut(BaseOutSchema):
	title: str
