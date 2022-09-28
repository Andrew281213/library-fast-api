from pydantic import BaseModel


class UserIn(BaseModel):
	username: str
	email: str
	password: str = None
	blocked: bool = False
	is_admin: bool = False
	register_date: int
	last_visit: int

	class Config:
		orm_mode = True


class UserOut(BaseModel):
	id: int
	username: str
	email: str
	register_date: int
	last_visit: int
	
	class Config:
		orm_mode = True


class GenreIn(BaseModel):
	title: str
	description: str
	
	class Config:
		orm_mode = True


class GenreOut(BaseModel):
	id: int
	title: str
	description: str

	class Config:
		orm_mode = True


class TagIn(BaseModel):
	title: str
	
	class Config:
		orm_mode = True


class TagOut(BaseModel):
	id: int
	title: str
	
	class Config:
		orm_mode = True


class BookIn(BaseModel):
	title: str
	description: str
	image: str
	available: bool
	release_date: int
	publish_date: int
	tags: list[int]
	genres: list[int]
	
	class Config:
		orm_mode = True


class BookOut(BaseModel):
	id: int
	title: str
	description: str
	image: str
	available: bool
	release_date: int
	publish_date: int
	tags: list[TagOut]
	genres: list[GenreOut]


class CommentIn(BaseModel):
	text: str
	user_id: int
	book_id: int
	
	class Config:
		orm_mode = True


class CommentOut(BaseModel):
	id: int
	text: str
	user_id: int
	book_id: int
	likes_cnt: int
	dislikes_cnt: int
	
	class Config:
		orm_mode = True
