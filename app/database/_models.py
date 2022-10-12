import sqlalchemy

from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, CheckConstraint, PrimaryKeyConstraint
from datetime import datetime

from app.database.db import db, metadata


books = sqlalchemy.Table(
	"books",
	metadata,
	Column("id", Integer, primary_key=True, index=True, autoincrement=True),
	Column("title", String(64), nullable=False, index=True, unique=True),
	Column("description", Text, nullable=False),
	Column("image", String, nullable=False, unique=True),
	Column("available", Boolean, default=True),
	Column("release_date", Integer, nullable=False),
	Column("publish_date", Integer, nullable=False, default=datetime.now().timestamp())
)


genres_book = sqlalchemy.Table(
	"genres_book",
	metadata,
	Column("genre_id", Integer, ForeignKey("genres.id"), nullable=False),
	Column("book_id", Integer, ForeignKey("books.id"), nullable=False),
	PrimaryKeyConstraint("genre_id", "book_id")
)


comments_book_user = sqlalchemy.Table(
	"comments_book_user",
	metadata,
	Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
	Column("book_id", Integer, ForeignKey("books.id"), nullable=False),
	Column("comment_id", Integer, ForeignKey("comments.id"), nullable=False),
	PrimaryKeyConstraint("user_id", "book_id", "comment_id")
)


tags_book = sqlalchemy.Table(
	"tags_book",
	metadata,
	Column("tag_id", Integer, ForeignKey("tags.id"), nullable=False),
	Column("book_id", Integer, ForeignKey("books.id"), nullable=False),
	PrimaryKeyConstraint("tag_id", "book_id")
)
