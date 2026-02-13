"""
CampusNexus - AI Matching Service
Implements semantic skill matching using sentence-transformers.
Upgraded from Jaccard similarity to NLP-based semantic similarity.
"""
from sentence_transformers import SentenceTransformer
import numpy as np

# Global model instance (loaded lazily on first use)
# This prevents import-time delays and allows the server to start immediately
_MODEL = None


def _get_model():
    """Lazy load the sentence-transformers model on first use."""
    global _MODEL
    if _MODEL is None:
        # all-MiniLM-L6-v2: Fast, lightweight model (384-dim embeddings, ~80MB)
        # Understands semantic relationships: "Frontend" → "React", "Backend" → "FastAPI"
        _MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    return _MODEL


def calculate_match_score(user_skills: list[str], project_skills: list[str]) -> float:
    """
    Calculate semantic similarity between user skills and project requirements.
    
    Uses sentence-transformers (all-MiniLM-L6-v2) with cosine similarity.
    This enables intelligent matching where "Backend" matches "FastAPI" even
    without exact keyword overlap.
    
    Args:
        user_skills: List of user's skills (e.g., ["Frontend", "UI/UX"])
        project_skills: List of project requirements (e.g., ["React", "Tailwind"])
    
    Returns:
        float: Similarity score between 0.0 and 1.0
    
    Example:
        >>> calculate_match_score(["Frontend Development"], ["React", "TypeScript"])
        0.87  # High match despite different keywords
    """
    if not user_skills or not project_skills:
        return 0.0
    
    # Combine skills into sentences for better semantic understanding
    # The model works better with natural language context
    user_text = ", ".join(user_skills)
    project_text = ", ".join(project_skills)
    
    # Get the model (lazy loaded)
    model = _get_model()
    
    # Generate 384-dimensional embeddings
    embeddings = model.encode([user_text, project_text])
    
    # Calculate cosine similarity between the two embeddings
    # Measures the angle between vectors (direction, not magnitude)
    similarity = np.dot(embeddings[0], embeddings[1]) / (
        np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
    )
    
    # Convert from [-1, 1] range to [0, 1] range
    # -1 = opposite meaning, 0 = unrelated, 1 = identical
    normalized_score = (similarity + 1) / 2
    
    return float(normalized_score)


def rank_projects(user_skills: list[str], projects: list[dict]) -> list[dict]:
    """
    Rank projects based on semantic skill match score.
    Returns projects with their match score attached.
    
    Args:
        user_skills: User's skill list
        projects: List of project dictionaries with 'skills_required' field
    
    Returns:
        list[dict]: Projects sorted by match_score (descending)
    """
    ranked = []
    
    for project in projects:
        score = calculate_match_score(user_skills, project.get("skills_required", []))
        
        # Only include projects with some relevance (>10% match)
        if score > 0.1:
            # Create a copy to avoid mutating original
            p_with_score = project.copy()
            p_with_score["match_score"] = round(score * 100, 1)  # Convert to percentage
            ranked.append(p_with_score)
            
    # Sort by score descending
    ranked.sort(key=lambda x: x["match_score"], reverse=True)
    
    return ranked
