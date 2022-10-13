from .schema import BaseSchema, BaseOutSchema


class GenreIn(BaseSchema):
	title: str
	description: str


class GenreOut(BaseOutSchema):
	title: str


class GenreDetailOut(GenreOut):
	description: str
