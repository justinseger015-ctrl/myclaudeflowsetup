# Session Restoration Template

## Purpose & Usage

The Session Restoration template enables seamless resumption of development work after interruptions. It captures complete session state including context, decisions, progress, and agent coordination state for perfect continuity across sessions.

**When to Use:**
- End of work day (save session state)
- Beginning of work day (restore session state)
- Context switching between projects
- Recovering from interruptions
- Onboarding new team members
- Debugging failed sessions

## Template Structure

```markdown
# Session Restoration: [Session ID]

## Session Metadata
- **Session ID**: [unique-session-id]
- **Project**: [project-name]
- **Session Type**: [development/debugging/refactoring/enhancement/planning]
- **Created**: [YYYY-MM-DD HH:MM]
- **Last Active**: [YYYY-MM-DD HH:MM]
- **Duration**: [Xh Ym]
- **Status**: [active/paused/completed/failed]

## Session Context

### Primary Objective
[Clear statement of what this session is trying to achieve]

### Current Phase
[What stage of work: planning/implementation/testing/review/deployment]

### Work Summary
**Completed in This Session**:
- ✅ [Achievement 1]
- ✅ [Achievement 2]
- ✅ [Achievement 3]

**In Progress**:
- 🔄 [Task 1] - [X% complete]
- 🔄 [Task 2] - [X% complete]

**Blocked**:
- 🚫 [Blocker 1] - [Severity: critical/high/medium/low]

**Next Steps** (in priority order):
1. [Immediate next action]
2. [Second priority action]
3. [Third priority action]

## File State

### Modified Files
```json
{
  "files": [
    {
      "path": "[absolute-path]",
      "status": "new|modified|deleted",
      "changes": "[brief description]",
      "last_modified": "[ISO-timestamp]",
      "checksum": "[file-hash]"
    }
  ]
}
```

### Unstaged Changes
```bash
# Git status at session pause
[Output of git status]
```

### Stashed Changes
```bash
# Any work stashed for context switch
Stash@{0}: [description]
```

## Environment State

### Working Directory
- **Path**: [absolute-path]
- **Branch**: [git-branch-name]
- **Commit**: [git-commit-hash]
- **Remote**: [remote-name/branch]

### Dependencies
**Installed Packages**:
```json
{
  "dependencies": {
    "[package]": "[version]",
    "[package]": "[version]"
  }
}
```

**Pending Installs**:
- [package@version] - [reason]

### Environment Variables
```bash
# Critical env vars (exclude secrets)
NODE_ENV=[value]
API_BASE_URL=[value]
[other non-secret vars]
```

### Running Processes
- [Process name]: PID [####] - [port/resource]
- [Process name]: PID [####] - [port/resource]

## Agent Coordination State

### Active Agents
```json
{
  "agents": [
    {
      "role": "[agent-role]",
      "task": "[current-task]",
      "status": "active|waiting|blocked",
      "progress": "[X%]",
      "last_update": "[ISO-timestamp]"
    }
  ]
}
```

### Agent Handoffs
**Pending Handoffs**:
- [Agent A] → [Agent B]: [What needs to be passed]
- [Agent B] → [Agent C]: [What needs to be passed]

**Completed Handoffs**:
- ✅ [Agent X] → [Agent Y]: [What was passed] @ [timestamp]

### Shared State
```json
{
  "shared_memory": {
    "key": "value",
    "decisions": ["DEC-ID-1", "DEC-ID-2"],
    "blockers": ["blocker-description"],
    "context_links": {
      "active_context": "[path]",
      "decision_log": "[path]",
      "progress_tracking": "[path]"
    }
  }
}
```

## Memory Snapshot

### Session Memory Keys
```bash
# Critical memory keys for this session
session/active-context         → [timestamp]
session/agent/[role]/state     → [timestamp]
project/decisions/DEC-XXX      → [timestamp]
sprint/[number]/progress       → [timestamp]
```

### Neural Enhancement State
```json
{
  "neural_state": {
    "active_patterns": ["coordination", "optimization"],
    "training_progress": {
      "epochs_completed": [X],
      "current_loss": [Y],
      "accuracy": "[Z%]"
    },
    "model_checkpoints": [
      {
        "model_id": "[id]",
        "checkpoint": "[path]",
        "timestamp": "[ISO-timestamp]"
      }
    ]
  }
}
```

## Performance Metrics

### Token Usage
- **Session Total**: [X] tokens
- **Budget Remaining**: [Y] / [Z] ([P%])
- **Avg per Operation**: [X] tokens

### Response Times
- **Average**: [X]ms
- **P95**: [Y]ms
- **P99**: [Z]ms

### Success Metrics
- **Tasks Completed**: [X]
- **Tests Passed**: [Y / Z] ([P%])
- **Code Review Pass Rate**: [X%]

## Restoration Instructions

### Quick Restore (< 5 minutes)
```bash
# 1. Navigate to working directory
cd [absolute-path]

