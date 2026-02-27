from sentence_transformers import SentenceTransformer
import numpy as np

_MODEL = None

def _get_model():

    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    return _MODEL

def calculate_match_score(user_skills: list[str], project_skills: list[str]) -> float:

    if not user_skills or not project_skills:
        return 0.0
    
    user_text = ", ".join(user_skills)
    project_text = ", ".join(project_skills)
    
    model = _get_model()
    
    embeddings = model.encode([user_text, project_text])
    
    similarity = np.dot(embeddings[0], embeddings[1]) / (
        np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
    )
    
    normalized_score = (similarity + 1) / 2
    
    return float(normalized_score)

def rank_projects(user_skills: list[str], projects: list[dict]) -> list[dict]:

    ranked = []
    
    for project in projects:
        score = calculate_match_score(user_skills, project.get("skills_required", []))
        
        if score > 0.1:
            p_with_score = project.copy()
            p_with_score["match_score"] = round(score * 100, 1)
            ranked.append(p_with_score)
            
    ranked.sort(key=lambda x: x["match_score"], reverse=True)
    
    return ranked
