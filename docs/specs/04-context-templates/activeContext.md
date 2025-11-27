# Active Context Template

## Purpose & Usage

The Active Context template maintains real-time awareness of the current development state, active tasks, and immediate goals. This template serves as the "working memory" for development sessions, ensuring continuity and focus.

**When to Use:**
- Starting a new development session
- Switching between tasks or features
- Coordinating multi-agent workflows
- Resuming interrupted work

## Template Structure

```markdown
# Active Context: [Project/Feature Name]

## Session Information
- **Session ID**: [unique-session-id]
- **Started**: [YYYY-MM-DD HH:MM]
- **Last Updated**: [YYYY-MM-DD HH:MM]
- **Current Agent**: [agent-role]
- **Session Type**: [development/debugging/refactoring/enhancement]

## Current Focus
**Primary Goal**: [What you're trying to achieve right now]

**Active Tasks**:
1. [Task 1 - Status: in_progress/blocked/waiting]
2. [Task 2 - Status: in_progress/blocked/waiting]
3. [Task 3 - Status: in_progress/blocked/waiting]

**Immediate Next Steps**:
- [ ] [Specific actionable step 1]
- [ ] [Specific actionable step 2]
- [ ] [Specific actionable step 3]

## Working Context

### Files Currently Modified
- `[file-path]` - [modification type: new/editing/refactoring]
- `[file-path]` - [modification type: new/editing/refactoring]

### Active Dependencies
- [Package/Module]: [version] - [why it's relevant]
- [Package/Module]: [version] - [why it's relevant]

### Environment State
- **Node Version**: [version]
- **Package Manager**: [npm/yarn/pnpm]
- **Branch**: [git-branch-name]
- **Uncommitted Changes**: [yes/no - brief description]

## Recent Changes (Last 30 minutes)
1. [HH:MM] - [Brief description of change]
2. [HH:MM] - [Brief description of change]
3. [HH:MM] - [Brief description of change]

## Blockers & Issues
**Active Blockers**:
- [Blocker description] - [Severity: critical/high/medium/low]
  - **Impact**: [What's being blocked]
  - **Mitigation**: [Current approach or need help]

**Known Issues**:
- [Issue description] - [Status: investigating/workaround-found/needs-decision]

## Agent Coordination

### Active Agents
- **[Agent Role]**: [Current task] - [Status]
- **[Agent Role]**: [Current task] - [Status]

### Handoff Points
- [Agent A] → [Agent B]: [What needs to be passed]
- [Agent B] → [Agent C]: [What needs to be passed]

### Memory Integration
```bash
# Store current context
npx claude-flow memory store "session/active-context" '{
  "session_id": "[session-id]",
  "primary_goal": "[goal]",
  "active_tasks": ["task1", "task2"],
  "modified_files": ["file1", "file2"],
  "blockers": [],
  "updated_at": "[ISO-timestamp]"
}' --namespace "development/session"

# Retrieve last session context
npx claude-flow memory retrieve --key "session/active-context" --namespace "development/session"
```

## Neural Enhancement Context

### Active Learning Patterns
- **Pattern Type**: [coordination/optimization/prediction]
- **Training Data**: [Brief description of what's being learned]
- **Application**: [How neural insights are being applied]

### Performance Metrics
- **Token Usage**: [current/budget]
- **Response Time**: [average ms]
- **Success Rate**: [percentage]

## Quick Reference Links
- [Related PRD Section](#)
- [Related Spec Document](#)
- [Related Decision Log Entry](#)
- [Related Progress Tracking](#)
```

## Example Usage

### Full-Stack Feature Development