# 2. Restore git state
git checkout [branch]
git stash pop  # if stashed changes exist

# 3. Restore dependencies
npm install  # or yarn/pnpm

# 4. Restore memory state
npx claude-flow hooks session-restore \
  --session-id "[session-id]" \
  --load-active-context true

# 5. Verify environment
npm run typecheck
npm test

# 6. Resume work
# Review active context: [path-to-active-context]
# Check next steps above
```

### Full Restore (5-15 minutes)
```bash
# 1. Quick restore steps (above)

# 2. Restore running services
npm run dev         # restart dev server
docker-compose up   # if using Docker

# 3. Restore agent coordination
npx claude-flow swarm init --topology [topology]
npx claude-flow hooks notify \
  --agent "all" \
  --message "Session restored: [session-id]"

# 4. Load decision context
# Review decision log: [path-to-decision-log]
# Review progress: [path-to-progress-tracking]

# 5. Validate restoration
npm run build
npm test
git status

# 6. Confirm with team
# Post status update if collaborative session
```

### Recovery from Failure
```bash
# If session failed or corrupted:

# 1. Identify last known good state
npx claude-flow memory retrieve \
  --key "session/checkpoints/last-good" \
  --namespace "recovery"

# 2. Reset to checkpoint
git reset --hard [checkpoint-commit]
git clean -fd

# 3. Restore from backup
npx claude-flow memory restore \
  --backup-id "[backup-id]"

# 4. Rebuild environment
rm -rf node_modules
npm install
npm run build

# 5. Validate
npm test
git status

# 6. Resume from checkpoint
# Review checkpoint context for next steps
```

## Validation Checklist

Before marking session as "restored", verify:

### Environment
- [ ] Correct git branch checked out
- [ ] All dependencies installed (node_modules present)
- [ ] Environment variables set correctly
- [ ] No unexpected modified files (`git status` clean or understood)

### Build & Tests
- [ ] Code compiles (`npm run build` succeeds)
- [ ] Type checking passes (`npm run typecheck` succeeds)
- [ ] Tests pass (`npm test` succeeds)
- [ ] Linting passes (`npm run lint` succeeds)

### Context
- [ ] Active context loaded and reviewed
- [ ] Decision log reviewed for recent decisions
- [ ] Progress tracking shows current sprint state
- [ ] Blockers documented and understood

### Coordination
- [ ] Agent states restored from memory
- [ ] Pending handoffs identified
- [ ] Shared state synchronized
- [ ] Team notified of session resumption (if collaborative)

### Memory
- [ ] Session memory keys retrieved successfully
- [ ] Neural enhancement state loaded (if applicable)
- [ ] Historical context available
- [ ] No memory corruption detected

## Integration Commands

### Save Session (End of Day)
```bash
# Comprehensive session save
npx claude-flow hooks session-end \
  --session-id "[session-id]" \
  --export-metrics true \
  --create-checkpoint true

# This automatically:
# - Stores all active context to memory
# - Saves agent coordination state
# - Exports performance metrics
# - Creates git checkpoint
# - Generates restoration instructions
```

### Restore Session (Start of Day)
```bash
# Comprehensive session restore
npx claude-flow hooks session-restore \
  --session-id "[session-id]" \
  --load-active-context true \
  --restore-agent-state true \
  --validate-environment true

# This automatically:
# - Restores memory state
# - Loads active context
# - Restores agent coordination
# - Validates environment
# - Checks for blockers
# - Displays next steps
```

### Auto-Checkpoint (Every 30 Minutes)
```bash
# Enable auto-checkpoint
npx claude-flow hooks auto-checkpoint \
  --interval 30 \
  --memory-persist true \
  --git-stash false

