from fastapi import APIRouter, HTTPException

from ..schema import TagIn as SchemaTagIn, TagOut as SchemaTagOut
from ..database.models import Tag


router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/")
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


@router.post("/")
async def create_tag(tag: SchemaTagIn):
	tag_id = await Tag.create(**tag.dict())
	return {"tag_id": tag_id}
