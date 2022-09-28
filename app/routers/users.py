from fastapi import APIRouter, HTTPException

from ..schema import UserIn as SchemaUserIn, UserOut as SchemaUserOut
from ..database.models import User


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[SchemaUserOut])
async def get_users():
	users = await User.get_all()
	users = [SchemaUserOut(**user) for user in users]
	return users


@router.get("/{user_id}", response_model=SchemaUserOut)
async def get_user_by_id(user_id: int):
	user = await User.get_by_id(user_id)
	if user is None:
		raise HTTPException(status_code=400, detail="User not found")
	return SchemaUserOut(**user)


@router.post("/")
async def create_user(user: SchemaUserIn):
	user_id = await User.create(**user.dict())
	return {"user_id": user_id}