# Creates lightweight checkpoints for recovery
```

## Memory Storage

```bash
# Store complete session state
npx claude-flow memory store "session/[session-id]/state" '{
  "session_id": "[session-id]",
  "project": "[project-name]",
  "objective": "[primary-objective]",
  "phase": "[current-phase]",
  "modified_files": ["file1", "file2"],
  "active_agents": [{"role": "agent1", "task": "task1"}],
  "blockers": [],
  "next_steps": ["step1", "step2"],
  "created_at": "[ISO-timestamp]",
  "last_active": "[ISO-timestamp]"
}' --namespace "development/sessions"

# Store checkpoint
npx claude-flow memory store "session/checkpoints/[timestamp]" '{
  "checkpoint_id": "[timestamp]",
  "session_id": "[session-id]",
  "git_commit": "[commit-hash]",
  "git_branch": "[branch]",
  "memory_snapshot": "[snapshot-id]",
  "agent_states": {...},
  "created_at": "[ISO-timestamp]"
}' --namespace "recovery"

# List available sessions
npx claude-flow memory search \
  --pattern "session/.*/state" \
  --namespace "development/sessions"
```

## Troubleshooting

### Common Issues

#### Environment Mismatch
**Problem**: Dependencies or Node version mismatch
**Solution**:
```bash
nvm use [version]    # Switch Node version
rm -rf node_modules
npm install
```

#### Memory State Corrupted
**Problem**: Cannot load session state from memory
**Solution**:
```bash
# Restore from previous checkpoint
npx claude-flow memory retrieve \
  --key "session/checkpoints/[previous]" \
  --namespace "recovery"
```

#### Git State Unclear
**Problem**: Unexpected changes or dirty working directory
**Solution**:
```bash
# Review changes
git status
git diff

# Stash if needed
git stash push -m "Pre-restoration state"

# Or reset to known state
git reset --hard [commit]
```

#### Agent Coordination Out of Sync
**Problem**: Agents show conflicting state
**Solution**:
```bash
# Reset agent coordination
npx claude-flow swarm destroy --all
npx claude-flow swarm init --topology [topology]

# Notify all agents
npx claude-flow hooks notify \
  --agent "all" \
  --message "Coordination reset"
```

```

## Example Usage

### Full Development Session

