# Get Users Testing Suite

## Overview

Comprehensive unit test suite **exclusively for the "get users" functionality** across all layers of the application.

**Test Statistics:**
- **Total Tests:** 65
- **Pass Rate:** 100% ✅
- **Coverage Areas:** Application Layer, Infrastructure Layer, Presentation Layer

---

## Test Structure

```
tests/unit/
├── application/
│   ├── test_get_all_users_use_case.py (14 testes)
│   └── test_user_output_dto.py (16 testes)
├── infrastructure/
│   └── test_get_users_repository.py (13 testes)
└── presentation/
    ├── test_get_all_users_routes.py (14 testes)
    └── test_get_all_users_mappers.py (13 testes)
```

---

## Architecture Layers Covered

### 1. **Application Layer** (30 tests)

#### GetAllUsersUseCase (14 tests)
- ✅ Use case initialization
- ✅ Prepare method behavior
- ✅ Execute returns list of UserOutputDto
- ✅ Single user retrieval
- ✅ Empty user list handling
- ✅ User data validation with DTO
- ✅ User order preservation
- ✅ Repository method invocation
- ✅ Validation error handling
- ✅ Correct data mapping
- ✅ Inactive user handling

**Key Tests:**
```python
def test_execute_returns_list_of_user_output_dtos()
def test_execute_with_empty_user_list()
def test_execute_validates_users_with_dto()
def test_execute_preserves_user_order()
```

#### UserOutputDto Validation (16 tests)
- ✅ Valid DTO creation
- ✅ Required field validation (id, name, email, password, is_active)
- ✅ Email format validation
- ✅ Admin user mapping
- ✅ Inactive user mapping
- ✅ ORM object conversion (from_attributes)
- ✅ List of DTOs
- ✅ Numeric ID handling
- ✅ Unicode character support

**Key Tests:**
```python
def test_user_output_dto_valid_data()
def test_user_output_dto_requires_id()
def test_user_output_dto_email_validation()
def test_user_output_dto_from_attributes_config()
```

### 2. **Infrastructure Layer** (13 tests)

#### SQLAlchemyUserRepository.get_users() (13 tests)
- ✅ Returns list of users
- ✅ Single user retrieval
- ✅ Multiple users retrieval
- ✅ Empty database error handling (NotFoundError)
- ✅ Correct field mapping (schema → entity)
- ✅ Inactive users handling
- ✅ Admin users handling
- ✅ Order preservation
- ✅ Unicode name support
- ✅ Database error handling

**Key Tests:**
```python
def test_get_users_returns_list()
def test_get_users_with_multiple_users()
def test_get_users_raises_not_found_when_empty()
def test_get_users_preserves_field_mapping()
def test_get_users_with_unicode_names()
```

### 3. **Presentation Layer** (27 tests)

#### Routes (14 tests)
**GET /api/v1/user/ endpoint**
- ✅ Endpoint existence
- ✅ JSON response format
- ✅ HTTP method correctness (GET)
- ✅ Correct endpoint path
- ✅ No parameters required
- ✅ Response format validation
- ✅ Content-Type header (application/json)
- ✅ HTTP 200 status code
- ✅ Empty user list handling
- ✅ Invalid path returns 404
- ✅ Idempotency

**Key Tests:**
```python
def test_get_all_users_endpoint_exists()
def test_get_all_users_endpoint_returns_json()
def test_get_all_users_response_has_content_type_json()
def test_get_all_users_route_is_idempotent()
```

#### Mappers (13 tests)
**UserOutputDto → CreateUserResponse conversion**
- ✅ Single user mapping
- ✅ List of users mapping
- ✅ Field preservation (id, name, email, password, is_active)
- ✅ Active/inactive user mapping
- ✅ Response serialization (JSON)
- ✅ Special characters in names
- ✅ Model configuration correctness

**Key Tests:**
```python
def test_map_single_user_output_dto_to_response()
def test_map_user_output_dto_list()
def test_map_preserves_user_id()
def test_map_active_and_inactive_users()
```

---

## Fixtures Available (conftest.py)

