import sqlalchemy

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint, Text
from datetime import datetime

from app.database.db import db, metadata


books = sqlalchemy.Table(
	"books",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("title", String(128), nullable=False, index=True),
	Column("author", String(128), nullable=False, index=True),
	Column("description", Text, nullable=False),
	Column("image", String(128), nullable=True),
	Column("available", Boolean, default=True, nullable=False),
	Column("release_date", Integer, nullable=False),
	Column("publish_date", Integer, nullable=False, default=datetime.now().timestamp())
)


class Book:
	@classmethod
	async def get_by_id(cls, idx: int):
		query = books.select().where(books.c.id == idx)
		return await db.fetch_one(query)
	
	@classmethod
	async def get_by_title_exact(cls, title: str):
		query = books.select().where(books.c.title == title)
		return await db.fetch_all(query)
	
	@classmethod
	async def get_by_title(cls, title: str):
		query = books.select().filter(books.c.title.like(title))
		return await db.fetch_all(query)
	
	@classmethod
	async def get_all(cls):
		query = books.select()
		return await db.fetch_all(query)
	
	@classmethod
	async def create(cls, **book):
		query = books.insert().values(**book)
		return await db.execute(query)
	
	@classmethod
	async def update(cls, idx: int, **book):
		query = books.update(books.c.id == idx).values(**book)
		return await db.execute(query)
	
	@classmethod
	async def delete(cls, idx):
		query = books.delete(books.c.id == idx)
		await db.execute(query)
