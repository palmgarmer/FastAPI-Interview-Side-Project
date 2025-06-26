"""
Unit tests for Interview API endpoints
"""
import pytest
from datetime import datetime
from httpx import AsyncClient

from app.models.candidate import CandidateStatus


@pytest.mark.asyncio
async def test_schedule_interview_success(test_client: AsyncClient, sample_candidate):
    """Test successful interview scheduling"""
    # Create an interview
    interview_data = {
        "interviewer": "Alice Johnson",
        "scheduled_at": "2025-06-30T14:00:00"
    }
    
    response = await test_client.post(
        f"/candidates/{sample_candidate['id']}/interviews",
        json=interview_data
    )
    
    assert response.status_code == 201
    data = response.json()
    
    # Verify interview data
    assert data["interviewer"] == interview_data["interviewer"]
    assert data["scheduled_at"] == interview_data["scheduled_at"]
    assert data["candidate_id"] == sample_candidate["id"]
    assert data["result"] is None
    assert "id" in data


@pytest.mark.asyncio
async def test_schedule_interview_candidate_not_found(test_client: AsyncClient):
    """Test scheduling interview for non-existent candidate"""
    import uuid
    fake_candidate_id = str(uuid.uuid4())
    
    interview_data = {
        "interviewer": "Alice Johnson",
        "scheduled_at": "2025-06-30T14:00:00"
    }
    
    response = await test_client.post(
        f"/candidates/{fake_candidate_id}/interviews",
        json=interview_data
    )
    
    assert response.status_code == 404
    assert "Candidate not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_schedule_interview_validation_error(test_client: AsyncClient, sample_candidate):
    """Test interview scheduling with invalid data"""
    interview_data = {
        "interviewer": "",  # Empty interviewer name
        "scheduled_at": "invalid-date"  # Invalid date format
    }
    
    response = await test_client.post(
        f"/candidates/{sample_candidate['id']}/interviews",
        json=interview_data
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_candidate_interviews_success(test_client: AsyncClient, sample_candidate):
    """Test successful listing of candidate interviews"""
    # First create some interviews
    interview_data_1 = {
        "interviewer": "Alice Johnson",
        "scheduled_at": "2025-06-30T14:00:00"
    }
    interview_data_2 = {
        "interviewer": "Bob Wilson",
        "scheduled_at": "2025-07-02T10:30:00"
    }
    
    # Create interviews
    await test_client.post(
        f"/candidates/{sample_candidate['id']}/interviews",
        json=interview_data_1
    )
    await test_client.post(
        f"/candidates/{sample_candidate['id']}/interviews",
        json=interview_data_2
    )
    
    # List interviews
    response = await test_client.get(f"/candidates/{sample_candidate['id']}/interviews")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should have 2 interviews
    assert len(data) == 2
    
    # Verify they're ordered by scheduled_at
    assert data[0]["scheduled_at"] <= data[1]["scheduled_at"]
    
    # Verify interview data
    assert data[0]["interviewer"] == "Alice Johnson"
    assert data[1]["interviewer"] == "Bob Wilson"


@pytest.mark.asyncio
async def test_list_candidate_interviews_empty(test_client: AsyncClient, sample_candidate):
    """Test listing interviews for candidate with no interviews"""
    response = await test_client.get(f"/candidates/{sample_candidate['id']}/interviews")
    
    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.asyncio
async def test_list_candidate_interviews_candidate_not_found(test_client: AsyncClient):
    """Test listing interviews for non-existent candidate"""
    import uuid
    fake_candidate_id = str(uuid.uuid4())
    
    response = await test_client.get(f"/candidates/{fake_candidate_id}/interviews")
    
    assert response.status_code == 404
    assert "Candidate not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_schedule_multiple_interviews_same_candidate(test_client: AsyncClient, sample_candidate):
    """Test scheduling multiple interviews for the same candidate"""
    interviews = [
        {
            "interviewer": "Technical Interviewer 1",
            "scheduled_at": "2025-06-30T09:00:00"
        },
        {
            "interviewer": "Technical Interviewer 2", 
            "scheduled_at": "2025-06-30T11:00:00"
        },
        {
            "interviewer": "HR Manager",
            "scheduled_at": "2025-06-30T15:00:00"
        }
    ]
    
    created_interviews = []
    for interview_data in interviews:
        response = await test_client.post(
            f"/candidates/{sample_candidate['id']}/interviews",
            json=interview_data
        )
        assert response.status_code == 201
        created_interviews.append(response.json())
    
    # Verify all interviews were created with unique IDs
    interview_ids = [interview["id"] for interview in created_interviews]
    assert len(set(interview_ids)) == 3  # All IDs should be unique
    
    # Verify we can list all interviews
    response = await test_client.get(f"/candidates/{sample_candidate['id']}/interviews")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
