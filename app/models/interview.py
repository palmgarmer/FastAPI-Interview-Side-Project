from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from .candidate import Candidate
    from .feedback import Feedback

class Interview(Base):
    __tablename__ = "interviews"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Foreign key to candidate (UUID)
    candidate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False)
    
    # Interview details (matching your requirements exactly)
    interviewer: Mapped[str] = mapped_column(String(100), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    candidate: Mapped['Candidate'] = relationship("Candidate", back_populates="interviews")
    feedback: Mapped[list['Feedback']] = relationship("Feedback", back_populates="interview")