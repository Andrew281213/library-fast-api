from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.database.models.user_model import User
from app.schemas.user_schema import UserOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/auth")


async def get_current_user(token: str = Depends(oauth2_scheme)):
	user = await User.get_by_token(token)
	if user is None:
		raise HTTPException(
			status_code=401, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"}
		)
	return user


async def is_admin(user: UserOut = Depends(get_current_user)):
	if not user.is_admin:
		raise HTTPException(status_code=403, detail="Not enough permissions")
	return user
