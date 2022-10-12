import sqlalchemy

from sqlalchemy import Column, Integer, String, Boolean
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