```markdown
# Active Context: User Authentication System

## Session Information
- **Session ID**: auth-session-2025-11-27-001
- **Started**: 2025-11-27 14:30
- **Last Updated**: 2025-11-27 16:45
- **Current Agent**: backend-dev
- **Session Type**: development

## Current Focus
**Primary Goal**: Implement JWT-based authentication with refresh tokens

**Active Tasks**:
1. JWT token generation service - Status: in_progress
2. Refresh token rotation mechanism - Status: in_progress
3. Auth middleware implementation - Status: waiting
4. Integration tests for auth flow - Status: waiting

**Immediate Next Steps**:
- [ ] Complete JWT service with expiration handling
- [ ] Implement refresh token storage in Redis
- [ ] Create auth middleware with token validation
- [ ] Write integration tests covering token lifecycle

## Working Context

### Files Currently Modified
- `/home/cabdru/project/src/services/auth.service.ts` - new
- `/home/cabdru/project/src/middleware/auth.middleware.ts` - new
- `/home/cabdru/project/src/config/jwt.config.ts` - new
- `/home/cabdru/project/tests/auth.integration.test.ts` - new

### Active Dependencies
- jsonwebtoken: ^9.0.2 - JWT creation and validation
- bcryptjs: ^2.4.3 - Password hashing
- redis: ^4.6.0 - Refresh token storage

### Environment State
- **Node Version**: v20.10.0
- **Package Manager**: npm
- **Branch**: feature/jwt-authentication
- **Uncommitted Changes**: yes - 4 new files, auth service implementation

## Recent Changes (Last 30 minutes)
1. 16:45 - Implemented JWT token generation with configurable expiration
2. 16:30 - Added Redis client configuration for token storage
3. 16:15 - Created auth service skeleton with TypeScript interfaces
4. 16:00 - Set up testing environment with Jest and supertest

## Blockers & Issues
**Active Blockers**:
- None currently

**Known Issues**:
- Token expiration testing requires time manipulation - Status: workaround-found
  - **Impact**: Integration tests for token lifecycle
  - **Mitigation**: Using jest.useFakeTimers() for time-based tests

## Agent Coordination

### Active Agents
- **backend-dev**: Implementing auth service - in_progress
- **tester**: Preparing test infrastructure - waiting
- **security-auditor**: Ready to review - waiting

### Handoff Points
- backend-dev → tester: Auth service completion, API endpoints ready
- tester → security-auditor: Test suite complete, vulnerability assessment needed

### Memory Integration
```bash
# Store current context
npx claude-flow memory store "session/active-context" '{
  "session_id": "auth-session-2025-11-27-001",
  "primary_goal": "Implement JWT-based authentication with refresh tokens",
  "active_tasks": ["jwt-generation", "refresh-rotation", "auth-middleware", "integration-tests"],
  "modified_files": ["auth.service.ts", "auth.middleware.ts", "jwt.config.ts", "auth.integration.test.ts"],
  "blockers": [],
  "updated_at": "2025-11-27T16:45:00Z"
}' --namespace "development/session"
```

## Neural Enhancement Context

### Active Learning Patterns
- **Pattern Type**: coordination
- **Training Data**: Multi-agent auth implementation workflow
- **Application**: Optimizing handoff timing between backend-dev and tester agents

### Performance Metrics
- **Token Usage**: 45000/200000
- **Response Time**: 180ms average
- **Success Rate**: 98.5%

## Quick Reference Links
- [Authentication PRD Section](../01-prd/01-core-system.md#authentication)
- [Auth Service Spec](../03-task-specs/backend/auth-service.md)
- [Security Decision Log](./decisionLog.md#security-decisions)
- [Sprint Progress](./progressTracking.md#sprint-3)
```

## Integration Points

### 1. Memory System Integration
```bash
# Auto-store context every 15 minutes via hooks
npx claude-flow hooks post-edit --file "activeContext.md" \
  --memory-key "session/active-context" \
  --auto-persist true

# Retrieve context on session start
npx claude-flow hooks session-restore \
  --session-id "current" \
  --load-active-context true
```

### 2. Agent Coordination
- Shared via `development/session` namespace
- Updated by any agent making changes
- Read before starting new tasks
- Synchronized on agent handoffs

### 3. Progress Tracking Integration
- Active tasks linked to sprint backlog
- Blockers escalated to progress tracking
- Completed tasks update progress metrics

### 4. Decision Log Integration
- Active blockers may trigger decision logging
- Mitigation approaches documented as decisions
- Technology choices referenced from decisions

## Best Practices

### ✅ DO
- **Update frequently** (every 15-30 minutes during active development)
- **Be specific** in task descriptions and next steps
- **Track blockers immediately** when they arise
- **Use timestamps** for all recent changes
- **Link to related documents** for quick context switching
- **Store in memory** after each significant update
- **Include environment details** that affect behavior
- **Document agent handoffs** explicitly

### ❌ DON'T
- **Don't let context go stale** (update at least hourly)
- **Don't use vague descriptions** ("fix bugs" vs "fix JWT expiration validation bug")
- **Don't forget to clear completed tasks** (move to progress tracking)
- **Don't mix multiple features** in one active context
- **Don't ignore blockers** (document and escalate)
- **Don't skip memory integration** (context must persist)
- **Don't duplicate information** (reference other docs instead)

### Context Lifecycle

1. **Session Start**: Load from memory or create new
2. **Active Development**: Update every 15-30 minutes
3. **Blockers Arise**: Document immediately with severity
4. **Agent Handoff**: Update coordination section, notify next agent
5. **Session Pause**: Store complete state to memory
6. **Session Resume**: Restore from memory, validate currency
7. **Session End**: Archive to progress tracking, clear active tasks

### Multi-Agent Coordination

When multiple agents work simultaneously:
- Each agent updates their section atomically
- Use memory locks for concurrent updates
- Agent-specific context in dedicated sections
- Shared state in top-level sections
- Handoff triggers memory notification

```bash
# Agent-specific context update
npx claude-flow memory store "session/agent/backend-dev" '{
  "current_task": "JWT service implementation",
  "status": "in_progress",
  "next_agent": "tester",
  "handoff_ready": false
}' --namespace "development/session"

# Notify next agent when ready
npx claude-flow hooks notify \
  --agent "tester" \
  --message "Auth service ready for testing" \
  --context-key "session/active-context"
```

## Performance Optimization

- **Keep file size under 10KB** for fast loading
- **Use references** instead of duplicating content
- **Archive old changes** (move to progress tracking after 24 hours)
- **Limit recent changes** to last 30 minutes only
- **Cache in memory** for sub-100ms retrieval
- **Index by session ID** for quick lookups

---

**Template Version**: 1.0.0
**Last Updated**: 2025-11-27
**Maintained By**: Claude Flow Blueprint Project
