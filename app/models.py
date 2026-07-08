from datetime import datetime
from typing import Dict, List, Optional

from pgvector.sqlalchemy import Vector
from pydantic import BaseModel, Field
from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SearchTarget(Base):
    __tablename__ = "search_targets"

    id = Column(Integer, primary_key=True, autoincrement=True)

    target_id = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    alternative_phrases = Column(JSON)

    match_document = Column(
        JSON,
        nullable=False,
    )

    embedding = Column(Vector(384))

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)

    query = Column(
        Text,
        nullable=False,
    )

    target_id = Column(String(100))

    similarity = Column(Float)

    feedback_type = Column(String(20))

    comment = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


class MatchDocument(BaseModel):
    type: str
    url: Optional[str] = None
    title: Optional[str] = None

    parameters: Dict = Field(default_factory=dict)

    content_summary: Optional[str] = None


class SearchTargetCreate(BaseModel):
    target_id: str

    description: str

    alternative_phrases: List[str] = Field(default_factory=list)

    match_document: MatchDocument