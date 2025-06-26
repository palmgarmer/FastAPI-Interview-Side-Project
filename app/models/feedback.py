from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interview import Interview

class Feedback(Base):
    __tablename__ = "feedback"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Foreign key to interview
    interview_id: Mapped[int] = mapped_column(Integer, ForeignKey("interviews.id"), nullable=False)
    
    # Feedback details (matching your requirements exactly)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5 rating
    comment: Mapped[str] = mapped_column(String(1000), nullable=False)
    
    # Relationships
    interview: Mapped['Interview'] = relationship("Interview", back_populates="feedback")
