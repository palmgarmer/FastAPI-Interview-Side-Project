from pydantic import BaseModel, Field

# Schema for POST /interviews/{id}/feedback
class FeedbackCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: str = Field(..., min_length=1, max_length=1000, description="Feedback comment")

# Schema for GET /interviews/{id}/feedback  
class FeedbackResponse(BaseModel):
    id: int
    interview_id: int
    rating: int
    comment: str
    
    class Config:
        from_attributes = True  
