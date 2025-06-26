"""
Unit tests for Feedback API endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_feedback_success(test_client: AsyncClient, sample_interview):
    """Test successful feedback addition"""
    feedback_data = {
        "rating": 4,
        "comment": "Great technical skills, good communication. Needs improvement in system design."
    }
    
    response = await test_client.post(
        f"/interviews/{sample_interview['id']}/feedback",
        json=feedback_data
    )
    
    assert response.status_code == 201
    data = response.json()
    
    # Verify feedback data
    assert data["rating"] == feedback_data["rating"]
    assert data["comment"] == feedback_data["comment"]
    assert data["interview_id"] == sample_interview["id"]
    assert "id" in data


@pytest.mark.asyncio
async def test_add_feedback_interview_not_found(test_client: AsyncClient):
    """Test adding feedback to non-existent interview"""
    fake_interview_id = 99999
    
    feedback_data = {
        "rating": 4,
        "comment": "Great technical skills"
    }
    
    response = await test_client.post(
        f"/interviews/{fake_interview_id}/feedback",
        json=feedback_data
    )
    
    assert response.status_code == 404
    assert "Interview not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_add_feedback_duplicate(test_client: AsyncClient, sample_interview):
    """Test adding duplicate feedback to same interview"""
    feedback_data = {
        "rating": 4,
        "comment": "Great technical skills"
    }
    
    # Add first feedback
    response1 = await test_client.post(
        f"/interviews/{sample_interview['id']}/feedback",
        json=feedback_data
    )
    assert response1.status_code == 201
    
    # Try to add second feedback to same interview
    response2 = await test_client.post(
        f"/interviews/{sample_interview['id']}/feedback",
        json=feedback_data
    )
    
    assert response2.status_code == 409
    assert "Feedback already exists" in response2.json()["detail"]


@pytest.mark.asyncio
async def test_add_feedback_validation_error(test_client: AsyncClient, sample_interview):
    """Test feedback addition with invalid data"""
    # Test invalid rating
    feedback_data = {
        "rating": 6,  # Rating should be 1-5
        "comment": "Good candidate"
    }
    
    response = await test_client.post(
        f"/interviews/{sample_interview['id']}/feedback",
        json=feedback_data
    )
    
    assert response.status_code == 422
    
    # Test empty comment
    feedback_data = {
        "rating": 4,
        "comment": ""  # Empty comment
    }
    
    response = await test_client.post(
        f"/interviews/{sample_interview['id']}/feedback",
        json=feedback_data
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_interview_feedback_success(test_client: AsyncClient, sample_interview):
    """Test successful feedback retrieval"""
    # First add feedback
    feedback_data = {
        "rating": 5,
        "comment": "Excellent candidate, strong technical skills and great cultural fit."
    }
    
    add_response = await test_client.post(
        f"/interviews/{sample_interview['id']}/feedback",
        json=feedback_data
    )
    assert add_response.status_code == 201
    
    # Get feedback
    response = await test_client.get(f"/interviews/{sample_interview['id']}/feedback")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should have 1 feedback item
    assert len(data) == 1
    assert data[0]["rating"] == feedback_data["rating"]
    assert data[0]["comment"] == feedback_data["comment"]
    assert data[0]["interview_id"] == sample_interview["id"]


@pytest.mark.asyncio
async def test_get_interview_feedback_empty(test_client: AsyncClient, sample_interview):
    """Test getting feedback for interview with no feedback"""
    response = await test_client.get(f"/interviews/{sample_interview['id']}/feedback")
    
    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.asyncio
async def test_get_interview_feedback_interview_not_found(test_client: AsyncClient):
    """Test getting feedback for non-existent interview"""
    fake_interview_id = 99999
    
    response = await test_client.get(f"/interviews/{fake_interview_id}/feedback")
    
    assert response.status_code == 404
    assert "Interview not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_rating_boundary_values(test_client: AsyncClient, sample_interview):
    """Test feedback rating boundary values (1 and 5)"""
    # Test minimum rating
    feedback_data_min = {
        "rating": 1,
        "comment": "Needs significant improvement"
    }
    
    response = await test_client.post(
        f"/interviews/{sample_interview['id']}/feedback",
        json=feedback_data_min
    )
    assert response.status_code == 201
    
    # Create a new interview for the second test (since feedback is unique per interview)
    interview_data = {
        "interviewer": "Test Interviewer 2",
        "scheduled_at": "2025-07-01T10:00:00"
    }
    
    # We need a candidate ID, let's create one
    candidate_data = {
        "name": "Test Candidate 2",
        "email": "test2@example.com",
        "position": "Test Position 2"
    }
    
    candidate_response = await test_client.post("/candidates/", json=candidate_data)
    candidate_id = candidate_response.json()["id"]
    
    interview_response = await test_client.post(
        f"/candidates/{candidate_id}/interviews",
        json=interview_data
    )
    interview_id = interview_response.json()["id"]
    
    # Test maximum rating
    feedback_data_max = {
        "rating": 5,
        "comment": "Outstanding performance"
    }
    
    response = await test_client.post(
        f"/interviews/{interview_id}/feedback",
        json=feedback_data_max
    )
    assert response.status_code == 201
    
    # Verify both feedbacks
    assert response.json()["rating"] == 5


@pytest.mark.asyncio
async def test_feedback_comment_length(test_client: AsyncClient, sample_interview):
    """Test feedback comment length validation"""
    # Test very long comment (should be acceptable as max is 1000 chars)
    long_comment = "A" * 500  # 500 characters should be fine
    
    feedback_data = {
        "rating": 3,
        "comment": long_comment
    }
    
    response = await test_client.post(
        f"/interviews/{sample_interview['id']}/feedback",
        json=feedback_data
    )
    
    assert response.status_code == 201
    assert response.json()["comment"] == long_comment