```markdown
# Session Restoration: neural-auth-feature-session-001

## Session Metadata
- **Session ID**: neural-auth-feature-session-001
- **Project**: claude-flow-blueprint
- **Session Type**: development
- **Created**: 2025-11-27 09:00
- **Last Active**: 2025-11-27 17:30
- **Duration**: 8h 30m
- **Status**: paused

## Session Context

### Primary Objective
Implement JWT-based authentication with neural enhancement for anomaly detection in authentication patterns.

### Current Phase
Implementation - 75% complete, moving into testing phase

### Work Summary
**Completed in This Session**:
- ✅ JWT token generation service with refresh token rotation
- ✅ Auth middleware with token validation
- ✅ pgvector schema for storing authentication patterns
- ✅ Neural pattern recognition for login anomalies
- ✅ Unit tests for auth service (92% coverage)
- ✅ API documentation for auth endpoints

**In Progress**:
- 🔄 Integration tests for auth flow - 60% complete
- 🔄 Neural training on historical login data - 40% complete

**Blocked**:
- 🚫 Staging deployment - Waiting on infrastructure approval (Medium severity)

**Next Steps** (in priority order):
1. Complete integration tests for token refresh flow
2. Finish neural model training (est. 2 more hours)
3. Implement auth monitoring dashboard
4. Code review with security-auditor agent
5. Deploy to staging once infrastructure approved

## File State

### Modified Files
```json
{
  "files": [
    {
      "path": "/home/cabdru/project/src/services/auth.service.ts",
      "status": "new",
      "changes": "JWT token generation and validation",
      "last_modified": "2025-11-27T17:15:00Z",
      "checksum": "a7f3e9d2b1c4..."
    },
    {
      "path": "/home/cabdru/project/src/middleware/auth.middleware.ts",
      "status": "new",
      "changes": "Auth middleware with token validation",
      "last_modified": "2025-11-27T16:45:00Z",
      "checksum": "b2c5f1e8d3a9..."
    },
    {
      "path": "/home/cabdru/project/src/config/jwt.config.ts",
      "status": "new",
      "changes": "JWT configuration with environment variables",
      "last_modified": "2025-11-27T15:20:00Z",
      "checksum": "c3d6g2f9e4b1..."
    },
    {
      "path": "/home/cabdru/project/src/neural/auth-pattern.service.ts",
      "status": "new",
      "changes": "Neural pattern recognition for auth anomalies",
      "last_modified": "2025-11-27T17:00:00Z",
      "checksum": "d4e7h3g1f5c2..."
    },
    {
      "path": "/home/cabdru/project/tests/auth.integration.test.ts",
      "status": "modified",
      "changes": "60% of integration tests complete",
      "last_modified": "2025-11-27T17:30:00Z",
      "checksum": "e5f8i4h2g6d3..."
    },
    {
      "path": "/home/cabdru/project/database/migrations/005_auth_patterns.sql",
      "status": "new",
      "changes": "pgvector schema for auth pattern storage",
      "last_modified": "2025-11-27T14:30:00Z",
      "checksum": "f6g9j5i3h7e4..."
    }
  ]
}
```

### Unstaged Changes
```bash
On branch feature/neural-authentication
Your branch is ahead of 'origin/feature/neural-authentication' by 3 commits.
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   src/services/auth.service.ts
        new file:   src/middleware/auth.middleware.ts
        new file:   src/config/jwt.config.ts
        new file:   src/neural/auth-pattern.service.ts
        new file:   database/migrations/005_auth_patterns.sql
        modified:   tests/auth.integration.test.ts

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        docs/api/authentication.md
```

### Stashed Changes
```bash
# No stashed changes
```

## Environment State

### Working Directory
- **Path**: /home/cabdru/project
- **Branch**: feature/neural-authentication
- **Commit**: 8f3a2c1 ("Add neural pattern recognition for auth")
- **Remote**: origin/feature/neural-authentication

### Dependencies
**Installed Packages**:
```json
{
  "dependencies": {
    "jsonwebtoken": "^9.0.2",
    "bcryptjs": "^2.4.3",
    "redis": "^4.6.0",
    "passport-jwt": "^4.0.1",
    "@tensorflow/tfjs-node": "^4.11.0",
    "pg": "^8.11.3",
    "pgvector": "^0.1.2"
  }
}
```

**Pending Installs**:
- None

### Environment Variables
```bash
NODE_ENV=development
API_BASE_URL=http://localhost:3000
JWT_SECRET=[stored in .env, not in version control]
JWT_EXPIRY=15m
REFRESH_TOKEN_EXPIRY=7d
REDIS_URL=redis://localhost:6379
DATABASE_URL=postgresql://localhost:5432/project_dev
```

### Running Processes
- Dev server: PID 12345 - port 3000
- Redis: PID 12346 - port 6379
- PostgreSQL: PID 12347 - port 5432

## Agent Coordination State

### Active Agents
```json
{
  "agents": [
    {
      "role": "backend-dev",
      "task": "Auth service implementation",
      "status": "completed",
      "progress": "100%",
      "last_update": "2025-11-27T17:15:00Z"
    },
    {
      "role": "ml-developer",
      "task": "Neural pattern training",
      "status": "active",
      "progress": "40%",
      "last_update": "2025-11-27T17:30:00Z"
    },
    {
      "role": "tester",
      "task": "Integration tests",
      "status": "active",
      "progress": "60%",
      "last_update": "2025-11-27T17:30:00Z"
    },
    {
      "role": "security-auditor",
      "task": "Awaiting code review",
      "status": "waiting",
      "progress": "0%",
      "last_update": "2025-11-27T17:00:00Z"
    }
  ]
}
```

### Agent Handoffs
**Pending Handoffs**:
- tester → security-auditor: Integration tests completion triggers security review
- ml-developer → backend-dev: Neural model ready for integration into auth service

**Completed Handoffs**:
- ✅ backend-dev → tester: Auth service API complete @ 2025-11-27T17:15:00Z
- ✅ backend-dev → ml-developer: Auth pattern schema ready @ 2025-11-27T14:30:00Z

### Shared State
```json
{
  "shared_memory": {
    "auth_endpoints": ["/auth/login", "/auth/refresh", "/auth/logout"],
    "test_coverage": "92%",
    "neural_model_accuracy": "pending_training",
    "decisions": ["DEC-2025-11-27-002"],
    "blockers": ["staging-infrastructure-approval"],
    "context_links": {
      "active_context": "/home/cabdru/project/docs/specs/04-context-templates/activeContext.md",
      "decision_log": "/home/cabdru/project/docs/specs/04-context-templates/decisionLog.md",
      "progress_tracking": "/home/cabdru/project/docs/specs/04-context-templates/progressTracking.md"
    }
  }
}
```

## Memory Snapshot

### Session Memory Keys
```bash
session/active-context                           → 2025-11-27T17:30:00Z
session/agent/backend-dev/state                  → 2025-11-27T17:15:00Z
session/agent/ml-developer/state                 → 2025-11-27T17:30:00Z
session/agent/tester/state                       → 2025-11-27T17:30:00Z
project/decisions/DEC-2025-11-27-002             → 2025-11-27T15:30:00Z
sprint/12/progress                               → 2025-11-27T17:00:00Z
swarm/coordination/neural-auth-feature           → 2025-11-27T17:30:00Z
```

### Neural Enhancement State
```json
{
  "neural_state": {
    "active_patterns": ["coordination", "anomaly-detection"],
    "training_progress": {
      "epochs_completed": 20,
      "current_loss": 0.085,
      "accuracy": "pending_validation"
    },
    "model_checkpoints": [
      {
        "model_id": "auth-anomaly-detector-v1",
        "checkpoint": "/home/cabdru/project/models/checkpoints/epoch-20.ckpt",
        "timestamp": "2025-11-27T17:25:00Z"
      }
    ]
  }
}
```

## Performance Metrics

### Token Usage
- **Session Total**: 145,320 tokens
- **Budget Remaining**: 54,680 / 200,000 (27.3%)
- **Avg per Operation**: 1,830 tokens

### Response Times
- **Average**: 220ms
- **P95**: 480ms
- **P99**: 750ms

### Success Metrics
- **Tasks Completed**: 6 / 8 (75%)
- **Tests Passed**: 48 / 52 (92%)
- **Code Review Pass Rate**: Pending

## Restoration Instructions

### Quick Restore (< 5 minutes)
```bash
# 1. Navigate to working directory
cd /home/cabdru/project

