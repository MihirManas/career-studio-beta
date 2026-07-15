-- Career Studio Beta: Supabase Schema Definition
-- Run this in the Supabase SQL Editor

CREATE TABLE knowledge_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR NOT NULL,
    source_type VARCHAR NOT NULL,
    raw_file VARCHAR,
    raw_text TEXT,
    cleaned_text TEXT,
    metadata_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE knowledge_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES knowledge_sources(id) ON DELETE CASCADE,
    json_representation JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE knowledge_artifacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_id UUID REFERENCES knowledge_models(id) ON DELETE CASCADE,
    parent_artifact_id UUID REFERENCES knowledge_artifacts(id) ON DELETE SET NULL,
    artifact_type VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'uploaded',
    raw_json JSONB,
    markdown TEXT,
    html TEXT,
    title VARCHAR,
    slug VARCHAR UNIQUE,
    seo_fields JSONB,
    quality_scores JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE artifact_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    artifact_id UUID REFERENCES knowledge_artifacts(id) ON DELETE CASCADE,
    author_type VARCHAR NOT NULL,
    content_json JSONB,
    content_md TEXT,
    version_number INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE article_views (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    artifact_id UUID REFERENCES knowledge_artifacts(id) ON DELETE CASCADE,
    viewer VARCHAR,
    source VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Optional: Create Indexes for faster querying
CREATE INDEX idx_knowledge_sources_user ON knowledge_sources(user_id);
CREATE INDEX idx_knowledge_artifacts_slug ON knowledge_artifacts(slug);
