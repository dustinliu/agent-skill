# Integration Test Guide

## Overview

Integration tests verify that different components of a system work together correctly. As a QA engineer performing Black Box Testing, you focus on testing the system from an external perspective without examining source code.

## Black Box Testing Principles

1. **No Source Code Access**: Do not read or analyze source code. Test based on PRD requirements and EDD specifications.
2. **External Perspective**: Test the system as an end user or external system would interact with it.
3. **Requirement-Based**: All tests must be traceable to PRD functional requirements and EDD design specifications.

## Test Planning from PRD and EDD

### Extracting Test Requirements from PRD

1. **Identify Functional Requirements**: Extract all functional requirements (FR-XXX) from PRD
2. **Map User Stories**: For each user story, identify test scenarios
3. **Identify Acceptance Criteria**: Each acceptance criterion should have corresponding test cases
4. **Non-Functional Requirements**: Note performance, security, and usability requirements for test planning

### Extracting Test Requirements from EDD

1. **API Endpoints**: Identify all API endpoints and their expected behaviors
2. **Data Models**: Understand data structures and relationships for test data preparation
3. **System Boundaries**: Understand integration points between components
4. **Error Handling**: Note expected error responses and status codes

### Categorizing Test Scenarios by Test Target

After identifying test scenarios from PRD and EDD, categorize them by test target:

**API Test** - Testing backend endpoints and business logic:
- API endpoint functionality (HTTP methods, status codes, response structure)
- Data validation and processing
- Authentication and authorization
- Error handling and edge cases
- Integration between backend components

**UI Test** - Testing user interface and interactions:
- User interface elements and layout
- Form validation and user input
- Navigation and user flows
- Visual presentation and responsive design
- Error message display

**Important**: Also identify the project's tech stack (check `package.json`, `go.mod`, `Cargo.toml`, etc.) to select the appropriate testing framework later.

## Test Case Design

### Test Case Structure

Use the Test Case template in `assets/test_case_template.md` for consistent documentation.

### Test Case Categories

1. **Happy Path Tests**: Verify normal operation with valid inputs
2. **Negative Tests**: Verify error handling with invalid inputs
3. **Boundary Tests**: Test edge cases and boundary conditions
4. **Integration Tests**: Verify component interactions
5. **Regression Tests**: Ensure existing functionality still works

### Test Data Management

- Use realistic test data that matches EDD data models
- Prepare both valid and invalid test data sets
- Consider edge cases: empty values, null values, maximum lengths, special characters

## API vs UI Testing Decision

