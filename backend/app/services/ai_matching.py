"""
CampusNexus - AI Matching Service
Implements skill matching logic for matching students to projects.
"""

def calculate_match_score(user_skills: list[str], project_skills: list[str]) -> float:
    """
    Calculate a match score between user skills and project requirements.
    Uses Jaccard similarity coefficient suitable for set comparison.
    """
    if not user_skills or not project_skills:
        return 0.0
        
    # Normalize skills to lowercase
    u_skills = set(s.lower().strip() for s in user_skills)
    p_skills = set(s.lower().strip() for s in project_skills)
    
    intersection = u_skills.intersection(p_skills)
    union = u_skills.union(p_skills)
    
    if not union:
        return 0.0
        
    return len(intersection) / len(union)

def rank_projects(user_skills: list[str], projects: list[dict]) -> list[dict]:
    """
    Rank projects based on skill match score.
    Returns projects with their match score attached.
    """
    ranked = []
    
    for project in projects:
        score = calculate_match_score(user_skills, project.get("skills_required", []))
        if score > 0:
            # Create a copy to avoid mutating original
            p_with_score = project.copy()
            p_with_score["match_score"] = round(score * 100, 1)  # Convert to percentage
            ranked.append(p_with_score)
            
    # Sort by score descending
    ranked.sort(key=lambda x: x["match_score"], reverse=True)
    
    return ranked
