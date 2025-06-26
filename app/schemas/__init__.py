"""
Schema resolver to handle forward references in Pydantic models
"""

def resolve_all_references():
    """Resolve all forward references in schemas"""
    # Import all schemas first to make them available
    from app.schemas import candidate, interview, feedback
    
    # Then import the resolver functions
    from app.schemas.candidate import resolve_candidate_references
    from app.schemas.interview import resolve_interview_references
    
    # Resolve in order
    resolve_interview_references()
    resolve_candidate_references()
