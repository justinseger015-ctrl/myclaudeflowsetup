# TASK-NEURAL-005: Error Recovery & Rollback System

## Metadata
- **Task ID**: TASK-NEURAL-005
- **Requirements**: Implements REQ-NEURAL-12, REQ-NEURAL-13, REQ-NEURAL-14
- **Dependencies**: TASK-NEURAL-004 (Pattern Verification)
- **Enables**: TASK-NEURAL-006, TASK-NEURAL-007
- **Complexity**: MEDIUM
- **Estimated Time**: 20 minutes
- **Category**: Safety & Resilience

## Context

Implements comprehensive error recovery mechanisms for neural enhancement workflows. Provides cleanup procedures for failed operations, rollback capabilities to restore previous states, and structured error logging for debugging and analysis. Ensures system stability when neural operations fail.

## Core Functionality

### 1. Project Cleanup System
Cleans up resources from failed or cancelled neural enhancement projects:
- Agent lifecycle management
- Memory namespace cleanup
- Swarm destruction when empty
- Project state updates

### 2. Rollback Procedures
Restores system to previous checkpoint state:
- Checkpoint validation
- State restoration
- Resource cleanup
- Rollback logging

### 3. Error Logging System
Structured error capture and storage:
- Error metadata collection
- Phase-specific error tracking
- Memory-based error persistence
- Error analysis support

## Pseudo-code

```javascript
/**
 * CLEANUP FUNCTION FOR PROJECT
 * Cleans up all resources associated with a project
 */
async function cleanupProject(projectId) {
  console.log(`Starting cleanup for project: ${projectId}`);

  // 1. List all agents for this project
  const agents = await mcp__ruv-swarm__agent_list({ filter: "all" });
  const projectAgents = agents.filter(agent =>
    agent.id.includes(projectId) || agent.metadata?.project === projectId
  );

  console.log(`Found ${projectAgents.length} agents to clean up`);

  // 2. Store cleanup record before deletion
  const cleanupRecord = {
    projectId,
    timestamp: Date.now(),
    agentsDeleted: projectAgents.map(a => ({
      id: a.id,
      type: a.type,
      status: a.status
    })),
    reason: "manual_cleanup"
  };

  await bash(`npx claude-flow@alpha memory store cleanup-record-${projectId} '${JSON.stringify(cleanupRecord)}' --namespace "projects/${projectId}/cleanup"`);

  // 3. Mark agents as deleted (store deletion status)
  for (const agent of projectAgents) {
    const deletionRecord = {
      agentId: agent.id,
      deletedAt: Date.now(),
      projectId,
      finalStatus: agent.status
    };

    await bash(`npx claude-flow@alpha memory store agent-deleted-${agent.id} '${JSON.stringify(deletionRecord)}' --namespace "projects/${projectId}/agents"`);
  }

  // 4. Check if swarm is empty and destroy if needed
  const remainingAgents = await mcp__ruv-swarm__agent_list({ filter: "active" });

  if (remainingAgents.length === 0) {
    console.log("No active agents remaining, destroying swarm");
    await mcp__ruv-swarm__swarm_destroy({ swarmId: projectId });
  }

  // 5. Update project status to cleaned
  const projectStatus = {
    projectId,
    status: "cleaned",
    cleanedAt: Date.now(),
    agentsCleaned: projectAgents.length
  };

  await bash(`npx claude-flow@alpha memory store project-status '${JSON.stringify(projectStatus)}' --namespace "projects/${projectId}"`);

  console.log(`Cleanup completed for project: ${projectId}`);
  return cleanupRecord;
}

/**
 * ROLLBACK TO CHECKPOINT
 * Restores system to a previous checkpoint state
 */
async function rollbackToCheckpoint(projectId, checkpointId = "latest") {
  console.log(`Starting rollback for project: ${projectId}, checkpoint: ${checkpointId}`);

  // 1. Retrieve checkpoint from memory
  const checkpointResult = await bash(`npx claude-flow@alpha memory retrieve checkpoints/${projectId}`);
  const checkpoint = JSON.parse(checkpointResult);

  // 2. Verify rollback is possible
  if (!checkpoint.can_rollback) {
    const error = new Error("Rollback not allowed: checkpoint is not rollback-safe");
    logError(projectId, "rollback_validation", error);
    throw error;
  }

  console.log(`Checkpoint verified, proceeding with rollback`);

  // 3. Execute cleanup of current state
  try {
    await cleanupProject(projectId);
  } catch (cleanupError) {
    logError(projectId, "rollback_cleanup", cleanupError);
    throw new Error(`Cleanup failed during rollback: ${cleanupError.message}`);
  }

  // 4. Store rollback log
  const rollbackLog = {
    projectId,
    checkpointId: checkpoint.id,
    rolledBackAt: Date.now(),
    previousPhase: checkpoint.phase,
    reason: "error_recovery",
    success: true
  };

  await bash(`npx claude-flow@alpha memory store rollback-log-${Date.now()} '${JSON.stringify(rollbackLog)}' --namespace "projects/${projectId}/rollbacks"`);

  console.log(`Rollback completed successfully`);
  return rollbackLog;
}

/**
 * ERROR LOGGING
 * Logs structured error information to memory
 */
function logError(projectId, phase, error) {
  const errorLog = {
    projectId,
    phase,
    timestamp: Date.now(),
    errorMessage: error.message,
    errorStack: error.stack,
    errorType: error.constructor.name,
    severity: determineSeverity(phase, error),
    metadata: {
      agentCount: error.agentCount || 0,
      failedOperations: error.failedOperations || []
    }
  };

  // Store error log in project-specific namespace
  bash(`npx claude-flow@alpha memory store error-${Date.now()} '${JSON.stringify(errorLog)}' --namespace "projects/${projectId}/errors"`);

  console.error(`[ERROR] ${phase}: ${error.message}`);

  return errorLog;
}

/**
 * DETERMINE ERROR SEVERITY
 * Classifies error severity based on phase and error type
 */
function determineSeverity(phase, error) {
  // Critical phases where errors are high severity
  const criticalPhases = ["pattern_verification", "knowledge_sharing", "rollback"];

  if (criticalPhases.includes(phase)) {
    return "HIGH";
  }

  // Network/timeout errors are medium severity
  if (error.message.includes("timeout") || error.message.includes("network")) {
    return "MEDIUM";
  }

  // Default to low severity
  return "LOW";
}

/**
 * RETRIEVE ERROR LOGS
 * Gets all error logs for a project
 */
async function getErrorLogs(projectId) {
  const result = await bash(`npx claude-flow@alpha memory search "error-*" --namespace "projects/${projectId}/errors"`);
  const errors = JSON.parse(result);

  // Sort by timestamp descending (most recent first)
  return errors.sort((a, b) => b.timestamp - a.timestamp);
}
```

