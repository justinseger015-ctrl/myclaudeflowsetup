# TASK-NEURAL-001: ReasoningBank & Project Isolation Setup

```xml
<task_spec id="TASK-NEURAL-001" version="1.0">
<metadata>
  <title>Setup ReasoningBank and Project Isolation</title>
  <status>ready</status>
  <implements>
    <requirement_ref>REQ-NEURAL-01</requirement_ref>
    <requirement_ref>REQ-NEURAL-02</requirement_ref>
  </implements>
  <depends_on>
    <task_ref>NONE (First task)</task_ref>
  </depends_on>
  <estimated_complexity>low</estimated_complexity>
  <estimated_time>15 minutes</estimated_time>
</metadata>

<context>
This is the FIRST task in neural enhancement implementation. It initializes the ReasoningBank memory system and creates project isolation infrastructure. All subsequent tasks depend on this foundation.

CRITICAL: This task must complete successfully before any other neural enhancement work begins.

The ReasoningBank system provides:
- Persistent memory across agent sessions
- Project isolation via namespacing
- Recovery checkpoints for rollback
- Shared knowledge coordination between agents

This task establishes the memory foundation that all 13 neural enhancement tasks will use.
</context>

<prerequisites>
  <check>Claude Flow installed: npx claude-flow@alpha --version</check>
  <check>Working directory is project root: /home/cabdru/claudeflowblueprint</check>
  <check>No existing neural enhancement projects running</check>
  <check>Memory system accessible</check>
</prerequisites>

<scope>
  <in_scope>
    - Initialize ReasoningBank memory system
    - Generate unique PROJECT_ID with timestamp
    - Create project metadata namespace
    - Store baseline configuration
    - Verify memory system operational
    - Create recovery checkpoint for rollback
    - Establish namespace patterns for future tasks
  </in_scope>
  <out_of_scope>
    - Agent creation (TASK-003)
    - DAA initialization (TASK-002)
    - Knowledge sharing setup (TASK-008)
    - Batch agent spawning (TASK-003)
    - Any implementation work
  </out_of_scope>
</scope>

<pseudo_code>
#!/bin/bash
# TASK-NEURAL-001: ReasoningBank & Project Isolation Setup

echo "=== STEP 1: Initialize ReasoningBank Memory System ==="
npx claude-flow@alpha agent memory init
npx claude-flow@alpha agent memory status
# Expected output: "Memory system initialized" or similar confirmation

echo "=== STEP 2: Generate Unique PROJECT_ID ==="
PROJECT_ID="neural-impl-$(date +%Y%m%d-%H%M%S)"
echo "Generated PROJECT_ID: $PROJECT_ID"
echo "This ID will be used by all 13 tasks for namespace isolation"

echo "=== STEP 3: Store Project Metadata ==="
# IMPORTANT: Using positional args syntax - store "key" 'value' --namespace "ns"
npx claude-flow memory store "project-metadata" "{
  \"project_id\": \"$PROJECT_ID\",
  \"created_at\": \"$(date -Iseconds)\",
  \"status\": \"initializing\",
  \"agent_count\": 0,
  \"phase\": \"pre-implementation\",
  \"task_sequence\": [
    \"TASK-NEURAL-001\",
    \"TASK-NEURAL-002\",
    \"TASK-NEURAL-003\",
    \"TASK-NEURAL-004\",
    \"TASK-NEURAL-005\",
    \"TASK-NEURAL-006\",
    \"TASK-NEURAL-007\",
    \"TASK-NEURAL-008\",
    \"TASK-NEURAL-009\",
    \"TASK-NEURAL-010\",
    \"TASK-NEURAL-011\",
    \"TASK-NEURAL-012\",
    \"TASK-NEURAL-013\"
  ]
}" --namespace "projects/$PROJECT_ID"

echo "=== STEP 4: Create Recovery Checkpoint ==="
npx claude-flow memory store "recovery-checkpoint" "{
  \"project_id\": \"$PROJECT_ID\",
  \"checkpoint_time\": \"$(date -Iseconds)\",
  \"swarm_state\": \"pre-initialization\",
  \"agent_count\": 0,
  \"can_rollback\": true,
  \"checkpoint_type\": \"baseline\",
  \"description\": \"Initial state before neural enhancement implementation\"
}" --namespace "projects/$PROJECT_ID/checkpoints"

echo "=== STEP 5: Store Namespace Pattern Documentation ==="
npx claude-flow memory store "namespace-patterns" "{
  \"project_root\": \"projects/$PROJECT_ID\",
  \"patterns\": {
    \"metadata\": \"projects/$PROJECT_ID\",
    \"checkpoints\": \"projects/$PROJECT_ID/checkpoints\",
    \"implementation\": \"projects/$PROJECT_ID/implementation\",
    \"agents\": \"projects/$PROJECT_ID/agents/[agent-id]\",
    \"shared_knowledge\": \"projects/$PROJECT_ID/knowledge\",
    \"task_status\": \"projects/$PROJECT_ID/tasks\"
  },
  \"usage_notes\": \"All tasks should use these namespace patterns for consistency\"
}" --namespace "projects/$PROJECT_ID"

echo "=== STEP 6: Verify Memory System ==="
echo "Retrieving project metadata to verify storage..."
npx claude-flow memory retrieve --key "project-metadata" --namespace "projects/$PROJECT_ID"

echo "Retrieving recovery checkpoint to verify checkpoint system..."
npx claude-flow memory retrieve --key "recovery-checkpoint" --namespace "projects/$PROJECT_ID/checkpoints"

echo "Retrieving namespace patterns to verify documentation..."
npx claude-flow memory retrieve --key "namespace-patterns" --namespace "projects/$PROJECT_ID"

echo "=== STEP 7: Store Task Completion ==="
npx claude-flow memory store "task-001-complete" "{
  \"task_id\": \"TASK-NEURAL-001\",
  \"status\": \"completed\",
  \"project_id\": \"$PROJECT_ID\",
  \"completed_at\": \"$(date -Iseconds)\",
  \"next_task\": \"TASK-NEURAL-002\",
  \"artifacts_created\": [
    \"project_id\",
    \"project_metadata\",
    \"recovery_checkpoint\",
    \"namespace_patterns\"
  ]
}" --namespace "projects/$PROJECT_ID/implementation"

echo ""
echo "==================================================================="
echo "TASK-NEURAL-001 COMPLETED SUCCESSFULLY"
echo "==================================================================="
echo "PROJECT_ID: $PROJECT_ID"
echo ""
echo "Next Task: TASK-NEURAL-002 (DAA Initialization)"
echo "Dependencies Ready: ReasoningBank initialized, PROJECT_ID available"
echo "==================================================================="
</pseudo_code>

<files_to_create>
  <file path="NONE">All work is memory-based using ReasoningBank</file>
</files_to_create>

<files_to_modify>
  <file path="NONE">No file modifications required</file>
</files_to_modify>

<validation_criteria>
  <criterion id="V1">Memory system status shows "initialized" or equivalent confirmation</criterion>
  <criterion id="V2">PROJECT_ID successfully generated with format: neural-impl-YYYYMMDD-HHMMSS</criterion>
  <criterion id="V3">Project metadata stored and retrievable from namespace: projects/$PROJECT_ID</criterion>
  <criterion id="V4">Recovery checkpoint exists in namespace: projects/$PROJECT_ID/checkpoints</criterion>
  <criterion id="V5">Namespace patterns documented and retrievable</criterion>
  <criterion id="V6">No errors in any command execution</criterion>
  <criterion id="V7">Task completion record stored in implementation namespace</criterion>
</validation_criteria>

<test_commands>
  <command description="Check memory system status">
    npx claude-flow@alpha agent memory status
  </command>
  <command description="Query for project metadata">
    npx claude-flow memory query "project-metadata"
  </command>
  <command description="Retrieve recovery checkpoint (replace $PROJECT_ID with actual value)">
    npx claude-flow memory retrieve --key "recovery-checkpoint" --namespace "projects/$PROJECT_ID/checkpoints"
  </command>
  <command description="Verify namespace patterns stored">
    npx claude-flow memory retrieve --key "namespace-patterns" --namespace "projects/$PROJECT_ID"
  </command>
  <command description="Confirm task completion record">
    npx claude-flow memory retrieve --key "task-001-complete" --namespace "projects/$PROJECT_ID/implementation"
  </command>
</test_commands>

<forward_looking_context>
**Next Task (TASK-NEURAL-002 - DAA Initialization)** will need:
- PROJECT_ID from this task's memory store
- Confirmation that ReasoningBank is operational
- Access to project metadata namespace: projects/$PROJECT_ID
- Namespace patterns for storing DAA configuration

**How TASK-002 retrieves PROJECT_ID:**
```bash
# Option 1: Query for project metadata
PROJECT_DATA=$(npx claude-flow memory query "project-metadata" | jq -r '.project_id')

