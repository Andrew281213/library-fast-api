import sqlalchemy

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timedelta

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


tokens = sqlalchemy.Table(
	"tokens",
	metadata,
	Column("id", Integer, primary_key=True),
	Column(
		"token", UUID(as_uuid=False), server_default=sqlalchemy.text("uuid_generate_v4()"), unique=True,
		nullable=False, index=True
	),
	Column("expires", DateTime()),
	Column("user_id", ForeignKey("users.id"))
)


class User:
	@classmethod
	async def get_by_id(cls, idx: int):
		query = users.select().where(users.c.id == idx)
		return await db.fetch_one(query)
	
	@classmethod
	async def get_by_username(cls, username: str):
		query = users.select().where(users.c.username == username)
		return await db.fetch_one(query)

	@classmethod
	async def get_by_token(cls, token: str):
		query = tokens.join(users).select(tokens.c.token == token and tokens.c.expires > datetime.now())
		return await db.fetch_one(query)
	
	@classmethod
	async def create_token(cls, user_id: int):
		query = (
			tokens.insert().values(expires=datetime.now() + timedelta(weeks=2), user_id=user_id)
		).returning(tokens.c.token, tokens.c.expires)
		return await db.fetch_one(query)
	
	@classmethod
	async def get_all(cls):
		query = users.select()
		return await db.fetch_all(query)
	
	@classmethod
	async def create(cls, **user):
		query = users.insert().values(**user)
		return await db.execute(query)

	@classmethod
	async def update(cls, idx, **user):
		query = users.update(users.c.id == idx).values(**user)
		await db.execute(query)
		return await cls.get_by_id(idx)