# 2. Restore git state
git checkout feature/neural-authentication
# Already on correct branch, no stashed changes

# 3. Restore dependencies
# Already installed, verify:
npm ls jsonwebtoken bcryptjs redis

# 4. Restore memory state
npx claude-flow hooks session-restore \
  --session-id "neural-auth-feature-session-001" \
  --load-active-context true

# 5. Verify environment
npm run typecheck  # Should pass
npm test           # 92% coverage, 48/52 passing

# 6. Resume work
# Next: Complete integration tests (tests/auth.integration.test.ts)
# Review: docs/specs/04-context-templates/activeContext.md
```

### Full Restore (5-15 minutes)
```bash
# 1. Quick restore steps (above)

# 2. Restore running services
npm run dev              # Restart dev server on port 3000
redis-server             # Ensure Redis running on port 6379
# PostgreSQL already running

# 3. Restore agent coordination
npx claude-flow swarm init --topology mesh
npx claude-flow agent spawn --type "tester" --name "integration-tester"
npx claude-flow agent spawn --type "ml-developer" --name "neural-trainer"
npx claude-flow hooks notify \
  --agent "all" \
  --message "Session restored: neural-auth-feature-session-001"

# 4. Load decision context
# Review DEC-2025-11-27-002 (API Authentication Strategy)
cat docs/specs/04-context-templates/decisionLog.md

# Review Sprint 12 progress
cat docs/specs/04-context-templates/progressTracking.md

# 5. Validate restoration
npm run build    # Should succeed
npm test         # 48/52 tests passing (expected)
git status       # 6 files staged, 1 untracked (docs)

# 6. Confirm with team
# Post to team channel: "Resumed neural-auth session, 75% complete, targeting completion by EOD"
```

## Validation Checklist

### Environment
- [x] Correct git branch checked out (feature/neural-authentication)
- [x] All dependencies installed (jsonwebtoken, bcryptjs, redis, etc.)
- [x] Environment variables set correctly (.env file loaded)
- [x] Expected modified files (6 staged, 1 untracked doc)

### Build & Tests
- [x] Code compiles (npm run build succeeds)
- [x] Type checking passes (npm run typecheck succeeds)
- [x] Tests mostly pass (48/52 - 92%, 4 integration tests pending)
- [x] Linting passes (npm run lint succeeds)

### Context
- [x] Active context loaded and reviewed
- [x] Decision log reviewed (DEC-2025-11-27-002)
- [x] Progress tracking shows Sprint 12 at 68% (this feature contributes)
- [x] Blocker documented (staging infrastructure approval)

### Coordination
- [x] Agent states restored from memory
- [x] Pending handoffs identified (tester → security-auditor)
- [x] Shared state synchronized (auth endpoints, coverage)
- [ ] Team notified of session resumption (TODO: post to Slack)

### Memory
- [x] Session memory keys retrieved successfully
- [x] Neural enhancement state loaded (epoch 20/50)
- [x] Historical context available
- [x] No memory corruption detected

## Integration Commands

### Save Session (End of Day)
```bash
npx claude-flow hooks session-end \
  --session-id "neural-auth-feature-session-001" \
  --export-metrics true \
  --create-checkpoint true

