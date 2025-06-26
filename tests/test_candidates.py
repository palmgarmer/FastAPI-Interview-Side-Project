"""
Unit tests for candidate endpoints
"""
import pytest
import uuid
from fastapi import status
from httpx import AsyncClient


class TestCandidateCreation:
    """Test candidate creation endpoint"""
    
    @pytest.mark.asyncio
    async def test_create_candidate_success(self, test_client: AsyncClient, sample_candidate_data):
        """Test successful candidate creation"""
        response = await test_client.post("/candidates/", json=sample_candidate_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        # Check response structure
        assert "id" in data
        assert data["name"] == sample_candidate_data["name"]
        assert data["email"] == sample_candidate_data["email"]
        assert data["position"] == sample_candidate_data["position"]
        assert data["status"] == "APPLIED"
        assert "created_at" in data
        assert "updated_at" in data
    
    @pytest.mark.asyncio
    async def test_create_candidate_duplicate_email(self, test_client: AsyncClient, sample_candidate_data):
        """Test duplicate email validation"""
        # Create first candidate
        response = await test_client.post("/candidates/", json=sample_candidate_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Try to create duplicate
        response = await test_client.post("/candidates/", json=sample_candidate_data)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already exists" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_create_candidate_invalid_data(self, test_client: AsyncClient):
        """Test validation errors"""
        invalid_data = {
            "name": "",  # Too short
            "email": "invalid-email",  # Invalid format
            "position": ""  # Too short
        }
        
        response = await test_client.post("/candidates/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestCandidateListing:
    """Test candidate listing endpoint"""
    
    @pytest.mark.asyncio
    async def test_list_empty_candidates(self, test_client: AsyncClient):
        """Test listing when no candidates exist"""
        response = await test_client.get("/candidates/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    @pytest.mark.asyncio
    async def test_list_candidates_with_data(self, test_client: AsyncClient, sample_candidate_data):
        """Test listing candidates with data"""
        # Create a candidate first
        create_response = await test_client.post("/candidates/", json=sample_candidate_data)
        created_candidate = create_response.json()
        
        # List candidates
        response = await test_client.get("/candidates/")
        
        assert response.status_code == status.HTTP_200_OK
        candidates = response.json()
        assert len(candidates) == 1
        assert candidates[0]["id"] == created_candidate["id"]
        assert candidates[0]["interviews"] == []  # No interviews yet


class TestCandidateStatusUpdate:
    """Test candidate status update endpoint"""
    
    @pytest.mark.asyncio
    async def test_update_candidate_status_success(self, test_client: AsyncClient, sample_candidate_data):
        """Test successful status update"""
        # Create candidate
        create_response = await test_client.post("/candidates/", json=sample_candidate_data)
        candidate_id = create_response.json()["id"]
        
        # Update status
        update_data = {"status": "INTERVIEWING"}
        response = await test_client.patch(f"/candidates/{candidate_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "INTERVIEWING"
        assert data["updated_at"] != data["created_at"]  # Should be different
    
    @pytest.mark.asyncio
    async def test_update_nonexistent_candidate(self, test_client: AsyncClient):
        """Test updating non-existent candidate"""
        fake_id = str(uuid.uuid4())
        update_data = {"status": "HIRED"}
        
        response = await test_client.patch(f"/candidates/{fake_id}", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    @pytest.mark.asyncio
    async def test_update_invalid_status(self, test_client: AsyncClient, sample_candidate_data):
        """Test invalid status update"""
        # Create candidate
        create_response = await test_client.post("/candidates/", json=sample_candidate_data)
        candidate_id = create_response.json()["id"]
        
        # Try invalid status
        update_data = {"status": "INVALID_STATUS"}
        response = await test_client.patch(f"/candidates/{candidate_id}", json=update_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestCandidateDeletion:
    """Test candidate deletion endpoint"""
    
    @pytest.mark.asyncio
    async def test_delete_candidate_success(self, test_client: AsyncClient, sample_candidate_data):
        """Test successful candidate deletion"""
        # Create candidate
        create_response = await test_client.post("/candidates/", json=sample_candidate_data)
        candidate_id = create_response.json()["id"]
        
        # Delete candidate
        response = await test_client.delete(f"/candidates/{candidate_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify deletion
        response = await test_client.get("/candidates/")
        assert response.json() == []
    
    @pytest.mark.asyncio
    async def test_delete_nonexistent_candidate(self, test_client: AsyncClient):
        """Test deleting non-existent candidate"""
        fake_id = str(uuid.uuid4())
        
        response = await test_client.delete(f"/candidates/{fake_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
