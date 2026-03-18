from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from datetime import datetime
import uuid
from pgvector.sqlalchemy import Vector

class KnowledgeDocumentBase(SQLModel):
    title: str
    description: Optional[str] = None
    source_type: str
    blob_uri: Optional[str] = None
    mime_type: Optional[str] = None
    status: str = "draft"
    version: int = 1
    tags: Optional[List[str]] = Field(default=None, sa_type=JSON)
    audiences: Optional[List[str]] = Field(default=None, sa_type=JSON)
    language: str = "en"
    author: Optional[str] = None
    priority: int = 0
    hash: str = ""

class KnowledgeDocument(KnowledgeDocumentBase, table=True):
    __tablename__ = "knowledge_documents"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None
    additional_metadata: dict = Field(default={}, sa_column=Column(JSON))

class KnowledgeChunkBase(SQLModel):
    text: str
    type: str = "text"
    tokens: int
    heading_path: Optional[List[str]] = Field(default=None, sa_type=JSON)
    section_anchor: Optional[str] = None
    start_offset: Optional[int] = None
    end_offset: Optional[int] = None
    hash: str

class KnowledgeChunk(KnowledgeChunkBase, table=True):
    __tablename__ = "knowledge_chunks"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    document_id: uuid.UUID = Field(foreign_key="knowledge_documents.id")
    embedding: Optional[List[float]] = Field(default=None, sa_type=Vector(1536))
    additional_metadata: dict = Field(default={}, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