# Output:
# ✅ Session state saved to memory
# ✅ Metrics exported to .claude-flow/metrics/
# ✅ Checkpoint created: checkpoint-2025-11-27-1730
# ✅ Restoration instructions generated
```

### Restore Session (Start of Day)
```bash
npx claude-flow hooks session-restore \
  --session-id "neural-auth-feature-session-001" \
  --load-active-context true \
  --restore-agent-state true \
  --validate-environment true

# Output:
# ✅ Memory state restored (7 keys)
# ✅ Active context loaded
# ✅ Agent coordination restored (4 agents)
# ✅ Environment validated (all checks passed)
# ⚠️  1 blocker found: staging-infrastructure-approval
#
# Next steps:
# 1. Complete integration tests (60% done)
# 2. Finish neural training (40% done)
# 3. Security review pending
```
```

## Integration Points

### 1. Memory System Integration
```bash
# Auto-save session every 30 minutes
npx claude-flow hooks auto-checkpoint \
  --interval 30 \
  --memory-persist true

# Retrieve last session
npx claude-flow memory retrieve \
  --key "session/last-active" \
  --namespace "development/sessions"

# List all sessions for project
npx claude-flow memory search \
  --pattern "session/.*neural-auth.*" \
  --namespace "development/sessions"
```

### 2. Active Context Integration
- Session restoration loads active context automatically
- Active context updated from session state
- Next steps populated from session objectives

### 3. Progress Tracking Integration
- Session progress contributes to sprint metrics
- Completed tasks update progress tracking
- Blockers from session escalated to progress

### 4. Decision Log Integration
- Session references relevant decisions
- Decisions made during session logged
- Restoration loads decision context

## Best Practices

### ✅ DO
- **Save session state frequently** (every 30-60 minutes)
- **Create checkpoints before risky operations** (major refactoring, etc.)
- **Validate restoration** before resuming work
- **Document blockers** in session state
- **Track file checksums** to detect corruption
- **Store in memory** for cross-machine access
- **Include next steps** for easy resumption
- **Test restoration process** regularly

### ❌ DON'T
- **Don't rely only on git** (memory state is critical)
- **Don't forget environment state** (node version, env vars)
- **Don't skip validation** after restoration
- **Don't lose checkpoint history** (archive, don't delete)
- **Don't ignore dirty git state** (document or clean up)
- **Don't assume dependencies are current** (verify after restore)
- **Don't skip team notification** on collaborative sessions

### Session Lifecycle

1. **Session Start**: Create session ID, initialize state
2. **Active Work**: Auto-checkpoint every 30 minutes
3. **Context Switch**: Save full state, mark as paused
4. **Session Resume**: Restore state, validate, resume work
5. **Session Complete**: Final save, mark complete, archive
6. **Session Failed**: Mark failed, store error state, create recovery checkpoint

### Checkpoint Strategy

**Frequent Checkpoints** (every 30 min):
- Lightweight memory-only
- Fast to create and restore
- For short interruptions

**Major Checkpoints** (before risky operations):
- Full state including git commit
- Includes file checksums
- For recovery from failures

**End-of-Day Checkpoints**:
- Complete session state
- Export metrics
- Generate restoration instructions

## Performance Optimization

- **Compress large file states** (only store diffs, not full content)
- **Lazy-load agent states** (only restore active agents)
- **Cache frequent checkpoints** in memory for fast access
- **Archive old checkpoints** (> 30 days) to separate storage
- **Index by session ID and timestamp** for O(1) lookup
- **Parallelize validation** (env, build, tests in parallel)

---

**Template Version**: 1.0.0
**Last Updated**: 2025-11-27
**Maintained By**: Claude Flow Blueprint Project
