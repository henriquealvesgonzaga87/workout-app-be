# Update User Tests

Comprehensive unit tests for the Update User functionality across all layers of the application.

## Test Structure

```
update_user_tests/
├── application/
│   ├── __init__.py
│   ├── test_user_dtos.py           # DTO validation tests
│   └── test_user_use_cases.py      # Use case business logic tests
├── domain/
│   └── __init__.py                 # Domain layer tests (placeholder)
├── infrastructure/
│   ├── __init__.py
│   └── test_user_repository.py     # Repository/Database layer tests
├── presentation/
│   ├── __init__.py
│   ├── test_user_mappers.py        # Mapper/Converter tests
│   └── test_user_routes.py         # API endpoint tests
└── README.md                        # This file
```

## Layer Coverage

### 1. Application Layer (`application/`)

#### `test_user_dtos.py`
Tests validation and data handling for update user DTOs:
- `UpdateUserDto` - Validates partial updates
- `UserOutputDto` - Validates response DTOs
- Email validation
- Field-by-field updates
- Edge cases (long names, special characters)

**Key Tests:**
- Only updating specific fields (name, email, password)
- Toggling boolean flags (is_active, is_super_admin)
- Handling None values (optional updates)
- Email format validation

#### `test_user_use_cases.py`
Tests the `UpdateUserUseCase` business logic:
- Initialization and dependency injection
- Password hashing in prepare method
- Partial updates implementation
- Error handling (RequestError, ResponseError)
- Return type validation
- Multiple sequential updates

**Key Tests:**
- Password hashing when provided
- Password preservation when None
- Partial field updates
- Correct repository method calls
- Output DTO generation

### 2. Domain Layer (`domain/`)
Placeholder for domain-specific business rule tests. Domain entities are primarily tested through application layer tests.

### 3. Infrastructure Layer (`infrastructure/`)

#### `test_user_repository.py`
Tests the SQLAlchemy repository `update` method:
- Database persistence
- Field-by-field updates
- Partial updates
- Creation_date preservation
- Update_date setting
- Error handling (NotFoundError, IntegrityError)
- Special characters and long strings

**Key Tests:**
- Updating individual fields (name, email, password)
- Toggling boolean flags in database
- Handling non-existent users
- Preventing duplicate emails
- Preserving creation_date on updates
- Data persistence verification

### 4. Presentation Layer (`presentation/`)

#### `test_user_mappers.py`
Tests conversion between API request/response models and DTOs:
- Converting `UpdateUserRequest` → `UpdateUserDto`
- Converting `UserOutputDto` → `CreateUserResponse`
- Setting update_date automatically
- Handling partial updates
- Field preservation through the chain

**Key Tests:**
- Mapper initialization and default values
- None value handling
- Field-by-field mapping
- Complete update chain (request → DTO → response)
- Special characters preservation

#### `test_user_routes.py`
Tests the HTTP endpoints for update user:
- PUT `/api/v1/user/{id}` endpoint
- Valid and invalid payloads
- Error responses (400, 404, 422)
- Partial updates via API
- Request validation
- Response structure

**Key Tests:**
- Endpoint accessibility
- Status codes for success/failure
- Partial updates support
- Email validation
- Invalid user IDs
- Successive and concurrent updates

## Test Execution

### Run all update user tests:
```bash
pytest tests/user_tests/update_user_tests/
```

### Run tests by layer:
```bash
# Application layer
pytest tests/user_tests/update_user_tests/application/

# Infrastructure layer
pytest tests/user_tests/update_user_tests/infrastructure/

# Presentation layer
pytest tests/user_tests/update_user_tests/presentation/
```

### Run specific test file:
```bash
pytest tests/user_tests/update_user_tests/application/test_user_use_cases.py
```

### Run with coverage:
```bash
pytest tests/user_tests/update_user_tests/ --cov=app --cov-report=html
```

## Test Data & Fixtures

Tests use fixtures defined in `tests/user_tests/conftest.py`:
- `test_db_session` - In-memory SQLite database
- `mock_user_entity` - User domain entity
- `mock_user_output_dto` - User output DTO
- `mock_user_schema` - User database schema
- `mock_user_repository` - Mocked repository

## Coverage Summary

### Application Layer
- ✅ DTO validation and transformation
- ✅ Use case initialization
- ✅ Password hashing logic
- ✅ Partial field updates
- ✅ Error handling and wrapping
- ✅ Output generation

### Infrastructure Layer
- ✅ Database update operations
- ✅ Field-level updates
- ✅ Data persistence
- ✅ Error conditions (NotFound, IntegrityError)
- ✅ Special character handling
- ✅ Date field handling

### Presentation Layer
- ✅ Request-to-DTO mapping
- ✅ DTO-to-response mapping
- ✅ HTTP endpoint availability
- ✅ Request validation
- ✅ Response structure
- ✅ Error status codes

## Key Testing Patterns

1. **Partial Updates**: Tests verify that only specified fields are updated
2. **Preservation**: Tests ensure original values are preserved when not updated
3. **Validation**: Tests check input validation at DTO and request levels
4. **Error Handling**: Tests verify proper error wrapping and status codes
5. **Data Persistence**: Tests confirm changes persist in database
6. **Field Coverage**: Tests cover individual field updates and combinations

## Running All Tests

```bash
# Application tests
pytest tests/user_tests/update_user_tests/application/ -v

# Infrastructure tests
pytest tests/user_tests/update_user_tests/infrastructure/ -v

# Presentation tests
pytest tests/user_tests/update_user_tests/presentation/ -v

# All layers with coverage
pytest tests/user_tests/update_user_tests/ --cov=app --cov-report=html -v
```
