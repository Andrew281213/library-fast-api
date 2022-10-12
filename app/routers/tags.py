from fastapi import APIRouter, HTTPException
from asyncpg.exceptions import UniqueViolationError

from app.schemas.tag_schema import TagIn as SchemaTagIn, TagOut as SchemaTagOut
from app.database.models.tag_model import Tag


router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=list[SchemaTagOut])
async def get_tags():
	tags = await Tag.get_all()
	tags = [SchemaTagOut(**tag) for tag in tags]
	return tags


@router.get("/{tag_id}", response_model=SchemaTagOut)
async def get_tag_by_id(tag_id: int):
	tag = await Tag.get_by_id(tag_id)
	if tag is None:
		raise HTTPException(status_code=400, detail="Tag not found")
	return SchemaTagOut(**tag)


@router.post("/", status_code=201)
async def create_tag(tag: SchemaTagIn):
	try:
		tag_id = await Tag.create(**tag.dict())
	except UniqueViolationError:
		raise HTTPException(status_code=400, detail="Tag already exists")
	return {"tag_id": tag_id}


@router.put("/{tag_id}", status_code=200, response_model=SchemaTagOut)
async def update_tag(tag_id: int, tag: SchemaTagIn):
	tag_dict = tag.dict()
	await Tag.update(idx=tag_id, **tag_dict)
	return SchemaTagOut(id=tag_id, **tag_dict)
