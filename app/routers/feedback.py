"""
Feedback API Router - Job Interview Management System

Endpoints:
- POST /interviews/{interview_id}/feedback: Add feedback to an interview
- GET /interviews/{interview_id}/feedback: Get feedback for an interview

Educational Notes:
- This demonstrates 3-level relationships: Feedback → Interview → Candidate
- Shows proper error handling for nested resources
- Uses validation to ensure data integrity
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db import get_db_session
from app.models.interview import Interview
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackResponse

# Note: We use /interviews prefix since feedback belongs to interviews
router = APIRouter(prefix="/interviews", tags=["feedback"])


# TODO: Implement POST endpoint here
@router.post("/{interview_id}/feedback", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def add_feedback(
    interview_id: int,
    feedback_data: FeedbackCreate,
    db: AsyncSession = Depends(get_db_session)
) -> FeedbackResponse:
    """Add feedback to an interview"""
    
    # Step 1: Check if interview exists
    result = await db.execute(select(Interview).where(Interview.id == interview_id))
    interview = result.scalar_one_or_none()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    # Step 2: Check if feedback already exists (business rule)
    result = await db.execute(select(Feedback).where(Feedback.interview_id == interview_id))
    existing_feedback = result.scalar_one_or_none()
    
    if existing_feedback:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Feedback already exists for this interview"
        )
    
    # Step 3: Create new feedback
    feedback = Feedback(
        interview_id=interview_id,
        rating=feedback_data.rating,
        comment=feedback_data.comment
    )
    
    db.add(feedback)
    await db.commit()
    await db.refresh(feedback)
    
    return feedback


# TODO: Implement GET endpoint here
@router.get("/{interview_id}/feedback", response_model=List[FeedbackResponse])
async def get_interview_feedback(
    interview_id: int,
    db: AsyncSession = Depends(get_db_session)
) -> List[FeedbackResponse]:
    """Get feedback for an interview"""
    
    # Step 1: Check if interview exists
    result = await db.execute(select(Interview).where(Interview.id == interview_id))
    interview = result.scalar_one_or_none()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    # Step 2: Get all feedback for this interview
    result = await db.execute(
        select(Feedback)
        .where(Feedback.interview_id == interview_id)
        .order_by(Feedback.id)
    )
    feedback_list = result.scalars().all()
    
    return feedback_list
