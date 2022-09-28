import sqlalchemy

from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, CheckConstraint, PrimaryKeyConstraint
from datetime import datetime

from app.database.db import db, metadata


users = sqlalchemy.Table(
	"users",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("username", String(24), index=True, unique=True, nullable=False),
	Column("email", String(64), index=True, unique=True, nullable=False),
	Column("password", String(64), nullable=False),
	Column("blocked", Boolean, default=False, nullable=False),
	Column("is_admin", Boolean, default=False, nullable=False),
	Column("register_date", Integer, default=datetime.now().timestamp(), nullable=False),
	Column("last_visit", Integer, default=datetime.now().timestamp(), nullable=False)
)


genres = sqlalchemy.Table(
	"genres",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("title", String(64), index=True, nullable=False, unique=True),
	Column("description", String(128), nullable=False)
)


books = sqlalchemy.Table(
	"books",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("title", String(64), nullable=False, index=True, unique=True),
	Column("description", Text, nullable=False),
	Column("image", String, nullable=False, unique=True),
	Column("available", Boolean, default=True),
	Column("release_date", Integer, nullable=False),
	Column("publish_date", Integer, nullable=False, default=datetime.now().timestamp())
)

comments = sqlalchemy.Table(
	"comments",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("text", Text, nullable=False),
	Column("likes_cnt", Integer, nullable=False, default=0),
	Column("dislikes_cnt", Integer, nullable=False, default=0),
	CheckConstraint("likes_cnt >= 0", name="likes_check"),
	CheckConstraint("dislikes_cnt >= 0", name="dislikes_check")
)


tags = sqlalchemy.Table(
	"tags",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("title", String(24), nullable=False)
)


genres_book = sqlalchemy.Table(
	"genres_book",
	metadata,
	Column("genre_id", Integer, ForeignKey("genres.id"), nullable=False),
	Column("book_id", Integer, ForeignKey("books.id"), nullable=False),
	PrimaryKeyConstraint("genre_id", "book_id")
)


comments_book_user = sqlalchemy.Table(
	"comments_book_user",
	metadata,
	Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
	Column("book_id", Integer, ForeignKey("books.id"), nullable=False),
	Column("comment_id", Integer, ForeignKey("comments.id"), nullable=False),
	PrimaryKeyConstraint("user_id", "book_id", "comment_id")
)


tags_book = sqlalchemy.Table(
	"tags_book",
	metadata,
	Column("tag_id", Integer, ForeignKey("tags.id"), nullable=False),
	Column("book_id", Integer, ForeignKey("books.id"), nullable=False),
	PrimaryKeyConstraint("tag_id", "book_id")
)


class User:
	@classmethod
	async def get_by_id(cls, idx):
		query = users.select().where(users.c.id == idx)
		user = await db.fetch_one(query)
		return user
	
	@classmethod
	async def get_by_username(cls, username):
		query = users.select().where(users.c.username == username)
		user = await db.fetch_one(query)
		return user

	@classmethod
	async def get_all(cls):
		query = users.select()
		items = await db.fetch_all(query)
		return items
	
	@classmethod
	async def create(cls, **user):
		query = users.insert().values(**user)
		user_id = await db.execute(query)
		return user_id


class Tag:
	@classmethod
	async def get_by_id(cls, idx):
		query = tags.select().where(tags.c.id == idx)
		tag = await db.fetch_one(query)
		return tag
	
	@classmethod
	async def get_all(cls):
		query = tags.select()
		tags_objs = await db.fetch_all(query)
		return tags_objs
	
	@classmethod
	async def create(cls, **tag):
		query = tags.insert().values(**tag)
		tag_id = await db.execute(query)
		return tag_id

class Genre:
	@classmethod
	async def get_by_id(cls, idx):
		query = genres.select().where(genres.c.id == idx)
		genre = await db.fetch_one(query)
		return genre
	
	@classmethod
	async def get_all(cls):
		query = genres.select()
		genres_objs = await db.fetch_all(query)
		return genres_objs

	@classmethod
	async def create(cls, **genre):
		query = genres.insert().values(**genre)
		genre_id = await db.execute(query)
		return genre_id
