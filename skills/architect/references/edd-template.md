# EDD Template (Engineering Design Document)

## Document Header

```markdown
# EDD: [Feature/System Name]

**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
```

## Required Sections

### Overview

Brief summary (2-3 sentences) of what this document covers.

### Problem Statement

- What problem are we solving?
- Who is affected?
- What is the current state?

### Goals and Non-Goals

**Goals:**
- Specific, measurable objectives
- What success looks like

**Non-Goals:**
- Explicitly out of scope items
- Prevents scope creep

### Background

- Relevant context
- Prior art or existing solutions
- Why now?

### Technical Design

Everything in this section is **authoritative** — backend engineers must follow these decisions.
For areas still under discussion, use the Open Questions section instead of including
them here. For areas where backend engineers have implementation flexibility, mark them explicitly
with a `> **Suggestion:**` callout.

#### Tech Stack

- Language & framework
- Database (type & engine)
- Infrastructure / deployment
- Architecture pattern (e.g. monolith, microservices)
- Key libraries or tools (if critical to the design)

#### High-Level Architecture

- System diagram (Mermaid flowchart)
- Component interactions (Mermaid if complicated)
- When system involves multiple services, internal or external, include sequence diagram (Mermaid) show the interaction flow

#### API Design

For each endpoint:
```
[METHOD] /api/v1/resource
Request:  { field: type }
Response: { field: type }
Errors:   [400, 401, 404, 500]
```

#### Database Schema

- Table definitions with types
- Indexes
- Relationships (FK)
- Migration strategy

#### Key Technical Decisions

| Decision | Options Considered | Choice | Rationale |
|----------|-------------------|--------|-----------|
| ...      | ...               | ...    | ...       |

### Security Considerations

- Authentication/Authorization
- Data encryption
- Input validation
- OWASP top 10 review

### Open Questions

| Question | Owner | Status | Resolution |
|----------|-------|--------|------------|
| ...      | ...   | Open   | ...        |

### References

- Related documents
- External resources
- Prior EDDs

---

## Writing Guidelines

- **Technical Design** is the contract between architect and backend engineer. Only include decisions that are finalized.
- **Undecided items** belong in Open Questions, not in the Technical Design section.
- **Flexible items** where the backend engineer may choose the approach: use `> **Suggestion:**` callout inline to distinguish them from authoritative decisions.
