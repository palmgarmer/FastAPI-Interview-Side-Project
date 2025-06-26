from typing import TYPE_CHECKING
from sqlalchemy import String, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base, create_created_at, create_updated_at
import enum
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from .interview import Interview

class CandidateStatus(enum.Enum):
    APPLIED = "APPLIED"
    INTERVIEWING = "INTERVIEWING"
    HIRED = "HIRED"
    REJECTED = "REJECTED"

class Candidate(Base):
    """Candidate model representing a job applicant."""
    
    __tablename__ = 'candidates'
    
    # UUID primary key (matching your requirements)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Core fields (matching your requirements exactly)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    position: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[CandidateStatus] = mapped_column(Enum(CandidateStatus), default=CandidateStatus.APPLIED)
    
    # Timestamps
    created_at: Mapped[datetime] = create_created_at()
    updated_at: Mapped[datetime] = create_updated_at()
    
    # Relationships
    interviews: Mapped[list['Interview']] = relationship("Interview", back_populates="candidate")
