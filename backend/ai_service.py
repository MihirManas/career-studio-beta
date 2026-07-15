import os
import json
import google.generativeai as genai
from schemas import KnowledgeModelSchema
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-2.5-flash",
  generation_config=generation_config,
)

def extract_knowledge_model(raw_text: str) -> dict:
    """
    Transforms raw uploaded text into the highly structured KnowledgeModel JSON.
    """
    prompt = f"""
    You are the core intelligence engine for a Career Operating System. 
    Your goal is to extract knowledge from the provided text and strictly output a JSON object 
    that matches the following schema:
    {{
      "type": "String", // project, experience, research, notes
      "title": "String", 
      "problem": "String", 
      "solution": "String", 
      "why_it_matters": "String", 
      "key_learnings": ["String"], 
      "mistakes": ["String"], 
      "metrics": ["String"], 
      "skills": ["String"], 
      "technologies": ["String"], 
      "industry": "String", 
      "difficulty": "String", 
      "audience": "String", 
      "prerequisites": ["String"], 
      "summary": "String", 
      "keywords": ["String"], 
      "references": ["String"], 
      "confidence": 0.94
    }}
    
    Extract the most insightful career-oriented details from the following raw text. 
    If a field cannot be derived, make an educated guess or leave it as an empty string/array. 
    
    RAW TEXT:
    {raw_text}
    """
    
    response = model.generate_content(prompt)
    
    try:
        data = json.loads(response.text)
        # Validate against schema to ensure correctness before returning
        validated_data = KnowledgeModelSchema(**data)
        return validated_data.model_dump()
    except Exception as e:
        print("Failed to parse JSON or validate schema:", e)
        # Fallback or error handling
        return {}

def generate_quality_score(artifact_markdown: str) -> dict:
    """
    Evaluates the final artifact and generates explainable AI quality scores.
    """
    prompt = f"""
    Evaluate the following markdown article. Provide a quality score between 0 and 100 for each of the 
    following categories, and provide a 1-sentence reason for your score.
    Strictly output JSON matching this schema:
    {{
      "seo": {{"score": 81, "reason": "Missing internal links."}},
      "readability": {{"score": 90, "reason": "Uses short paragraphs."}},
      "technical_depth": {{"score": 70, "reason": "Lacks code examples."}},
      "originality": {{"score": 85, "reason": "Good personal insights."}},
      "spam_risk": {{"score": 5, "reason": "High quality content."}}
    }}
    
    ARTIFACT MARKDOWN:
    {artifact_markdown}
    """
    
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except Exception as e:
        print("Failed to generate quality score:", e)
        return {}
