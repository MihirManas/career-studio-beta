import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from database import Base, engine

# Helper to use standard JSON if not running Postgres, or JSONB if Postgres
# For the sake of local SQLite fallback in the dry run, we'll use standard JSON type
# but in production, this should be JSONB
DB_JSON = JSON

class KnowledgeSource(Base):
    __tablename__ = "knowledge_sources"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True) # Typically a UUID string from Auth
    source_type = Column(String, index=True) # e.g. pdf, markdown, notes, github
    raw_file = Column(String, nullable=True) # URL to storage
    raw_text = Column(Text, nullable=True) # Extracted raw text
    cleaned_text = Column(Text, nullable=True) # Cleaned formatted text
    metadata_json = Column(DB_JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class KnowledgeModel(Base):
    __tablename__ = "knowledge_models"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String, ForeignKey("knowledge_sources.id"))
    json_representation = Column(DB_JSON) # This holds the core Knowledge Schema
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class KnowledgeArtifact(Base):
    __tablename__ = "knowledge_artifacts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    model_id = Column(String, ForeignKey("knowledge_models.id"))
    parent_artifact_id = Column(String, ForeignKey("knowledge_artifacts.id"), nullable=True)
    artifact_type = Column(String, index=True) # e.g. article, linkedin_post
    status = Column(String, index=True, default="uploaded") # processing, review, draft, published
    raw_json = Column(DB_JSON)
    markdown = Column(Text)
    html = Column(Text)
    title = Column(String)
    slug = Column(String, unique=True, index=True)
    seo_fields = Column(DB_JSON)
    quality_scores = Column(DB_JSON) # Explainable AI scores
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ArtifactVersion(Base):
    __tablename__ = "artifact_versions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    artifact_id = Column(String, ForeignKey("knowledge_artifacts.id"))
    author_type = Column(String) # ai, user, system
    content_json = Column(DB_JSON)
    content_md = Column(Text)
    version_number = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class ArticleView(Base):
    __tablename__ = "article_views"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    artifact_id = Column(String, ForeignKey("knowledge_artifacts.id"), index=True)
    viewer = Column(String) # anonymous IP hash or user UUID
    source = Column(String) # e.g. direct, linkedin, twitter
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables for the dry run automatically (In prod, use Alembic)
Base.metadata.create_all(bind=engine)
