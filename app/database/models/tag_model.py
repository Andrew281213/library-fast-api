import sqlalchemy

from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, CheckConstraint, PrimaryKeyConstraint

from app.database.db import db, metadata


tags = sqlalchemy.Table(
	"tags",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("title", String(24), nullable=False, unique=True)
)


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
