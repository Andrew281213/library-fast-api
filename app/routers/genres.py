from fastapi import APIRouter, HTTPException
from asyncpg.exceptions import UniqueViolationError

from ..schema import GenreIn as SchemaGenreIn, GenreOut as SchemaGenreOut
from ..database.models import Genre


router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("/", response_model=list[SchemaGenreOut])
async def get_genres():
	genres = await Genre.get_all()
	genres = [SchemaGenreOut(**genre) for genre in genres]
	return genres


@router.get("/{genre_id}", response_model=SchemaGenreOut)
async def get_genre_by_id(genre_id: int):
	genre = await Genre.get_by_id(genre_id)
	if genre is None:
		raise HTTPException(status_code=400, detail="Genre not found")
	return SchemaGenreOut(**genre)


@router.post("/")
async def create_genre(genre: SchemaGenreIn):
	try:
		genre_id = await Genre.create(**genre.dict())
	except UniqueViolationError:
		raise HTTPException(status_code=400, detail="Genre already exists")
	return genre_id
