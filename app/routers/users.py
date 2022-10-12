from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from asyncpg.exceptions import UniqueViolationError

from app.schemas.user_schema import UserIn, UserOut, UserDetailed, UserUpdate, TokenBase
from app.database.models.user_model import User
from app.utils.users import get_hashed_password, verify_password
from app.utils.dependencies import get_current_user


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/auth", response_model=TokenBase)
async def auth(form: OAuth2PasswordRequestForm = Depends()):
	user = await User.get_by_username(username=form.username)
	if user is None:
		raise HTTPException(
			status_code=400, detail="Incorrect login or password"
		)
	if not verify_password(password=form.password, hashed_password=user["password"]):
		raise HTTPException(
			status_code=400, detail="Incorrect login or password"
		)
	content = TokenBase(**await User.create_token(user["id"]))
	headers = {
		"Authorization": f"{content.token_type} {content.token}"
	}
	return JSONResponse(content=content.json(), headers=headers)


@router.get("/me", response_model=UserOut)
async def get_me(current_user: UserIn = Depends(get_current_user)):
	return current_user


@router.get("/", response_model=list[UserOut], dependencies=[Depends(get_current_user)])
async def get_users():
	users = await User.get_all()
	users = [UserOut(**user) for user in users]
	return users


@router.get("/{username}", response_model=UserOut, dependencies=[Depends(get_current_user)])
async def get_user_by_username(username: str):
	user = await User.get_by_username(username)
	if user is None:
		raise HTTPException(status_code=400, detail="User not found")
	return UserOut(**user)


@router.post("/", status_code=201)
async def create_user(user: UserIn):
	user.password = get_hashed_password(user.password)
	try:
		user_id = await User.create(**user.dict())
	except UniqueViolationError:
		raise HTTPException(status_code=400, detail="User already exists")
	return {"user_id": user_id}


@router.put("/{user_id}", status_code=200, response_model=UserOut)
async def update_user(user_id: int, user: UserUpdate = Depends(get_current_user)):
	user_dict = user.dict()
	try:
		user_data = await User.update(idx=user_id, **user_dict)
	except UniqueViolationError:
		raise HTTPException(status_code=400, detail="Email is already in use")
	return UserOut(**user_data)
