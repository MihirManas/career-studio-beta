from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# ==========================================
# Core Knowledge Model Schema (The Heart)
# ==========================================
class KnowledgeModelSchema(BaseModel):
    type: str = Field(..., description="e.g. project, experience, notes")
    title: str
    problem: str
    solution: str
    why_it_matters: str
    key_learnings: List[str]
    mistakes: List[str]
    metrics: List[str]
    skills: List[str]
    technologies: List[str]
    industry: str
    difficulty: str
    audience: str
    prerequisites: List[str]
    summary: str
    keywords: List[str]
    references: List[str]
    confidence: float

# ==========================================
# Explainable Quality Score Schema
# ==========================================
class ScoreDetail(BaseModel):
    score: int
    reason: str

class QualityScores(BaseModel):
    seo: Optional[ScoreDetail]
    readability: Optional[ScoreDetail]
    technical_depth: Optional[ScoreDetail]
    originality: Optional[ScoreDetail]
    spam_risk: Optional[ScoreDetail]

# ==========================================
# API Request/Response Schemas
# ==========================================
class UploadKnowledgeRequest(BaseModel):
    user_id: str
    source_type: str
    raw_text: str

class GenerateArtifactRequest(BaseModel):
    model_id: str
    artifact_type: str # article, linkedin, thread
    parent_artifact_id: Optional[str] = None
