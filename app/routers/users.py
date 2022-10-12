from fastapi import APIRouter, HTTPException
from asyncpg.exceptions import UniqueViolationError

from app.schemas.user_schema import UserIn as SchemaUserIn, UserOut as SchemaUserOut, UserUpdate as SchemaUserUpdate
from app.database.models.user_model import User


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[SchemaUserOut])
async def get_users():
	users = await User.get_all()
	users = [SchemaUserOut(**user) for user in users]
	return users


@router.get("/{username}", response_model=SchemaUserOut)
async def get_user_by_username(username: str):
	user = await User.get_by_username(username)
	if user is None:
		raise HTTPException(status_code=400, detail="User not found")
	return SchemaUserOut(**user)


@router.post("/", status_code=201)
async def create_user(user: SchemaUserIn):
	try:
		user_id = await User.create(**user.dict())
	except UniqueViolationError:
		raise HTTPException(status_code=400, detail="User already exists")
	return {"user_id": user_id}


@router.put("/{user_id}", status_code=200, response_model=SchemaUserOut)
async def update_user(user_id: int, user: SchemaUserUpdate):
	user_dict = user.dict()
	try:
		user_data = await User.update(idx=user_id, **user_dict)
	except UniqueViolationError:
		raise HTTPException(status_code=400, detail="Email is already in use")
	return SchemaUserOut(**user_data)
