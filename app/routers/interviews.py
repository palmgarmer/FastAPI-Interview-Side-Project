"""
Interview API Router - Job Interview Management System

Endpoints:
- POST /candidates/{candidate_id}/interviews: Schedule a new interview
- GET /candidates/{candidate_id}/interviews: List all interviews for a candidate
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
import uuid

from app.db import get_db_session
from app.models.candidate import Candidate
from app.models.interview import Interview
from app.models.feedback import Feedback
from app.schemas.interview import InterviewCreate, InterviewResponse

router = APIRouter(prefix="/candidates", tags=["interviews"])


@router.post("/{candidate_id}/interviews", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED)
async def schedule_interview(
    candidate_id: uuid.UUID,
    interview_data: InterviewCreate,
    db: AsyncSession = Depends(get_db_session)
) -> InterviewResponse:
    """Schedule a new interview for a candidate"""
    
    # Check if candidate exists
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Create new interview
    interview = Interview(
        candidate_id=candidate_id,
        interviewer=interview_data.interviewer,
        scheduled_at=interview_data.scheduled_at
    )
    
    db.add(interview)
    await db.commit()
    await db.refresh(interview)
    
    return interview


@router.get("/{candidate_id}/interviews", response_model=List[InterviewResponse])
async def list_candidate_interviews(
    candidate_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
) -> List[InterviewResponse]:
    """List all interviews for a candidate"""
    
    # Check if candidate exists
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Get all interviews for this candidate
    result = await db.execute(
        select(Interview)
        .where(Interview.candidate_id == candidate_id)
        .order_by(Interview.scheduled_at)
    )
    interviews = result.scalars().all()
    
    return interviews
