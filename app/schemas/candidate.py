from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
import uuid
from datetime import datetime
from app.models.candidate import CandidateStatus

# Basic feedback schema (to avoid circular imports)
class FeedbackInCandidate(BaseModel):
    id: int
    interview_id: int
    rating: int
    comment: str
    
    class Config:
        from_attributes = True

# Interview schema for use in candidate response
class InterviewInCandidate(BaseModel):
    id: int
    candidate_id: uuid.UUID
    interviewer: str
    scheduled_at: datetime
    result: Optional[str] = None
    feedback: List[FeedbackInCandidate] = []
    
    class Config:
        from_attributes = True

# Schema for POST /candidates
class CandidateCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Full name of the candidate")
    email: EmailStr = Field(..., description="Valid email address")
    position: str = Field(..., min_length=1, max_length=100, description="Position applied for")

# Schema for PATCH /candidates/{id}
class CandidateUpdate(BaseModel):
    status: CandidateStatus

# Basic candidate response without nested data
class CandidateResponseBase(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    position: str
    status: CandidateStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Schema for GET /candidates (with interviews and feedback)
class CandidateResponse(CandidateResponseBase):
    interviews: List[InterviewInCandidate] = []
    
    class Config:
        from_attributes = True
