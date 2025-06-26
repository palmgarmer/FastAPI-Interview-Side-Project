"""
Candidate API Router - Job Interview Management System

Endpoints:
- POST /candidates: Create a new candidate
- GET /candidates: List all candidates with their interviews
- PATCH /candidates/{id}: Update candidate status
- DELETE /candidates/{id}: Delete a candidate
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
from app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateResponse, CandidateResponseBase

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.post("/", response_model=CandidateResponseBase, status_code=status.HTTP_201_CREATED)
async def create_candidate(
    candidate_data: CandidateCreate,
    db: AsyncSession = Depends(get_db_session)
) -> CandidateResponseBase:
    """Create a new candidate"""
    
    # Check if email already exists
    result = await db.execute(select(Candidate).where(Candidate.email == candidate_data.email))
    existing_candidate = result.scalar_one_or_none()
    
    if existing_candidate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Candidate with this email already exists"
        )
    
    # Create new candidate
    candidate = Candidate(
        name=candidate_data.name,
        email=candidate_data.email,
        position=candidate_data.position
    )
    
    db.add(candidate)
    await db.commit()
    await db.refresh(candidate)
    
    return candidate


@router.get("/", response_model=List[CandidateResponse])
async def list_candidates(
    db: AsyncSession = Depends(get_db_session)
) -> List[CandidateResponse]:
    """List all candidates with their interviews and feedback"""
    
    # Use selectinload to eagerly load interviews and their feedback
    result = await db.execute(
        select(Candidate)
        .options(
            selectinload(Candidate.interviews).selectinload(Interview.feedback)
        )
        .order_by(Candidate.created_at)
    )
    candidates = result.scalars().all()
    
    return candidates


@router.patch("/{candidate_id}", response_model=CandidateResponseBase)
async def update_candidate_status(
    candidate_id: uuid.UUID,
    update_data: CandidateUpdate,
    db: AsyncSession = Depends(get_db_session)
) -> CandidateResponseBase:
    """Update candidate status"""
    
    # Find candidate
    result = await db.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Update status
    candidate.status = update_data.status
    await db.commit()
    await db.refresh(candidate)
    
    return candidate


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    candidate_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """Delete a candidate and all associated interviews and feedback"""
    
    # Find candidate
    result = await db.execute(
        select(Candidate).where(Candidate.id == candidate_id)
    )
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Delete candidate (this will cascade to interviews and feedback due to foreign keys)
    await db.delete(candidate)
    await db.commit()
    
    return None
