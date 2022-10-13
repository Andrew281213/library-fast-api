from .schema import BaseSchema, BaseOutSchema
from .tag import TagOut
from .genre import GenreOut


class BookIn(BaseSchema):
	title: str
	author: str
	description: str
	image: str
	available: bool
	release_date: int
	publish_date: int
	genres: list[int]
	tags: list[int] = []


class BookOut(BaseOutSchema):
	title: str
	author: str
	description: str
	image: str
	available: bool
	release_date: int
	publish_date: int
	genres: list[GenreOut]
	tags: list[TagOut]
