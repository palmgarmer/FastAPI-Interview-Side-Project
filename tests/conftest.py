"""
Test configuration and fixtures for FastAPI Interview Management System
"""
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db import get_db_session
from app.models import Base


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=StaticPool,
    connect_args={
        "check_same_thread": False,
    },
)

# Test session maker
TestSessionLocal = async_sessionmaker(
    test_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


@pytest_asyncio.fixture
async def db_session():
    """Create a test database session"""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        yield session
    
    # Drop tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def test_client(db_session):
    """Create a test client with dependency override"""
    
    def override_get_db():
        return db_session
    
    app.dependency_overrides[get_db_session] = override_get_db
    
    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def sample_candidate_data():
    """Sample candidate data for testing"""
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "position": "Software Engineer"
    }


@pytest_asyncio.fixture
async def sample_candidate(test_client: AsyncClient, sample_candidate_data):
    """Create a sample candidate for testing"""
    response = await test_client.post("/candidates/", json=sample_candidate_data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def sample_interview_data():
    """Sample interview data for testing"""
    return {
        "interviewer": "Alice Johnson",
        "scheduled_at": "2025-06-30T14:00:00"
    }


@pytest_asyncio.fixture
async def sample_interview(test_client: AsyncClient, sample_candidate, sample_interview_data):
    """Create a sample interview for testing"""
    response = await test_client.post(
        f"/candidates/{sample_candidate['id']}/interviews", 
        json=sample_interview_data
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def sample_feedback_data():
    """Sample feedback data for testing"""
    return {
        "rating": 5,
        "comment": "Excellent technical skills and communication"
    }
