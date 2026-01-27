# User Login API - Valid Credentials

## Test Case ID
TC-Auth-001-API

## Test Target
- [x] API Test (Backend endpoint testing - Automation code will be generated)
- [ ] UI Test (Frontend/User interface testing - Manual execution)

## Priority
- [x] P0 (Critical)
- [ ] P1 (High)
- [ ] P2 (Medium)
- [ ] P3 (Low)

## Related Requirements
- PRD Section: 3.2 User Authentication
- EDD Section: 4.1 Authentication API Endpoints
- Functional Requirement: FR-AUTH-001

## Test Objective
Verify that the login API endpoint correctly authenticates users with valid credentials and returns an authentication token.

## Preconditions
- User account exists in the database
- User credentials are valid and active
- API server is running and accessible

## Test Steps

| Step | Action | Expected Result |
|------|--------|------------------|
| 1 | Send POST request to `/api/auth/login` with valid username and password in request body | API accepts the request |
| 2 | Verify response status code | Status code is 200 OK |
| 3 | Verify response contains authentication token | Response body contains `token` field with non-empty string value |
| 4 | Verify response contains user information | Response body contains `user` object with `id`, `username`, and `email` fields |
| 5 | Verify token format | Token is a valid JWT string with expected structure |

## Test Data
- **Username**: `testuser@example.com`
- **Password**: `SecurePassword123!`
- **Expected User ID**: `user-123-abc`
- **Expected Username**: `testuser@example.com`

**Request Body**:
```json
{
  "username": "testuser@example.com",
  "password": "SecurePassword123!"
}
```

**Expected Response Body**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user-123-abc",
    "username": "testuser@example.com",
    "email": "testuser@example.com"
  }
}
```

## Expected Result
- API returns status code 200 OK
- Response contains valid authentication token (JWT format)
- Response contains complete user information
- Token can be used for subsequent authenticated requests

## Postconditions
- User session is created in the system
- Authentication token is valid for the configured duration
- User can use the token to access protected endpoints

## Notes

### Automation Code
This test case will have corresponding automation code generated in the `tests/automation/` directory.

**Important**: The automation code will be written in the **same programming language as the project**:
- Python project → pytest with requests/httpx
- Go project → Go testing with net/http
- Rust project → Rust testing with reqwest
- JavaScript/TypeScript project → Jest/Mocha with axios
- Java project → JUnit with RestAssured

The automation code will reference this test case ID (TC-Auth-001-API) in its comments.

### Related Test Cases
- TC-Auth-002-API: User Login API - Invalid Password
- TC-Auth-003-API: User Login API - Non-existent User
- TC-Auth-004-UI: User Login UI - Form Validation
