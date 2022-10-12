from fastapi import APIRouter, HTTPException
from asyncpg.exceptions import UniqueViolationError

from app.schemas.genre_schema import GenreIn as SchemaGenreIn, GenreOut as SchemaGenreOut
from app.database.models.genre_model import Genre


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


@router.post("/", status_code=201)
async def create_genre(genre: SchemaGenreIn):
	try:
		genre_id = await Genre.create(**genre.dict())
	except UniqueViolationError:
		raise HTTPException(status_code=400, detail="Genre already exists")
	return genre_id


@router.put("/{genre_id}", status_code=200)
async def update_genre(genre_id: int, genre: SchemaGenreIn):
	await Genre.update(idx=genre_id, **genre.dict())
	return SchemaGenreOut(id=genre_id, **genre.dict())
