# Test Suite Documentation

## Overview

Complete unit test suite for the Workout App Backend covering all layers of the architecture.

**Test Statistics:**
- **Total Tests:** 112
- **Pass Rate:** 100%
- **Coverage Areas:** DTOs, Use Cases, Repositories, Error Handlers, Mappers, Routes, Utilities

## Test Structure

```
tests/
├── conftest.py                 # Fixtures and mock data
├── unit/
│   ├── application/
│   │   ├── test_user_dtos.py       # DTO validation tests (17 tests)
│   │   └── test_user_use_cases.py  # Use case business logic tests (16 tests)
│   ├── infrastructure/
│   │   └── test_user_repository.py # Repository & DB tests (14 tests)
│   ├── presentation/
│   │   ├── test_user_mappers.py    # Mapper tests (8 tests)
│   │   ├── test_error_handlers.py  # Error handling tests (29 tests)
│   │   └── test_user_routes.py     # Route integration tests (20 tests)
│   └── test_hash_utils.py          # Password hashing tests (16 tests)
```

## Fixtures and Mock Data

The `conftest.py` provides comprehensive fixtures:

### Database Fixtures
- `test_db_engine` - In-memory SQLite database
- `test_db_session` - Fresh SQLAlchemy session per test

### User Entity Fixtures
- `mock_user_entity` - Single User entity
- `mock_user_entity_list` - List of User entities
- `mock_user_schema` - UserSchema persisted in DB
- `mock_multiple_user_schemas` - Multiple persisted users

### DTO Fixtures
- `mock_create_user_dto` - CreateUserDto instance
- `mock_user_output_dto` - UserOutputDto instance
- `mock_user_output_dto_list` - List of output DTOs

### Repository Fixtures
- `mock_user_repository` - Mock repository
- `mock_user_repository_with_user` - Mock returning single user
- `mock_user_repository_with_users` - Mock returning multiple users

## Test Coverage by Layer

### Domain Layer
- User entity dataclass structures

### Application Layer

**DTOs (test_user_dtos.py):**
- CreateUserDto validation
- UserOutputDto validation
- Email format validation
- Required field validation
- Default value handling

**Use Cases (test_user_use_cases.py):**
- CreateUserUseCase
  - Password hashing
  - User creation
  - Data preservation
  - Error handling
- GetAllUsersUseCase
  - User list retrieval
  - DTO validation
  - Empty list handling
  - Order preservation

### Infrastructure Layer

**Repositories (test_user_repository.py):**
- User creation with generated IDs
- Bulk user creation
- User retrieval from database
- Duplicate email detection (IntegrityError)
- Empty database handling (NotFoundError)
- Correct data mapping from schema to entity

### Presentation Layer

**Mappers (test_user_mappers.py):**
- Request to DTO conversion
- DTO to response conversion
- Round-trip mapping validation
- Various email format handling

**Error Handlers (test_error_handlers.py):**
- ResponseError (500 status)
- RequestError (400 status)
- IntegrityError (409 status)
- Error message preservation

**Routes (test_user_routes.py):**
- Endpoint existence validation
- Request validation
- Missing field handling
- Invalid email format rejection
- Status code verification
- Response content type checking

### Utilities (test_hash_utils.py):**
- Password hashing with argon2
- Password verification
- Hash security properties
- Special character handling
- Long password support

## Running Tests

### Run all tests
```bash
poetry run pytest tests/unit/ -v
```

### Run specific test file
```bash
poetry run pytest tests/unit/application/test_user_dtos.py -v
```

### Run specific test class
```bash
poetry run pytest tests/unit/application/test_user_use_cases.py::TestCreateUserUseCase -v
```

### Run with coverage report
```bash
poetry run pytest tests/unit/ --cov=app --cov-report=html
```

### Run with detailed output
```bash
poetry run pytest tests/unit/ -vv --tb=short
```

## Technology Stack

- **Test Framework:** pytest 9.0.2
- **Database (Tests):** SQLite in-memory
- **Mocking:** unittest.mock
- **Data Validation:** Pydantic v2

## In-Memory Database Strategy

Repository tests use an in-memory SQLite database created fresh for each test:
- No external dependencies
- Fast test execution
- Complete isolation between tests
- Full ACID compliance for transaction testing

## Key Testing Patterns

### 1. Test Classes Over Functions
All tests organized in classes for logical grouping and shared setup.

### 2. Descriptive Test Names
Test method names clearly describe what is being tested:
```python
def test_execute_validates_users_with_dto(self):
    """Verifies validation of user list using UserOutputDto."""
```

### 3. Fixture-Based Data
Mock data stored in conftest.py for reusability and maintainability.

### 4. Mocking Boundaries
- Mocks used for external dependencies (repositories)
- Real implementations tested where appropriate (DTOs, mappers)
- In-memory DB for repository tests

### 5. Comprehensive Assertions
Tests verify:
- Return types and values
- Exception raising
- Side effects (data persistence)
- Edge cases and error conditions

## Architecture Compliance

Tests follow the Clean Architecture principles:
- **Domain Tests:** Entity structure validation
- **Application Tests:** Use case logic with mocked dependencies
- **Infrastructure Tests:** Repository with in-memory DB
- **Presentation Tests:** Route handlers and error formatting

## Future Enhancements

- Add integration tests with FastAPI TestClient
- Add performance/load tests
- Add mutation testing
- Add parameterized tests for edge cases
- Add API documentation tests

## Troubleshooting

### Tests failing with "file not found"
Ensure you're running pytest from the project root directory.

### PyCache issues
Delete `.pytest_cache` and `__pycache__` directories:
```bash
find . -type d -name __pycache__ -delete
rm -rf .pytest_cache
```

### Database lock issues
Tests use in-memory SQLite, which should clean up automatically. If issues persist, restart the test runner.
