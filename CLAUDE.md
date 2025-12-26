# CLAUDE.md - AI Assistant Development Guide

**Last Updated**: 2025-12-26
**Repository**: Claude-main
**Purpose**: Comprehensive guide for AI assistants working with this codebase

---

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Codebase Structure](#codebase-structure)
3. [Development Workflow](#development-workflow)
4. [Key Conventions](#key-conventions)
5. [Git Workflow](#git-workflow)
6. [Code Style Guidelines](#code-style-guidelines)
7. [Testing Strategy](#testing-strategy)
8. [Documentation Standards](#documentation-standards)
9. [Common Tasks](#common-tasks)
10. [Troubleshooting](#troubleshooting)

---

## Repository Overview

### Project Purpose
This repository is part of the Claude ecosystem. As development progresses, update this section with:
- Project mission and goals
- Key features and capabilities
- Target audience/users
- Technology stack overview

### Current Status
- **Repository State**: Newly initialized
- **Main Branch**: TBD (to be established)
- **Active Development**: Yes
- **Production Ready**: No

---

## Codebase Structure

### Directory Layout

```
Claude-main/
├── .git/                  # Git version control
├── src/                   # Source code (to be added)
├── tests/                 # Test files (to be added)
├── docs/                  # Documentation (to be added)
├── config/                # Configuration files (to be added)
├── scripts/               # Build and utility scripts (to be added)
└── CLAUDE.md             # This file - AI assistant guide
```

### Key Directories (Update as project grows)

**`src/`** - Main source code directory
- Purpose: Core application logic
- Organization: TBD based on architecture

**`tests/`** - Testing suite
- Purpose: Unit, integration, and end-to-end tests
- Framework: TBD

**`docs/`** - Documentation
- Purpose: User guides, API docs, architecture decisions
- Format: Markdown preferred

**`config/`** - Configuration files
- Purpose: Environment configs, settings, dependencies
- Security: Never commit secrets or credentials

**`scripts/`** - Automation scripts
- Purpose: Build, deploy, test automation
- Usage: Document each script's purpose clearly

---

## Development Workflow

### For AI Assistants: Standard Operating Procedure

#### 1. **Understanding the Task**
- Read the entire request carefully
- Identify the scope: bug fix, feature, refactor, documentation
- Check for related issues or PRs
- Ask clarifying questions if requirements are ambiguous

#### 2. **Code Analysis Before Changes**
- **ALWAYS** read existing files before modifying them
- Understand current patterns and conventions
- Check for similar implementations elsewhere
- Identify dependencies and impacts

#### 3. **Planning Complex Changes**
- Use TodoWrite tool for multi-step tasks
- Break down large features into smaller commits
- Consider backwards compatibility
- Identify testing requirements

#### 4. **Implementation**
- Follow existing code patterns and style
- Keep changes focused and minimal
- Avoid over-engineering
- Don't add unnecessary features or refactoring
- Prioritize simplicity over cleverness

#### 5. **Testing**
- Run existing tests before committing
- Add tests for new functionality
- Verify edge cases
- Test error handling

#### 6. **Documentation**
- Update relevant documentation
- Add comments only where logic isn't self-evident
- Update CLAUDE.md if workflows change
- Keep README.md current

#### 7. **Commit and Push**
- Write clear, descriptive commit messages
- Follow conventional commit format (see Git Workflow)
- Push to feature branches (claude/* prefix)
- Create PRs with detailed descriptions

---

## Key Conventions

### File Naming
- Use descriptive, lowercase names
- Prefer kebab-case for multi-word files: `user-service.js`
- Match file names to primary export/class
- Use appropriate extensions

### Code Organization
- One primary responsibility per file
- Group related functionality together
- Keep files focused and reasonably sized
- Use clear module boundaries

### Import/Export Patterns
- Prefer named exports for better refactoring
- Group imports: external libs, then internal modules
- Avoid circular dependencies
- Use absolute imports where configured

### Error Handling
- Validate at system boundaries (user input, external APIs)
- Use appropriate error types/classes
- Provide meaningful error messages
- Log errors with context
- Don't over-handle errors in internal code

### Security Practices
- **Never commit secrets, API keys, or credentials**
- Use environment variables for sensitive data
- Validate and sanitize all external input
- Follow OWASP guidelines
- Watch for: XSS, SQL injection, command injection, CSRF

### Performance Considerations
- Avoid premature optimization
- Profile before optimizing
- Consider algorithmic complexity for large datasets
- Cache expensive operations when justified
- Document performance-critical sections

---

## Git Workflow

### Branch Naming Convention

**Feature Branches**: `claude/<descriptive-name>-<session-id>`
- Example: `claude/add-user-auth-LQM6O`
- Always include session ID suffix
- Use kebab-case for description

**Branch Types** (if project scales):
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation only
- `refactor/*` - Code refactoring
- `test/*` - Test improvements

### Commit Message Format

Follow Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(auth): add JWT token validation

Implement JWT token validation middleware for protected routes.
Includes token expiration checking and signature verification.

Closes #123

---

fix(api): handle null response in user fetch

Previously crashed when API returned null.
Now returns empty user object with appropriate logging.

---

docs(readme): update installation instructions

Add steps for configuring environment variables.
```

### Commit Best Practices

1. **Commit frequently** - Small, logical chunks
2. **One concern per commit** - Don't mix unrelated changes
3. **Write clear messages** - Future you will thank you
4. **Reference issues** - Use "Closes #123" or "Refs #456"
5. **Test before committing** - Ensure tests pass

### Push Protocol

```bash
# Always push to feature branch with -u flag
git push -u origin <branch-name>

# Retry on network failures (up to 4 times)
# Exponential backoff: 2s, 4s, 8s, 16s
```

**Critical**: Branch must start with `claude/` and end with session ID, or push will fail with 403.

### Pull Request Guidelines

**Title**: Clear, concise description of changes

**Description Template**:
```markdown
## Summary
- Bullet point summary of changes
- What problem does this solve?
- What approach was taken?

## Changes Made
- List specific files/modules changed
- Highlight any breaking changes
- Note any new dependencies

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Edge cases verified

## Documentation
- [ ] Code comments added where needed
- [ ] README updated if applicable
- [ ] CLAUDE.md updated if workflows changed

## Screenshots/Examples
(If applicable)

## Related Issues
Closes #123
Refs #456
```

---

## Code Style Guidelines

### General Principles

1. **Readability First**: Code is read more than written
2. **Consistency**: Follow existing patterns
3. **Simplicity**: Prefer simple solutions
4. **Explicitness**: Be clear over clever
5. **DRY Cautiously**: Don't repeat yourself, but don't abstract too early

### Language-Specific Guidelines (Update based on stack)

#### JavaScript/TypeScript
- Use `const` by default, `let` when needed, never `var`
- Prefer async/await over promises chains
- Use template literals for string interpolation
- Destructure objects and arrays when it improves clarity
- Use arrow functions for callbacks
- Prefer functional array methods (map, filter, reduce)

#### Python
- Follow PEP 8
- Use type hints for function signatures
- Prefer list comprehensions for simple transformations
- Use context managers (`with` statements)
- Document classes and public methods

#### General
- Maximum line length: 80-120 characters (check project config)
- Indentation: Spaces (2 or 4, follow project convention)
- No trailing whitespace
- Files end with newline

### Comments and Documentation

**When to Comment**:
- Complex algorithms or business logic
- Non-obvious workarounds
- Performance-critical sections
- Security considerations
- API usage examples

**When NOT to Comment**:
- Self-evident code
- Redundant descriptions
- Obvious variable names
- Standard patterns

**Good Comment**:
```javascript
// Cache user permissions for 5 minutes to reduce database load
// during high-traffic periods. See performance doc #45.
const cachedPermissions = cache.get(userId, 300);
```

**Bad Comment**:
```javascript
// Get the user name
const userName = user.name;
```

---

## Testing Strategy

### Testing Philosophy

- **Write tests for new features** - Before or during development
- **Don't break existing tests** - Fix or update as needed
- **Test behavior, not implementation** - Tests should survive refactoring
- **Test edge cases** - Null, empty, boundary conditions
- **Keep tests simple** - Tests should be easy to understand

### Test Organization

```
tests/
├── unit/              # Unit tests - test individual functions/classes
├── integration/       # Integration tests - test module interactions
├── e2e/              # End-to-end tests - test full workflows
└── fixtures/         # Test data and mocks
```

### Testing Checklist

- [ ] Happy path tested
- [ ] Error cases tested
- [ ] Edge cases (null, empty, boundary values)
- [ ] Integration points verified
- [ ] Performance acceptable for critical paths
- [ ] Security considerations tested (if applicable)

### Running Tests

```bash
# Update these commands based on actual test setup
npm test              # Run all tests
npm run test:unit     # Run unit tests only
npm run test:watch    # Run tests in watch mode
npm run test:coverage # Generate coverage report
```

---

## Documentation Standards

### Code Documentation

**Functions/Methods**:
- Document public APIs
- Include parameter descriptions
- Specify return types and values
- Note side effects or mutations
- Provide usage examples for complex functions

**Example**:
```javascript
/**
 * Authenticates a user and returns a JWT token.
 *
 * @param {string} username - User's login name
 * @param {string} password - User's password (will be hashed)
 * @returns {Promise<string>} JWT token valid for 24 hours
 * @throws {AuthenticationError} If credentials are invalid
 *
 * @example
 * const token = await authenticateUser('john', 'password123');
 */
async function authenticateUser(username, password) {
  // ...
}
```

### Project Documentation

**README.md** - Should include:
- Project description
- Installation instructions
- Quick start guide
- Basic usage examples
- Link to full documentation
- Contributing guidelines
- License information

**ARCHITECTURE.md** - For complex projects:
- System architecture overview
- Component interactions
- Data flow diagrams
- Technology decisions and rationale
- Scalability considerations

**API.md** - For APIs:
- Endpoint documentation
- Request/response examples
- Authentication requirements
- Error codes and handling
- Rate limiting information

### Keeping Documentation Current

- Update docs in the same PR as code changes
- Review docs during code review
- Archive outdated documentation
- Version API documentation
- Keep CLAUDE.md synchronized with workflows

---

## Common Tasks

### Starting a New Feature

1. Ensure you're on the correct branch:
   ```bash
   git status
   # Should show: claude/<feature-name>-<session-id>
   ```

2. Create branch if needed:
   ```bash
   git checkout -b claude/<feature-name>-<session-id>
   ```

3. Plan the implementation (use TodoWrite for complex features)

4. Read relevant existing code

5. Implement changes incrementally

6. Test thoroughly

7. Commit and push

### Fixing a Bug

1. **Reproduce the bug** - Understand the issue

2. **Locate the problem** - Use Grep, Glob, Read tools

3. **Understand the context** - Read surrounding code

4. **Write a failing test** - Captures the bug

5. **Fix the bug** - Minimal changes

6. **Verify the fix** - Test passes, no regressions

7. **Document if needed** - If bug was non-obvious

### Refactoring Code

⚠️ **Caution**: Only refactor when explicitly requested or clearly necessary.

1. **Ensure test coverage** - Critical for safe refactoring

2. **Make small changes** - One refactoring at a time

3. **Run tests frequently** - After each change

4. **Keep commits atomic** - Each commit should be functional

5. **Don't change behavior** - Refactoring shouldn't alter functionality

### Adding Dependencies

1. **Justify the need** - Don't add dependencies lightly

2. **Check license** - Ensure compatibility

3. **Review security** - Check for known vulnerabilities

4. **Consider size** - Impact on bundle/deployment size

5. **Update documentation** - Note new dependency and purpose

---

## Troubleshooting

### Common Issues for AI Assistants

#### "Permission Denied" on Push
**Cause**: Branch name doesn't match required pattern
**Solution**: Ensure branch starts with `claude/` and ends with session ID

#### "Network Error" on Git Operations
**Cause**: Connectivity issues with local proxy
**Solution**: Retry with exponential backoff (2s, 4s, 8s, 16s)

#### "Tests Failing" After Changes
**Cause**: Breaking changes or incomplete implementation
**Solution**:
- Read test output carefully
- Fix the code or update tests if behavior changed intentionally
- Don't commit failing tests

#### "File Not Found" When Reading
**Cause**: Incorrect path or file doesn't exist
**Solution**:
- Use Glob to find files by pattern
- Check current working directory
- Use absolute paths

#### "Merge Conflicts"
**Cause**: Changes conflict with main branch
**Solution**:
- Fetch latest changes
- Resolve conflicts manually
- Test after resolution
- Ask user if uncertain about resolution

### Debug Workflow

1. **Reproduce the issue** - Understand what's wrong
2. **Gather information** - Logs, error messages, stack traces
3. **Isolate the problem** - Narrow down the scope
4. **Form hypothesis** - What might be causing it?
5. **Test hypothesis** - Make minimal changes to verify
6. **Fix and verify** - Ensure fix works and doesn't break anything
7. **Prevent recurrence** - Add tests, update documentation

---

## Best Practices Summary

### DO:
✅ Read existing code before making changes
✅ Follow established patterns and conventions
✅ Write clear, descriptive commit messages
✅ Add tests for new functionality
✅ Keep changes focused and minimal
✅ Ask questions when requirements are unclear
✅ Update documentation with code changes
✅ Use TodoWrite for complex multi-step tasks
✅ Verify tests pass before committing
✅ Consider security implications

### DON'T:
❌ Make changes without reading existing code
❌ Add unnecessary features or "improvements"
❌ Over-engineer solutions
❌ Commit secrets or credentials
❌ Skip testing
❌ Write unclear commit messages
❌ Mix unrelated changes in one commit
❌ Assume - verify with code inspection
❌ Refactor without being asked
❌ Batch multiple todo completions

---

## Updating This Document

This is a living document. Update it when:

- Development workflows change
- New conventions are established
- Tools or frameworks are added
- Common issues are discovered
- Project structure evolves
- Best practices are refined

**Process for updates**:
1. Make changes in a feature branch
2. Include updates in relevant PR
3. Update the "Last Updated" date at the top
4. Document what changed and why
5. Get review from team/stakeholders

---

## Additional Resources

### External Documentation
- [Conventional Commits](https://www.conventionalcommits.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

### Project-Specific Resources
(Add as project grows)
- API Documentation: TBD
- Architecture Docs: TBD
- Contributing Guide: TBD
- Code of Conduct: TBD

---

## Contact and Support

**For AI Assistants**:
- Reference this document for workflow questions
- Use TodoWrite for task management
- Ask clarifying questions when uncertain
- Update this document as the project evolves

**For Humans**:
- Check README.md for project-specific guidance
- Consult CONTRIBUTING.md (when available)
- Review open issues and PRs
- Ask in team channels

---

**Remember**: The goal is to write clean, maintainable code that serves the project's needs. When in doubt, favor simplicity, clarity, and consistency with existing patterns.

**Last Updated**: 2025-12-26
**Next Review**: As project structure is established
