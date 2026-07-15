import markdown
from typing import Dict, Any

def render_article_markdown(model_data: Dict[str, Any]) -> str:
    """
    Renders the structured KnowledgeModel JSON into a beautiful Markdown Article.
    """
    md = f"# {model_data.get('title', 'Untitled')}\n\n"
    
    if model_data.get('summary'):
        md += f"**Summary**: {model_data['summary']}\n\n"
        
    if model_data.get('problem'):
        md += f"## The Problem\n{model_data['problem']}\n\n"
        
    if model_data.get('why_it_matters'):
        md += f"### Why It Matters\n{model_data['why_it_matters']}\n\n"
        
    if model_data.get('solution'):
        md += f"## The Solution\n{model_data['solution']}\n\n"
        
    if model_data.get('technologies'):
        md += f"### Technologies Used\n"
        for tech in model_data['technologies']:
            md += f"- {tech}\n"
        md += "\n"
        
    if model_data.get('metrics'):
        md += f"## Results & Metrics\n"
        for metric in model_data['metrics']:
            md += f"- {metric}\n"
        md += "\n"
        
    if model_data.get('key_learnings'):
        md += f"## Key Learnings\n"
        for learning in model_data['key_learnings']:
            md += f"- {learning}\n"
        md += "\n"
        
    if model_data.get('mistakes'):
        md += f"## Pitfalls & Mistakes (Authenticity)\n"
        for mistake in model_data['mistakes']:
            md += f"- {mistake}\n"
        md += "\n"
        
    return md

def render_markdown_to_html(md_text: str) -> str:
    """
    Converts the generated markdown into HTML for the frontend to easily display.
    """
    return markdown.markdown(md_text, extensions=['extra', 'codehilite'])

def generate_artifact_content(model_data: Dict[str, Any], artifact_type: str) -> dict:
    """
    Dispatcher to render the appropriate format based on artifact type.
    """
    if artifact_type == "article":
        md = render_article_markdown(model_data)
        html = render_markdown_to_html(md)
    elif artifact_type == "linkedin_post":
        # Simplified renderer for LinkedIn
        title = model_data.get('title', '')
        problem = model_data.get('problem', '')
        solution = model_data.get('solution', '')
        metrics = "\\n".join([f"📈 {m}" for m in model_data.get('metrics', [])])
        md = f"**{title}**\n\nEver struggled with: {problem}?\n\nHere is how we solved it: {solution}\n\n{metrics}\n\n#Tech #Career"
        html = render_markdown_to_html(md)
    else:
        # Fallback
        md = render_article_markdown(model_data)
        html = render_markdown_to_html(md)
        
    return {
        "markdown": md,
        "html": html,
        "raw_json": model_data # Reusing the data
    }
