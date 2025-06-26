from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, Text
from datetime import datetime
from typing import Optional


class Base(AsyncAttrs, DeclarativeBase):
    """Base model class with async support for SQLAlchemy 2.0"""
    pass


def create_id_pk():
    return mapped_column(Integer, primary_key=True, index=True)

def create_created_at():
    return mapped_column(DateTime, default=datetime.utcnow)

def create_updated_at():
    return mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
