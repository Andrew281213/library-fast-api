from .schema import BaseSchema, BaseOutSchema


class CommentIn(BaseSchema):
	text: str
	user_id: int
	book_id: int


class CommentOut(BaseOutSchema):
	text: str
	user_id: int
	book_id: int
	likes_cnt: int
	dislikes_cnt: int
