from .schema import BaseSchema, BaseOutSchema


class GenreIn(BaseSchema):
	title: str
	description: str


class GenreOut(BaseOutSchema):
	title: str
	description: str
