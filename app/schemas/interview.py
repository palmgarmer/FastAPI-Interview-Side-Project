from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

# Import feedback schema
from .feedback import FeedbackResponse

# Schema for POST /candidates/{id}/interviews
class InterviewCreate(BaseModel):
    interviewer: str = Field(..., min_length=1, max_length=100, description="Name of the interviewer")
    scheduled_at: datetime = Field(..., description="Scheduled date and time for the interview")

# Schema for GET /candidates/{id}/interviews (without feedback)
class InterviewResponse(BaseModel):
    id: int
    candidate_id: uuid.UUID
    interviewer: str
    scheduled_at: datetime
    result: Optional[str] = None
    
    class Config:
        from_attributes = True

# Schema for GET /candidates (includes feedback)
class InterviewWithFeedback(BaseModel):
    id: int
    candidate_id: uuid.UUID
    interviewer: str
    scheduled_at: datetime
    result: Optional[str] = None
    feedback: List[FeedbackResponse] = []
    
    class Config:
        from_attributes = True