# Option 2: List recent projects and select latest
npx claude-flow memory list --namespace "projects"
```

**Future Tasks (TASK-003 to TASK-013)** will use:
- PROJECT_ID for agent naming convention: [role]-[agent-name]-$PROJECT_ID
  - Example: literature-mapper-neural-impl-20250127-143022
- Namespace pattern: projects/$PROJECT_ID/[area]/[key]
  - agents/[agent-id] - Individual agent state
  - knowledge - Shared knowledge base
  - tasks - Task status tracking
  - implementation - Implementation progress
- Recovery checkpoint for rollback procedures
- Task completion records for dependency tracking

**Memory Retrieval Pattern for Subsequent Tasks:**
```bash
# Every task should start with:
PROJECT_ID=$(npx claude-flow memory query "project-metadata" | jq -r '.project_id')
echo "Using PROJECT_ID: $PROJECT_ID"

# Check previous task completion:
npx claude-flow memory retrieve --key "task-[XXX]-complete" --namespace "projects/$PROJECT_ID/implementation"
```

**Critical Dependencies Established:**
1. ReasoningBank operational - enables all future memory operations
2. PROJECT_ID generated - provides namespace isolation
3. Namespace patterns defined - ensures consistency across all 13 tasks
4. Recovery checkpoint - enables rollback if needed
5. Task tracking initialized - provides audit trail
</forward_looking_context>

<memory_storage>
# Store task completion record
npx claude-flow memory store "task-001-complete" "{
  \"task_id\": \"TASK-NEURAL-001\",
  \"status\": \"completed\",
  \"project_id\": \"$PROJECT_ID\",
  \"completed_at\": \"$(date -Iseconds)\",
  \"next_task\": \"TASK-NEURAL-002\",
  \"artifacts_created\": [
    \"project_id\",
    \"project_metadata\",
    \"recovery_checkpoint\",
    \"namespace_patterns\"
  ],
  \"validation_passed\": true
}" --namespace "projects/$PROJECT_ID/implementation"

# Update project metadata with task progress
npx claude-flow memory store "project-metadata" "{
  \"project_id\": \"$PROJECT_ID\",
  \"created_at\": \"$(date -Iseconds)\",
  \"status\": \"task-001-complete\",
  \"agent_count\": 0,
  \"phase\": \"foundation-established\",
  \"tasks_completed\": [\"TASK-NEURAL-001\"],
  \"current_task\": \"TASK-NEURAL-002\"
}" --namespace "projects/$PROJECT_ID"
</memory_storage>

<troubleshooting>
**Issue**: Memory init fails with "command not found"
**Solution**:
1. Check Claude Flow version: npx claude-flow@alpha --version
2. Reinstall if needed: npm install -g @ruvnet/claude-flow@alpha
3. Verify PATH includes npm global binaries

**Issue**: Memory init fails with "already initialized"
**Solution**: This is OK - memory system is already ready. Proceed to Step 2.

**Issue**: PROJECT_ID generation fails
**Solution**:
- Ensure `date` command available (should work on Linux/Mac/WSL)
- Manual alternative: PROJECT_ID="neural-impl-$(python3 -c 'import datetime; print(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))')"

**Issue**: Memory store returns syntax error
**Solution**:
- Verify using positional args: store "key" 'value' --namespace "ns"
- Ensure JSON is properly escaped in bash (use single quotes around JSON)
- Check for proper quote escaping within JSON strings

**Issue**: Memory retrieve returns "not found"
**Solution**:
1. Verify namespace spelling matches store command exactly
2. List all keys in namespace: npx claude-flow memory list --namespace "projects/$PROJECT_ID"
3. Check if PROJECT_ID variable is set correctly: echo $PROJECT_ID

**Issue**: Date command not available
**Solution**: Install coreutils package or use Python alternative above

**Issue**: jq not available for parsing (in forward-looking tasks)
**Solution**: Install jq: sudo apt-get install jq (Debian/Ubuntu) or brew install jq (Mac)
</troubleshooting>

<success_indicators>
When this task is complete, you should see:
1. ✅ Memory system status confirms initialization
2. ✅ PROJECT_ID echoed to console (save this for reference)
3. ✅ Three successful memory retrieve operations showing stored data
4. ✅ No error messages in console output
5. ✅ Task completion record confirms "completed" status

Example successful output:
```
Generated PROJECT_ID: neural-impl-20250127-143022
Memory system initialized
✓ Project metadata stored
✓ Recovery checkpoint created
✓ Namespace patterns documented
✓ Task completion recorded

TASK-NEURAL-001 COMPLETED SUCCESSFULLY
Next Task: TASK-NEURAL-002
```
</success_indicators>

</task_spec>
```

## Implementation Notes

**Critical Success Factors:**
1. Memory system must be operational before proceeding
2. PROJECT_ID must be captured and documented
3. All memory stores must succeed with verification
4. Namespace patterns must be established for future tasks

**For Task Executor:**
- Copy the pseudo-code section into a bash script
- Execute line by line, verifying each step
- Save PROJECT_ID to a temporary file for reference: `echo $PROJECT_ID > /tmp/neural-project-id.txt`
- Proceed to TASK-NEURAL-002 only after all validation criteria pass

**Memory Coordination:**
This task establishes the memory foundation. All subsequent tasks (002-013) will rely on:
- The PROJECT_ID stored in this task
- The namespace patterns defined here
- The recovery checkpoint mechanism
- The task completion tracking system
