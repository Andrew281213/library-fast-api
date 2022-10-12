import sqlalchemy

from sqlalchemy import Column, Integer, String

from app.database.db import db, metadata


genres = sqlalchemy.Table(
	"genres",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("title", String(64), index=True, nullable=False, unique=True),
	Column("description", String(128), nullable=False)
)


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

	@classmethod
	async def update(cls, idx, **genre):
		query = genres.update(genres.c.id == idx).values(**genre)
		await db.execute(query)