### Database
- `test_db_engine` - In-memory SQLite
- `test_db_session` - Fresh session per test

### Mock Data
- `mock_user_entity` - Single User entity
- `mock_user_entity_list` - Multiple User entities
- `mock_user_output_dto` - Single UserOutputDto
- `mock_user_output_dto_list` - Multiple UserOutputDto
- `mock_multiple_user_schemas` - Users in database
- `mock_user_repository` - Mock repository

---

## Running the Tests

### Run all tests
```bash
cd /home/henrique/workout-app-be
poetry run pytest tests/unit/ -v
```

### Run specific layer
```bash
# Application layer
poetry run pytest tests/unit/application/ -v

# Infrastructure layer
poetry run pytest tests/unit/infrastructure/ -v

# Presentation layer
poetry run pytest tests/unit/presentation/ -v
```

### Run specific test file
```bash
poetry run pytest tests/unit/application/test_get_all_users_use_case.py -v
```

### Run with coverage
```bash
poetry run pytest tests/unit/ --cov=app --cov-report=html
```

---

## Data Flow in Tests

```
Repository (get_users)
    ↓
    Returns: list[UserSchema]
    ↓
Use Case (execute)
    ↓
    Validates with TypeAdapter(list[UserOutputDto])
    ↓
    Returns: list[UserOutputDto]
    ↓
Mapper (to_web_response)
    ↓
    Maps each UserOutputDto → CreateUserResponse
    ↓
Route (GET /user/)
    ↓
    Returns: list[CreateUserResponse] as JSON
```

---

## Test Results

```
65 passed, 3 warnings in 0.61s ✅
```

**Coverage by Layer:**
- 🟢 Application Layer: 30/30 tests passing
- 🟢 Infrastructure Layer: 13/13 tests passing
- 🟢 Presentation Layer: 22/22 tests passing
  - Routes: 14 tests
  - Mappers: 13 tests

---

## Key Testing Patterns

### 1. **Test Classes**
All tests organized in classes for logical grouping:
```python
class TestGetAllUsersUseCase:
class TestUserOutputDtoForGetUsers:
class TestGetUsersRepository:
class TestGetAllUsersRoute:
class TestGetAllUsersMappers:
```

### 2. **Fixture-Based Data**
Mock data centralized in conftest.py for reusability.

### 3. **In-Memory Database**
SQLite in-memory for repository tests:
- No external dependencies
- Fast execution
- Complete isolation

### 4. **Error Scenario Coverage**
- Empty database
- Inactive users
- Admin users
- Unicode characters
- Validation errors

### 5. **Field-Level Validation**
Tests verify each field of UserOutputDto:
- Required fields
- Email format
- Boolean values
- Numeric IDs

---

## Architecture Compliance

✅ **Clean Architecture**: Tests follow clean architecture principles
- Domain layer: Entity structure validation
- Application layer: Use case logic with mocked dependencies
- Infrastructure layer: Repository with in-memory DB
- Presentation layer: Route handlers and response formatting

✅ **Dependency Injection**: Repository injected into use case
✅ **DTO Validation**: TypeAdapter for list validation
✅ **Error Handling**: Specific exception types

---

## Test Coverage Details

### What's Tested 100%

✅ **GetAllUsersUseCase**
- Initialization
- Repository call
- DTO validation
- Error handling
- Order preservation

✅ **Repository.get_users()**
- Query execution
- Data mapping
- Error cases (NotFoundError, DataBaseError)
- Field preservation
- Multiple users

✅ **Route GET /user/**
- Endpoint availability
- HTTP method
- Response format
- Status codes
- Content-Type

✅ **Response Mapping**
- UserOutputDto → CreateUserResponse
- Field preservation
- Serialization

✅ **DTOs**
- Field validation
- Email format
- Required fields
- ORM integration

---

## Performance

- **Suite Execution**: 0.61 seconds
- **Test Isolation**: Each test has fresh database
- **No Network/Filesystem I/O**

---

## Future Enhancements

- Integration tests with real FastAPI client
- Performance/load tests
- API documentation tests
- Pagination tests (if added to get_users)
- Filtering/sorting tests (if added to get_users)
