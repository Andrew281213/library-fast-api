from fastapi import FastAPI

from .database.db import db
from .routers import users, tags


app = FastAPI()
app.include_router(users.router, prefix="/api/v1")
app.include_router(tags.router, prefix="/api/v1")


@app.on_event("startup")
async def startup():
	await db.connect()


@app.on_event("shutdown")
async def shutdown():
	await db.disconnect()


