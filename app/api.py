from fastapi import FastAPI

from app.database.db import db
from app.database.models import User as ModelUser
from app.schema import User as SchemaUser


app = FastAPI()


@app.on_event("startup")
async def startup():
	await db.connect()


@app.on_event("shutdown")
async def shutdown():
	await db.disconnect()


@app.post("/users")
async def create_user(user: SchemaUser):
	user_id = await ModelUser.create(**user.dict())
	return {"user_id": user_id}


@app.get("/users", response_model=list[SchemaUser])
async def get_users():
	users = await ModelUser.get_all()
	users = [SchemaUser(**user) for user in users]
	return users


@app.get("/users/{uuid}", response_model=SchemaUser)
async def get_user(uuid: int):
	user = await ModelUser.get(uuid)
	return SchemaUser(**user)