The decision of what to test is based on the **test target** (what you're testing), not the execution method (how you test it).

### API Test → Automation Code
**API tests** focus on backend endpoints and business logic. These tests are automated because:
- HTTP requests/responses are easily automated
- Tests are repeatable and deterministic
- Suitable for regression testing
- Can be integrated into CI/CD pipelines

**When to use API Test:**
- Testing backend API endpoints
- Data validation and processing
- Business logic verification
- Authentication and authorization flows
- Error handling and edge cases

**Automation code language:** Must match the project's programming language (Python, Go, Rust, JavaScript/TypeScript, Java, etc.)

### UI Test → Manual Test Case
**UI tests** focus on user interface and user experience. These are manual because:
- Visual verification requires human judgment
- UI/UX testing involves subjective assessment
- Complex user flows need contextual understanding

**When to use UI Test:**
- Testing user interface elements
- Visual verification (layout, styling, responsive design)
- User interaction flows
- Form validation and error message display
- Navigation and user experience

## Automation Test Implementation

### Location
Place automation test scripts/code in `tests/automation/` directory at project root.

### Best Practices

1. **Framework Selection**:

   **Important Principle**: Automation test code MUST use the same programming language as the project.

   **Steps to select framework:**
   - **Identify project tech stack**: Check configuration files like `package.json`, `go.mod`, `Cargo.toml`, `pom.xml`, `requirements.txt`
   - **Choose corresponding testing framework**:
     - **Python project** → pytest with requests/httpx
     - **Go project** → standard testing package with net/http
     - **Rust project** → Rust testing framework with reqwest
     - **JavaScript/TypeScript project** → Jest/Mocha with axios/superagent
     - **Java project** → JUnit with RestAssured

   **Benefits of matching project language:**
   - Share dependencies and tools with the main project
   - Team is already familiar with the language
   - Easier to maintain and integrate with existing codebase

2. **Test Structure**:
   - Organize tests by feature/module
   - Use descriptive test names
   - Follow AAA pattern (Arrange, Act, Assert)

3. **API Testing**:
   - Test all HTTP methods (GET, POST, PUT, DELETE, etc.)
   - Verify status codes
   - Validate response structure and data
   - Test error responses

4. **Test Independence**: Each test should be independent and runnable in isolation

5. **Cleanup**: Ensure tests clean up test data and don't leave side effects

## Manual Test Case Writing

### Location
Place manual test case documents in `tests/test_cases/` directory at project root (same location as API test cases, distinguished by filename suffix `-UI.md`).

### Writing Effective Test Cases

1. **Clear Steps**: Each step should be unambiguous and executable
2. **Specific Actions**: Use exact UI elements, button names, field names from EDD/PRD
3. **Verifiable Results**: Expected results should be objectively verifiable
4. **Complete Coverage**: Cover all acceptance criteria from PRD

### Test Case Execution

Manual test cases are executed by human testers following the test steps. AI Agent does not execute manual test cases.

## Test Execution Workflow

The QA workflow follows a four-phase approach to ensure comprehensive test coverage:

### Phase 1: Requirement Analysis & Test Scenario Identification
1. **Read PRD and EDD**: Understand functional requirements and design specifications
2. **Identify all test scenarios**: Extract test scenarios from requirements
3. **Categorize scenarios**: Classify each scenario as API Test or UI Test
4. **Identify project tech stack**: Check configuration files to determine programming language

### Phase 2: Test Case Creation (All Scenarios)
1. **Write all test cases**: Create test case documents for both API and UI tests
2. **Use template**: Follow `assets/test_case_template.md` structure
3. **Mark test target**: Clearly mark each test case as API Test or UI Test
4. **Save with naming convention**: Use `TC-[Module]-[Number]-[API|UI].md` format
5. **Save location**: Place all test cases in `tests/test_cases/` directory

### Phase 3: Automation Code Generation (API Tests Only)
1. **Identify API test cases**: Find all test cases marked as "API Test"
2. **Choose testing framework**: Select framework matching project language
3. **Generate automation code**: Write automation code in project's language
4. **Reference test case IDs**: Include test case ID in code comments
5. **Save location**: Place automation code in `tests/automation/` directory

### Phase 4: Test Execution & Reporting
1. **Execute automation tests**: Run automation code for API tests
2. **Report automation results**: Document pass/fail status and issues
3. **Provide manual test cases**: UI test cases are ready for human execution
4. **Document findings**: Report all discovered issues with test case references

**Note**: Manual test cases (UI tests) are written for human testers to execute. AI Agent does not execute manual test cases.

## Test Case Naming Convention

Test case files should follow a consistent naming pattern for easy identification and organization:

**Format**: `TC-[Module]-[Number]-[API|UI].md`

**Components**:
- `TC` - Test Case prefix
- `[Module]` - The module or feature being tested (e.g., Auth, Dashboard, Payment)
- `[Number]` - Sequential number (001, 002, 003, ...)
- `[API|UI]` - Test target indicator

**Examples**:
- `TC-Auth-001-API.md` - API test for authentication module (first test case)
- `TC-Auth-002-UI.md` - UI test for authentication module (second test case)
- `TC-Dashboard-001-UI.md` - UI test for dashboard module
- `TC-Payment-001-API.md` - API test for payment module
- `TC-Payment-002-API.md` - Second API test for payment module

**Benefits**:
- Easy to identify the module being tested
- Quick distinction between API and UI tests
- Natural organization by module and sequence
- Clear test case identification in reports and automation code

## Common Integration Test Scenarios

### API Integration Tests
- End-to-end API workflows
- Authentication and authorization flows
- Data validation and error handling
- API versioning and backward compatibility

### Database Integration Tests
- Data persistence and retrieval
- Transaction handling
- Data integrity constraints
- Query performance (if specified in requirements)

### External Service Integration Tests
- Third-party API integrations
- Webhook handling
- Message queue processing
- File upload/download

## Reporting Test Results

Document test execution results including:
- Test case ID and title
- Execution status (Pass/Fail/Blocked)
- Actual vs Expected results
- Screenshots or logs (for failures)
- Defect information (if applicable)
