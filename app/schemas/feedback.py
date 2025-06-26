from pydantic import BaseModel, Field, ConfigDict

# Schema for POST /interviews/{id}/feedback
class FeedbackCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: str = Field(..., min_length=1, max_length=1000, description="Feedback comment")

# Schema for GET /interviews/{id}/feedback  
class FeedbackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    interview_id: int
    rating: int
    comment: str  
