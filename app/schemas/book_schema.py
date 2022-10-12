from .schema import BaseSchema, BaseOutSchema
from .tag_schema import TagOut
from .genre_schema import GenreOut


class BookIn(BaseSchema):
	title: str
	description: str
	image: str
	available: bool
	release_date: int
	publish_date: int
	tags: list[int]
	genres: list[int]


class BookOut(BaseOutSchema):
	title: str
	description: str
	image: str
	available: bool
	release_date: int
	publish_date: int
	tags: list[TagOut]
	genres: list[GenreOut]