## Implementation Procedures

### Procedure 1: Cleanup Execution
```bash
# 1. List agents for project
npx ruv-swarm agent-list --filter all

# 2. Store cleanup record
npx claude-flow@alpha memory store cleanup-record-{project-id} '{...}' \
  --namespace "projects/{project-id}/cleanup"

# 3. Store agent deletion records
npx claude-flow@alpha memory store agent-deleted-{agent-id} '{...}' \
  --namespace "projects/{project-id}/agents"

# 4. Check remaining agents
npx ruv-swarm agent-list --filter active

# 5. Destroy swarm if empty
npx ruv-swarm swarm-destroy --swarm-id {project-id}

# 6. Update project status
npx claude-flow@alpha memory store project-status '{status: "cleaned"}' \
  --namespace "projects/{project-id}"
```

### Procedure 2: Rollback Process
```bash
# 1. Retrieve checkpoint
npx claude-flow@alpha memory retrieve checkpoints/{project-id}

# 2. Verify can_rollback flag
# (Check in retrieved JSON)

# 3. Execute cleanup
# (Run Procedure 1)

# 4. Store rollback log
npx claude-flow@alpha memory store rollback-log-{timestamp} '{...}' \
  --namespace "projects/{project-id}/rollbacks"
```

### Procedure 3: Error Logging
```bash
# 1. Capture error information
# (In code: error.message, error.stack, phase context)

# 2. Store error log
npx claude-flow@alpha memory store error-{timestamp} '{...}' \
  --namespace "projects/{project-id}/errors"

# 3. Retrieve error logs for analysis
npx claude-flow@alpha memory search "error-*" \
  --namespace "projects/{project-id}/errors"
```

## Validation Checklist

### Cleanup Validation
- [ ] All project agents identified correctly
- [ ] Cleanup record stored before deletion
- [ ] Agent deletion records created
- [ ] Swarm destroyed when empty
- [ ] Project status updated to "cleaned"

### Rollback Validation
- [ ] Checkpoint retrieved successfully
- [ ] `can_rollback` flag verified
- [ ] Cleanup executed before rollback
- [ ] Rollback log stored with metadata
- [ ] Previous state can be referenced

### Error Logging Validation
- [ ] Errors captured with full context
- [ ] Phase information included
- [ ] Severity correctly determined
- [ ] Errors stored in project namespace
- [ ] Error logs retrievable for analysis

## Integration Points

### Inputs from Previous Tasks
- **TASK-004**: Verification patterns that may fail requiring cleanup
- Checkpoint data structure from validation tasks

### Outputs to Next Tasks
- **TASK-007**: Error logs for testing failure scenarios
- **TASK-008**: Cleanup procedures for knowledge sharing failures
- **TASK-009**: Error recovery testing scenarios
- **TASK-010**: Rollback procedures for deployment failures

## Error Scenarios

### Cleanup Failures
- Agent list retrieval fails → Log error, continue with known agents
- Memory storage fails → Log to console, continue cleanup
- Swarm destruction fails → Log error, mark swarm for manual cleanup

### Rollback Failures
- Checkpoint not found → Throw error, cannot rollback
- `can_rollback` is false → Throw error with reason
- Cleanup fails during rollback → Log error, partial rollback state

### Logging Failures
- Memory storage unavailable → Fallback to console logging
- Invalid error object → Log basic message and phase

## Success Criteria

1. **Cleanup Success**: All project resources cleaned up, no orphaned agents
2. **Rollback Success**: System restored to checkpoint state, rollback logged
3. **Error Logging Success**: All errors captured with context, retrievable for analysis
4. **Resilience**: Procedures handle partial failures gracefully

## Notes

- Cleanup is **non-destructive** to memory records (stores deletion status, doesn't delete memories)
- Rollback requires explicit `can_rollback` flag in checkpoint
- Error severity determines escalation procedures
- All recovery operations are logged for audit trails
- Cleanup can be triggered manually or automatically on critical errors

## Forward References

- TASK-006 will use cleanup for knowledge sharing failures
- TASK-007 will test error recovery scenarios
- TASK-008 will integrate error logs for debugging
- TASK-010 will use rollback for deployment failures
