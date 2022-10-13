import sqlalchemy

from sqlalchemy import Column, Integer, Text, CheckConstraint

from app.database.db import db, metadata


comments = sqlalchemy.Table(
	"comments",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("text", Text, nullable=False),
	Column("likes_cnt", Integer, nullable=False, default=0),
	Column("dislikes_cnt", Integer, nullable=False, default=0),
	CheckConstraint("likes_cnt >= 0", name="likes_check"),
	CheckConstraint("dislikes_cnt >= 0", name="dislikes_check")
)
