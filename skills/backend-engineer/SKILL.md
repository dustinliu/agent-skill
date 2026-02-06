---
name: backend-engineer
description: >
  Backend implementation workflow following EDD specifications. Covers implementation planning,
  code architecture design, and TDD-style development. Use when implementing backend features
  from EDD or User Stories. Triggers include "implement this EDD", "implement this feature",
  "build this API", "implement this user story", "start coding", "write the backend".
  Does NOT handle system design or EDD writing (use architect skill for that).
  STRICTLY backend only — NEVER create or modify frontend files (HTML, CSS, JavaScript, templates, static assets).
---

# Backend Engineer

Implement backend systems following EDD specifications with TDD approach.

**Input:** EDD (Engineering Design Document) or User Story (or both)
**Output:** Working code with tests (coverage > 85%) + documentation

## Scope — Backend Only

**NEVER create or modify:**
- HTML files (`.html`, `.htm`)
- CSS files (`.css`, `.scss`, `.sass`, `.less`)
- JavaScript/TypeScript frontend files (`.js`, `.ts`, `.jsx`, `.tsx` in frontend directories)
- Template files (`.hbs`, `.ejs`, `.pug`, `.jinja2` used for rendering HTML)
- Static assets (images, fonts, frontend bundles)

If the EDD or User Story includes frontend requirements, skip them and notify the user that frontend work is out of scope for this skill.

**Documentation ownership:**
- `README.md` - Quick start guide
- `docs/codebase-guide.md` - Code architecture

## Workflow

```
1. UNDERSTAND        → Read EDD + User Story, clarify requirements
        ↓  ↻ iterate until user confirms
2. OPENAPI SPEC      → Expand EDD API design into OpenAPI 3.x spec
        ↓  ↻ iterate until user confirms
3. ARCHITECTURE DOC  → Design and document code architecture
        ↓  ↻ iterate until user confirms
4. IMPLEMENT (TDD)   → For each task: Code → Test → Verify → Next
        ↓
5. FINALIZE          → Verify coverage, update docs, cleanup
```

**Phase 1–3 iteration loop:** Complete the phase → present result to user → STOP and wait for confirmation. If user gives feedback, discuss to reach agreement → apply changes → present again → repeat until user says OK. Only then proceed to the next phase.

## Phase 1: Understand

Read and analyze (as provided):
- **EDD:** Tech stack, API design, database schema, architecture decisions
- **User Story:** Specific requirements for this implementation

**Clarify all ambiguities before proceeding.** EDD and PRD are useful sources for answers, but always confirm understanding with user if any doubt remains.

**User review gate:** Summarize understanding of requirements and STOP. Wait for user confirmation before proceeding to Phase 2.

## Phase 2: Generate OpenAPI Spec

Convert the EDD's concise API design into a full OpenAPI 3.x specification.

- Input: API endpoints from EDD's Technical Design section
- Output: `docs/openapi.yaml`
- Expand each endpoint into complete OpenAPI format: parameters, request/response schemas, error codes, examples
- This spec becomes the authoritative API contract for implementation

**User review gate:** Present the OpenAPI spec and STOP. Wait for user confirmation before proceeding to Phase 3.

## Phase 3: Code Architecture Document

Create `docs/codebase-guide.md` using [template](assets/codebase-guide-template.md).

Document:
- Directory structure
- Layer architecture (API → Service → Repository → DB)
- Key components and their responsibilities
- Data flow
- Common patterns used

This document helps future developers understand the codebase without reading all code.

**Avoid duplicating EDD content.** EDD covers system design decisions; this document focuses on code-level structure and patterns.

**User review gate:** Present the architecture document and STOP. Wait for user confirmation before proceeding to Phase 4.

## Phase 4: Implement (TDD)

Use `/test-driven-development` and `/software-architecture` skills for implementation.

**Language-specific guidance:** Check `references/<language>.md` if available (e.g., `references/go.md`, `references/rust.md`).

### Implementation Strategy

**Vertical slice approach:** Organize tasks by feature/endpoint, not by layer. Each task is a complete feature across all layers (model → repository → service → handler).

For each task, identify:
- **Layers** involved
- **Dependencies** on other tasks
- **Acceptance Criteria** — break down each feature into specific, testable behaviors. Each AC maps to one or more test cases in the TDD cycle. Include:
  - Success cases (happy path)
  - Error/edge cases (validation failures, not found, conflicts)
  - Side effects (e.g., password hashed before storage, audit log created)

Start with a **Task 0: Project Setup** for initialization (project structure, dependencies, config, DB connection).

### Per-AC TDD cycle

For each **feature (task)**, iterate through each **acceptance criteria (AC)**:

```mermaid
flowchart TD
    START([Pick next feature]) --> AC([Pick next AC])
    AC --> RED["1. RED — Write test for this AC<br/>Test should fail initially"]
    RED --> GREEN["2. GREEN — Write minimal code to pass test"]
    GREEN --> REFACTOR["3. REFACTOR — Clean up while tests stay green"]
    REFACTOR --> VERIFY["4. VERIFY — Run ALL tests, ensure all pass<br/>Check coverage >= 85%"]
    VERIFY --> AC_CHECK{"More ACs in this feature?"}
    AC_CHECK -- Yes --> AC
    AC_CHECK -- No --> FEAT_CHECK{"More features?"}
    FEAT_CHECK -- Yes --> START
    FEAT_CHECK -- No --> DONE([All features complete])
```

**Rules:**
- Every AC maps to one or more test cases
- Run full test suite after each AC completion

## Phase 5: Finalize

1. **Final test run** - all tests must pass
2. **Verify test coverage** > 85%
3. **Update `docs/codebase-guide.md`** if codebase changed during implementation
4. **Update `README.md`** using [template](assets/readme-template.md) — ensure quick start guide, setup instructions, and documentation links are current

**User review gate:** Present the final state (test results, coverage, updated docs) and STOP. Wait for user confirmation.

## References
- [Codebase Guide Template](assets/codebase-guide-template.md)
