from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database
import models
import schemas
import ai_service
from typing import Dict, Any

router = APIRouter(prefix="/api/v1/knowledge", tags=["Knowledge Engine"])

@router.post("/upload", response_model=Dict[str, Any])
def upload_knowledge(request: schemas.UploadKnowledgeRequest, db: Session = Depends(database.get_db)):
    # 1. Create KnowledgeSource
    db_source = models.KnowledgeSource(
        user_id=request.user_id,
        source_type=request.source_type,
        raw_text=request.raw_text,
        cleaned_text=request.raw_text # In phase 1, we assume raw_text is somewhat clean or we clean it in AI
    )
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    
    # 2. Extract structured KnowledgeModel via AI
    extracted_data = ai_service.extract_knowledge_model(db_source.raw_text)
    if not extracted_data:
        raise HTTPException(status_code=500, detail="Failed to extract knowledge model using AI")
        
    # 3. Save KnowledgeModel
    db_model = models.KnowledgeModel(
        source_id=db_source.id,
        json_representation=extracted_data
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    
    return {
        "status": "success",
        "source_id": db_source.id,
        "model_id": db_model.id,
        "knowledge_model": extracted_data
    }

from renderer import generate_artifact_content
import uuid

@router.post("/generate-artifact", response_model=Dict[str, Any])
def generate_artifact(request: schemas.GenerateArtifactRequest, db: Session = Depends(database.get_db)):
    # 1. Fetch KnowledgeModel
    db_model = db.query(models.KnowledgeModel).filter(models.KnowledgeModel.id == request.model_id).first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Knowledge Model not found")
        
    # 2. Render content via FastAPI Renderer
    rendered_data = generate_artifact_content(db_model.json_representation, request.artifact_type)
    
    # 3. Generate Explainable Quality Score via AI
    quality_scores = ai_service.generate_quality_score(rendered_data["markdown"])
    
    # 4. Save KnowledgeArtifact
    # Simple slug generation for demo purposes
    slug = db_model.json_representation.get("title", "untitled").lower().replace(" ", "-") + "-" + str(uuid.uuid4())[:8]
    
    db_artifact = models.KnowledgeArtifact(
        model_id=db_model.id,
        parent_artifact_id=request.parent_artifact_id,
        artifact_type=request.artifact_type,
        status="review",
        raw_json=rendered_data["raw_json"],
        markdown=rendered_data["markdown"],
        html=rendered_data["html"],
        title=db_model.json_representation.get("title", "Untitled Artifact"),
        slug=slug,
        quality_scores=quality_scores,
        seo_fields={}
    )
    db.add(db_artifact)
    db.commit()
    db.refresh(db_artifact)
    
    # 5. Log the AI Version in artifact_versions
    db_version = models.ArtifactVersion(
        artifact_id=db_artifact.id,
        author_type="ai",
        content_json=rendered_data["raw_json"],
        content_md=rendered_data["markdown"],
        version_number=1
    )
    db.add(db_version)
    db.commit()
    
    return {
        "status": "success",
        "artifact_id": db_artifact.id,
        "artifact": {
            "title": db_artifact.title,
            "markdown": db_artifact.markdown,
            "html": db_artifact.html,
            "quality_scores": quality_scores
        }
    }
