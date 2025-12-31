<!--
Sync Impact Report:
Version: 0.1.0 → 1.0.0
Bump Rationale: MAJOR - Initial constitution establishment with full governance structure
Modified Principles: N/A (initial creation)
Added Sections: All core sections established
Removed Sections: None
Templates Status:
  ✅ plan-template.md - Constitution Check section aligns
  ✅ spec-template.md - Scope/requirements alignment verified
  ✅ tasks-template.md - Task categorization reflects principles
  ⚠ Command files - No command files found in .specify/templates/commands/
Follow-up TODOs: None - all placeholders resolved
-->

# Todo App Constitution

## Core Principles

### I. AI-Native Development (NON-NEGOTIABLE)

All code MUST be generated through Claude Code using Spec-Kit Plus workflow. Zero manual coding is allowed. This ensures consistent quality, full traceability of design decisions, and alignment with specification-driven methodology.

**Rationale**: Enforces learning objectives for AI-assisted development and maintains audit trail for academic evaluation.

### II. Specification-Driven Workflow (NON-NEGOTIABLE)

Every change MUST follow the sequence: Write spec → Plan → Break into tasks → Implement → Test. No implementation may begin without a corresponding specification artifact.

**Rationale**: Separates business understanding from technical execution, enabling clear validation of requirements before expensive implementation work begins.

### III. Clean Architecture & Modularity

Code MUST follow single-responsibility principle with clear separation of concerns. Python modules must be organized by function (models, services, CLI interface).

**Requirements**:
- Each module serves one clear purpose
- Dependencies flow inward (services → models)
- CLI layer remains thin, delegating to services
- No circular dependencies

**Rationale**: Enables independent testing, future extensibility (e.g., adding persistence layer), and maintainability.

### IV. Test-First Development

All core CRUD features MUST be demonstrable and testable via CLI. Manual testing protocol required before marking tasks complete.

**Requirements**:
- Each feature must have documented test cases
- Test cases must cover happy path and edge cases
- CLI output must clearly indicate success/failure
- State validation (e.g., task count, ID consistency) required

**Rationale**: Console-based validation ensures functionality without requiring test framework infrastructure, appropriate for Phase I scope.

### V. Version-Controlled Specifications

All specification documents MUST be stored in `specs_history/` with version tracking. Each iteration of requirements must be preserved with timestamp and rationale for changes.

**Requirements**:
- Spec files named with version suffix (e.g., `spec_v1.md`, `spec_v2.md`)
- Changes documented with date and reason
- No deletion of prior spec versions
- Link current implementation to spec version

**Rationale**: Demonstrates iterative refinement process and provides evidence of specification evolution for academic assessment.

### VI. Simplicity & Constraints

**MUST adhere to**:
- Python 3.13+ only
- UV package manager exclusively
- In-memory storage (no databases, no file persistence)
- Standard library preferred; third-party packages only if justified
- No web frameworks or external services

**MUST avoid**:
- Over-engineering for future requirements not in Phase I scope
- Abstractions without concrete need (e.g., no ORM for in-memory storage)
- Feature creep beyond the 5 core CRUD operations

**Rationale**: Focuses effort on demonstrating SDD workflow rather than complex infrastructure. Constraints simulate real-world architectural limitations.

## Development Environment Standards

### Platform Requirements

**Windows developers**: MUST use WSL2 (Ubuntu-22.04) for consistent Unix-like development environment.

**Rationale**: Ensures script compatibility, UV package manager reliability, and consistent path handling across development environments.

### Project Structure (MANDATORY)

```
/
├── src/                    # All production Python code
│   ├── models/            # Task data structures
│   ├── services/          # Business logic (CRUD operations)
│   └── cli/               # Command-line interface
├── specs_history/          # Version-controlled specifications
│   └── v1/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── history/
│   ├── prompts/           # Prompt History Records
│   └── adr/               # Architecture Decision Records
├── .specify/
│   ├── memory/
│   │   └── constitution.md  # This file
│   └── templates/         # Spec-Kit Plus templates
├── README.md              # Setup and usage instructions
├── CLAUDE.md              # AI workflow documentation
└── pyproject.toml         # UV dependency specification
```

**No deviation allowed** from this structure without constitution amendment.

## Quality Gates

### Before Implementation Begins

- [ ] Feature specification exists in `specs_history/`
- [ ] Plan document outlines technical approach
- [ ] Tasks broken down with clear acceptance criteria
- [ ] All tasks map to spec requirements
- [ ] PHR created for planning session

### Before Marking Task Complete

- [ ] Feature demonstrable via CLI
- [ ] Manual test cases executed and documented
- [ ] Error handling verified (invalid input, edge cases)
- [ ] Code follows single-responsibility principle
- [ ] PHR created documenting implementation session

### Before Feature Completion

- [ ] All 5 CRUD operations functional
- [ ] Task IDs remain consistent across operations
- [ ] State management validated (add → view → update → delete → view)
- [ ] README updated with usage examples
- [ ] Spec version archived with implementation reference

## Success Criteria for Phase I

### Functional Completeness

1. **Add Tasks**: Create task with title + description, assign unique ID
2. **View Tasks**: List all tasks with status (complete/incomplete), show counts
3. **Update Tasks**: Modify task title/description by ID
4. **Delete Tasks**: Remove task by ID, handle non-existent IDs gracefully
5. **Toggle Status**: Mark task complete/incomplete by ID

### Process Completeness

- All specifications in `specs_history/` with version tracking
- PHRs document all major AI interactions
- ADRs created for significant decisions (minimum 1 expected)
- README provides clear setup instructions (UV install, run commands)
- CLAUDE.md documents workflow steps used

### Code Quality

- Clean module separation (models, services, CLI)
- No hardcoded values; configuration externalized where applicable
- Error messages clear and actionable
- Code runs without errors in fresh UV environment
- No security vulnerabilities (input validation, no command injection)

## Governance

### Amendment Procedure

1. Propose change with rationale in new PHR (stage: constitution)
2. Document impact on existing templates, specs, or code
3. Update constitution version according to semver rules:
   - **MAJOR**: Backward-incompatible principle removal/redefinition
   - **MINOR**: New principle added or section expanded
   - **PATCH**: Clarifications, wording, typo fixes
4. Update all dependent templates in `.specify/templates/`
5. Create ADR if architectural implications exist
6. Commit with message: `docs: amend constitution to vX.Y.Z (brief reason)`

### Version Bump Rules

- Removal of a principle: MAJOR bump
- Addition of a principle: MINOR bump
- Clarification without semantic change: PATCH bump
- Multiple changes: Use highest applicable bump level

### Compliance Verification

All PRs and commits MUST self-verify against this constitution. Non-compliance requires either:
- Justification in Complexity Tracking section of plan.md, or
- Constitution amendment following procedure above

**Enforcement**: This constitution supersedes all other guidance. In case of conflict between constitution and other documentation, constitution takes precedence.

**Version**: 1.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31
