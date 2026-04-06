# Delete User Tests

This directory contains comprehensive unit tests for the delete user functionality across all layers of the application architecture.

## Test Structure

The tests are organized following the clean architecture pattern with tests for each layer:

### 1. Application Layer (`application/`)
**File:** `test_user_use_cases.py`

Tests the `DeleteUserUseCase` class, which contains the business logic for user deletion.

**Key Test Cases:**
- ✅ Use case initialization
- ✅ ID preparation and validation (integer conversion, type checking)
- ✅ Invalid ID handling (non-integer strings, None, floats, etc.)
- ✅ Successful user deletion execution
- ✅ Return value validation (always returns boolean True)
- ✅ Error propagation (RequestError, ResponseError)
- ✅ Boundary values (zero, negative IDs)
- ✅ Multiple sequential deletions

**Total Test Cases:** 18

### 2. Infrastructure Layer (`infrastructure/`)
**File:** `test_user_repository.py`

Tests the `SQLAlchemyUserRepository.delete()` method, which handles database operations.

**Key Test Cases:**
- ✅ Repository initialization
- ✅ Successful user deletion from database
- ✅ Return value validation (returns True)
- ✅ Database state verification (user removed)
- ✅ Non-existent user handling (NotFoundError)
- ✅ Multiple user deletions
- ✅ Already-deleted user handling (idempotency)
- ✅ Edge cases (zero ID, negative ID)
- ✅ Special user types (admin users, inactive users)
- ✅ Sequential user deletions with correct ID matching

**Total Test Cases:** 13

### 3. Presentation Layer (`presentation/`)

#### Routes Tests
**File:** `test_user_routes.py`

Tests the DELETE `/api/v1/user/{id}` endpoint behavior.

**Key Test Cases:**
- ✅ Endpoint existence
- ✅ Valid ID handling
- ✅ Invalid ID format handling (strings, floats, special characters)
- ✅ No ID provided (missing endpoint)
- ✅ HTTP 204 NO_CONTENT response for successful deletion
- ✅ HTTP method validation (DELETE vs other methods)
- ✅ Sequential deletions
- ✅ Edge cases (ID=0, negative IDs)
- ✅ Boundary values (large IDs)
- ✅ Content-type header handling
- ✅ Idempotent behavior
- ✅ API documentation

**Total Test Cases:** 16

#### Error Handler Tests
**File:** `test_error_handlers.py`

Tests error handling and error propagation in delete operations.

**Key Test Cases:**
- ✅ RequestError handling (invalid input)
- ✅ ResponseError handling (validation errors)
- ✅ NotFoundError handling (user not found)
- ✅ DataBaseError handling (DB connection issues)
- ✅ Error message formatting and clarity
- ✅ Error type distinction (RequestError vs ResponseError)
- ✅ Multiple sequential errors
- ✅ Error recovery
- ✅ Error isolation between calls
- ✅ Boundary value error handling
- ✅ Unknown type error handling (dict, objects, etc.)

**Total Test Cases:** 17

## Running the Tests

### Run all delete user tests:
```bash
pytest tests/user_tests/delete_user_tests/ -v
```

### Run specific layer tests:
```bash
# Application layer only
pytest tests/user_tests/delete_user_tests/application/ -v

# Infrastructure layer only
pytest tests/user_tests/delete_user_tests/infrastructure/ -v

# Presentation layer only
pytest tests/user_tests/delete_user_tests/presentation/ -v
```

### Run tests with coverage:
```bash
pytest tests/user_tests/delete_user_tests/ --cov=app.application.user.use_cases.delete_user_use_case --cov=app.infrastructure.repositories.sqlalchemy.user.user_repo --cov=app.presentation.routes.user.user_routes -v
```

### Run specific test class:
```bash
pytest tests/user_tests/delete_user_tests/application/test_user_use_cases.py::TestDeleteUserUseCase -v
```

### Run specific test:
```bash
pytest tests/user_tests/delete_user_tests/application/test_user_use_cases.py::TestDeleteUserUseCase::test_execute_deletes_user_successfully -v
```

## Test Coverage Summary

| Layer | File | Test Class | # Tests |
|-------|------|-----------|---------|
| Application | test_user_use_cases.py | TestDeleteUserUseCase | 18 |
| Infrastructure | test_user_repository.py | TestSQLAlchemyUserRepositoryDelete | 13 |
| Presentation | test_user_routes.py | TestDeleteUserRoutes | 16 |
| Presentation | test_error_handlers.py | TestDeleteUserErrorHandling | 17 |
| **Total** | | | **64** |

## Fixtures Used

All tests utilize fixtures from the parent `conftest.py`:

- `test_db_engine` - In-memory SQLite database
- `test_db_session` - Database session for tests
- `mock_user_repository` - Mocked user repository
- `mock_user_entity` - Sample User entity
- `mock_user_output_dto` - Sample output DTO

## Architecture Layers Tested

### 1. Domain Layer
- User entity structure and validation (tested implicitly)

### 2. Application Layer
- Business logic for deletion (use case)
- Input validation and preparation
- Error handling strategy

### 3. Infrastructure Layer
- Database operations (SQLAlchemy)
- Data persistence
- Transaction management

### 4. Presentation Layer
- HTTP endpoint handling
- Route mapping
- Error response formatting
- HTTP status codes

## Key Test Patterns

### Successful Operation
```python
def test_execute_deletes_user_successfully(self, mock_user_repository):
    mock_user_repository.delete.return_value = True
    use_case = DeleteUserUseCase(user_repository=mock_user_repository)
    result = use_case.execute(id=1)
    assert result is True
```

### Error Handling
```python
def test_delete_non_existent_user_raises_error(self, test_db_session):
    repo = SQLAlchemyUserRepository(db_session=test_db_session)
    with pytest.raises(NotFoundError):
        repo.delete(id=99999)
```

### Edge Cases
```python
def test_execute_with_zero_id(self, mock_user_repository):
    use_case = DeleteUserUseCase(user_repository=mock_user_repository)
    result = use_case.execute(id=0)
    assert result is True
```

## Dependencies

- `pytest` - Test framework
- `pytest-cov` - Coverage plugin
- `sqlalchemy` - ORM for database testing
- `fastapi` - Web framework
- `unittest.mock` - Mocking utilities

## Notes

- All tests use in-memory SQLite database for isolation
- Each test is independent and doesn't affect others
- Tests use both mocks and real database operations for comprehensive coverage
- Error scenarios are tested to ensure proper error propagation
- Edge cases and boundary values are validated

## Future Enhancements

- Integration tests with real database
- Performance tests for bulk deletions
- Concurrent deletion testing
- Audit logging verification
- Soft delete vs hard delete testing
