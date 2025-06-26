# Job Interview Management System API

A comprehensive FastAPI-based interview management system built with SQLAlchemy 2.0 and SQLite.

## 🎯 Project Overview

This project implements a complete Job Interview Management System API that manages:
- **Candidates** - Job applicants with status lifecycle
- **Interviews** - Scheduled interview sessions
- **Feedback** - Interview feedback and ratings

## 🚀 Features

- **Async FastAPI** with SQLAlchemy 2.0
- **Complete CRUD operations** for all entities
- **Nested relationships** - Candidates with interviews and feedback
- **Email uniqueness** validation
- **Comprehensive error handling** (404, 409, 422)
- **Full test coverage** with pytest and async testing
- **Type hints** throughout the codebase
- **Pydantic validation** for all inputs

## 📋 Requirements Met

### Models (SQLAlchemy 2.0)
- ✅ **Candidate**: UUID primary key, name, unique email, position, status enum
- ✅ **Interview**: Integer primary key, candidate foreign key, interviewer, scheduled_at, optional result
- ✅ **Feedback**: Integer primary key, interview foreign key, rating (1-5), comment

### API Endpoints
- ✅ `POST /candidates` - Create candidate
- ✅ `GET /candidates` - List all candidates with interviews and feedback
- ✅ `PATCH /candidates/{id}` - Update candidate status
- ✅ `DELETE /candidates/{id}` - Delete candidate
- ✅ `POST /candidates/{id}/interviews` - Schedule interview
- ✅ `GET /candidates/{id}/interviews` - List candidate's interviews
- ✅ `POST /interviews/{id}/feedback` - Submit feedback
- ✅ `GET /interviews/{id}/feedback` - View feedback

### Technical Constraints
- ✅ **Async/await** throughout
- ✅ **Type hinting** on all functions
- ✅ **Pydantic models** with validation
- ✅ **Email uniqueness** enforced
- ✅ **SQLite database** with async driver
- ✅ **SQLAlchemy 2.0** with proper relationships
- ✅ **404 error handling** for all endpoints

### Unit Tests
- ✅ **26 comprehensive tests** covering all functionality
- ✅ Candidate creation, listing, status updates, deletion
- ✅ Interview scheduling and listing
- ✅ Feedback submission and retrieval
- ✅ **Test database** (in-memory SQLite)
- ✅ **Edge cases** and error scenarios

## 🛠️ Installation & Setup

1. **Clone the repository**:
```bash
git clone https://github.com/palmgarmer/FastAPI-Interview-Side-Project.git
cd FastAPI-Interview-Side-Project
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
uvicorn app.main:app --reload --port 8000
```

5. **Access the API**:
- **API Documentation**: http://127.0.0.1:8000/docs
- **Alternative docs**: http://127.0.0.1:8000/redoc

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=app

# Run specific test file
python -m pytest tests/test_candidates.py -v
```

## 📁 Project Structure

```
FastAPI-Interview-Side-Project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app instance
│   ├── db.py                   # Database configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── candidate.py        # Candidate model
│   │   ├── interview.py        # Interview model
│   │   └── feedback.py         # Feedback model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── candidate.py        # Candidate Pydantic schemas
│   │   ├── interview.py        # Interview Pydantic schemas
│   │   └── feedback.py         # Feedback Pydantic schemas
│   └── routers/
│       ├── __init__.py
│       ├── candidates.py       # Candidate endpoints
│       ├── interviews.py       # Interview endpoints
│       └── feedback.py         # Feedback endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Test configuration
│   ├── test_candidates.py     # Candidate tests
│   ├── test_interviews.py     # Interview tests
│   └── test_feedback.py       # Feedback tests
├── requirements.txt
├── README.md
└── candidates.db              # SQLite database file
```

## 🔗 API Endpoints

### Candidates
- `POST /candidates/` - Create a new candidate
- `GET /candidates/` - List all candidates with interviews and feedback
- `PATCH /candidates/{id}` - Update candidate status
- `DELETE /candidates/{id}` - Delete candidate

### Interviews
- `POST /candidates/{id}/interviews` - Schedule interview for candidate
- `GET /candidates/{id}/interviews` - List candidate's interviews

### Feedback
- `POST /interviews/{id}/feedback` - Submit interview feedback
- `GET /interviews/{id}/feedback` - Get interview feedback

## 📊 Example Usage

### Create a candidate:
```bash
curl -X POST "http://127.0.0.1:8000/candidates/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "position": "Software Engineer"
  }'
```

### Schedule an interview:
```bash
curl -X POST "http://127.0.0.1:8000/candidates/{candidate_id}/interviews" \
  -H "Content-Type: application/json" \
  -d '{
    "interviewer": "Alice Johnson",
    "scheduled_at": "2025-06-30T14:00:00"
  }'
```

### Submit feedback:
```bash
curl -X POST "http://127.0.0.1:8000/interviews/{interview_id}/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Excellent technical skills and communication"
  }'
```

## 🎯 Key Features Implemented

1. **Async Architecture**: Full async/await with SQLAlchemy 2.0
2. **Proper Relationships**: Candidates → Interviews → Feedback with eager loading
3. **Status Lifecycle**: Candidate status enum (APPLIED, INTERVIEWING, HIRED, REJECTED)
4. **Validation**: Email format, rating ranges (1-5), required fields
5. **Error Handling**: 404 (not found), 409 (conflicts), 422 (validation)
6. **Test Coverage**: 26 tests covering all endpoints and edge cases
7. **Database Design**: Proper foreign keys, unique constraints, UUIDs

## 🔧 Technologies Used

- **FastAPI** - Modern async web framework
- **SQLAlchemy 2.0** - ORM with async support
- **Pydantic** - Data validation and serialization
- **SQLite** - Lightweight database with aiosqlite
- **pytest** - Testing framework with async support
- **httpx** - Async HTTP client for testing

## 📈 Test Coverage

- **26 tests** with 100% endpoint coverage
- **Candidate operations**: Creation, listing, updates, deletion
- **Interview management**: Scheduling, listing
- **Feedback system**: Submission, retrieval
- **Error scenarios**: 404s, duplicates, validation errors
- **Edge cases**: Boundary values, empty data

---

Built with ❤️ using FastAPI and SQLAlchemy 2.0
