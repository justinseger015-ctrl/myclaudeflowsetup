# Neural Enhancement Implementation Prompt - IMMEDIATE (30 minutes)

## OBJECTIVE

You are implementing neural cognitive pattern enhancements for existing research agent swarms. This prompt covers:
1. Initializing DAA (Decentralized Autonomous Agents) with learning enabled
2. Assigning optimal cognitive patterns to all research agents
3. Verifying the configuration is active and working
4. **[NEW]** Establishing error recovery and cleanup mechanisms
5. **[NEW]** Creating project isolation and baseline metrics

## CONTEXT

The system has these neural capabilities available:
- **6 Cognitive Patterns**: convergent, divergent, lateral, systems, critical, adaptive
- **DAA Service**: Enables autonomous learning, peer coordination, neural integration
- **Knowledge Domains**: general, coordination, adaptation, neural, optimization

## ⚠️ CRITICAL SAFETY MEASURES

**Before starting, understand these risk mitigations:**

1. **Incremental Rollout**: Create agents in batches of 5-10, not all 35 at once
2. **Project Isolation**: Use unique project IDs to prevent knowledge contamination
3. **Error Recovery**: Transactional agent creation with rollback capability
4. **Performance Baselines**: Measure metrics BEFORE and AFTER neural enhancement
5. **Agent Lifecycle**: Cleanup strategy for completed projects

## PHASE 0: PRE-IMPLEMENTATION SETUP

### Step 0.1: Generate Unique Project ID

Create a unique identifier for this implementation to isolate from other projects:

```bash
# Generate unique project ID with timestamp
PROJECT_ID="neural-impl-$(date +%Y%m%d-%H%M%S)"
echo "Project ID: $PROJECT_ID"

# Store project metadata
npx claude-flow memory store "project-metadata" "{
  \"project_id\": \"$PROJECT_ID\",
  \"created_at\": \"$(date -Iseconds)\",
  \"status\": \"initializing\",
  \"agent_count\": 0,
  \"phase\": \"pre-implementation\"
}" --namespace "projects/$PROJECT_ID"
```

### Step 0.2: Capture Baseline Performance Metrics

**CRITICAL**: Measure performance WITHOUT neural enhancements first:

```javascript
// Capture baseline metrics
mcp__ruv-swarm__benchmark_run({
  type: "all",
  iterations: 5
})

// Store baseline for comparison
mcp__ruv-swarm__daa_performance_metrics({
  category: "all"
})
```

```bash
# Store baseline metrics with project ID
npx claude-flow memory store "baseline-metrics" "{
  \"project_id\": \"$PROJECT_ID\",
  \"captured_at\": \"$(date -Iseconds)\",
  \"note\": \"Metrics captured BEFORE neural enhancement\",
  \"benchmark_results\": \"<paste results here>\",
  \"system_metrics\": \"<paste metrics here>\"
}" --namespace "projects/$PROJECT_ID/baselines"
```

### Step 0.3: Create Error Recovery Checkpoint

```bash
# Create rollback point
npx claude-flow memory store "recovery-checkpoint" "{
  \"project_id\": \"$PROJECT_ID\",
  \"checkpoint_time\": \"$(date -Iseconds)\",
  \"swarm_state\": \"pre-initialization\",
  \"agent_count\": 0,
  \"can_rollback\": true
}" --namespace "projects/$PROJECT_ID/checkpoints"
```

---

## PHASE 1: INITIALIZE DAA SERVICE

### Step 1.1: Initialize DAA with Full Learning Capabilities

Execute this MCP tool call FIRST before any other operations:

```javascript
mcp__ruv-swarm__daa_init({
  enableLearning: true,
  enableCoordination: true,
  persistenceMode: "memory"
})
```

**Expected Response Structure**:
```json
{
  "success": true,
  "initialized": true,
  "features": {
    "autonomousLearning": true,
    "peerCoordination": true,
    "persistenceMode": "memory",
    "neuralIntegration": true,
    "cognitivePatterns": 6
  }
}
```

**Verification**: If `success: true` and `autonomousLearning: true`, proceed. If not, retry once then report error.

**Error Recovery**: If initialization fails, run:
```bash
npx claude-flow memory store "error-log" "{
  \"project_id\": \"$PROJECT_ID\",
  \"phase\": \"daa-init\",
  \"error\": \"<error message>\",
  \"timestamp\": \"$(date -Iseconds)\",
  \"action\": \"stopped-before-agent-creation\"
}" --namespace "projects/$PROJECT_ID/errors"
```

### Step 1.2: Initialize Swarm with Adaptive Strategy

Execute immediately after DAA init:

```javascript
mcp__ruv-swarm__swarm_init({
  topology: "hierarchical",
  maxAgents: 20,
  strategy: "adaptive"
})
```

**Why hierarchical**: Research swarms have natural coordinator → specialist structure.
**Why 20 agents**: Allows full PhD swarm (15+ agents) plus buffer.
**Why adaptive**: Neural networks optimize task routing automatically.

**Expected Response**: Look for `"cognitive_diversity": true` and `"neural_networks": true` in features.

---

## PHASE 2: COGNITIVE PATTERN ASSIGNMENTS

### Understanding Cognitive Patterns

| Pattern | Description | Optimal For |
|---------|-------------|-------------|
| **convergent** | Linear, focused, efficient | Bug fixes, precise execution, methodology writing, final synthesis |
| **divergent** | Creative, exploratory, multiple solutions | Literature exploration, option generation, brainstorming, hypothesis generation |
| **lateral** | Indirect, unconventional, cross-domain | Finding non-obvious connections, unique insights, leadership profiling |
| **systems** | Holistic, interconnected, big picture | Architecture, theory building, relationship mapping, company intelligence |
| **critical** | Analytical, evaluative, challenging | Gap analysis, adversarial review, risk assessment, contradiction finding |
| **adaptive** | Versatile, context-switching | General coordinators, orchestration agents |

### Step 2.1: PhD Research Agent Cognitive Assignments

**IMPORTANT**: Create agents in BATCHES of 5-10 to prevent resource exhaustion.

**Batch 1: Exploration Phase Agents (4 agents)**

Create each agent with its assigned cognitive pattern and PROJECT ISOLATION:

```javascript
// EXPLORATION PHASE AGENTS (Divergent + Critical)
// Batch 1 - Create with error handling
const batch1Agents = [
  {
    id: `literature-review-writer-${PROJECT_ID}`,
    capabilities: ["research", "synthesis", "writing", "thematic-analysis"],
    cognitivePattern: "divergent",
    enableMemory: true,
    learningRate: 0.1,
    metadata: { projectId: PROJECT_ID, batch: 1, created: new Date().toISOString() }
  },
  {
    id: `literature-mapper-${PROJECT_ID}`,
    capabilities: ["search", "categorization", "citation-tracking", "knowledge-mapping"],
    cognitivePattern: "divergent",
    enableMemory: true,
    learningRate: 0.1,
    metadata: { projectId: PROJECT_ID, batch: 1, created: new Date().toISOString() }
  },
  {
    id: `gap-hunter-${PROJECT_ID}`,
    capabilities: ["analysis", "gap-identification", "opportunity-finding"],
    cognitivePattern: "critical",
    enableMemory: true,
    learningRate: 0.12,
    metadata: { projectId: PROJECT_ID, batch: 1, created: new Date().toISOString() }
  },
  {
    id: `contradiction-analyzer-${PROJECT_ID}`,
    capabilities: ["conflict-detection", "reconciliation", "evidence-analysis"],
    cognitivePattern: "critical",
    enableMemory: true,
    learningRate: 0.12,
    metadata: { projectId: PROJECT_ID, batch: 1, created: new Date().toISOString() }
  }
];

// Create batch 1 with transaction-like behavior
let batch1Success = [];
let batch1Failures = [];

for (const agentConfig of batch1Agents) {
  try {
    const result = await mcp__ruv-swarm__daa_agent_create(agentConfig);
    batch1Success.push(agentConfig.id);
    console.log(`✓ Created: ${agentConfig.id}`);
  } catch (error) {
    batch1Failures.push({ id: agentConfig.id, error: error.message });
    console.error(`✗ Failed: ${agentConfig.id} - ${error.message}`);
  }
}

// Store batch 1 results
npx claude-flow memory store "batch-1-results" JSON.stringify({
  project_id: PROJECT_ID,
  batch: 1,
  success_count: batch1Success.length,
  failure_count: batch1Failures.length,
  successful_agents: batch1Success,
  failed_agents: batch1Failures,
  timestamp: new Date().toISOString()
}) --namespace "projects/$PROJECT_ID/agent-batches"

// STOP HERE if failures > 50%
if (batch1Failures.length > batch1Success.length) {
  console.error("CRITICAL: >50% batch 1 failures. STOPPING agent creation.");
  console.error("Run rollback: See Step 2.X for recovery procedure");
  throw new Error("Batch creation failure threshold exceeded");
}

// Wait 5 seconds before next batch to prevent resource saturation
await new Promise(resolve => setTimeout(resolve, 5000));

mcp__ruv-swarm__daa_agent_create({
  id: "literature-mapper",
  capabilities: ["search", "categorization", "citation-tracking", "knowledge-mapping"],
  cognitivePattern: "divergent",
  enableMemory: true,
  learningRate: 0.1
})

mcp__ruv-swarm__daa_agent_create({
  id: "gap-hunter",
  capabilities: ["analysis", "gap-identification", "opportunity-finding"],
  cognitivePattern: "critical",
  enableMemory: true,
  learningRate: 0.12
})

mcp__ruv-swarm__daa_agent_create({
  id: "contradiction-analyzer",
  capabilities: ["conflict-detection", "reconciliation", "evidence-analysis"],
  cognitivePattern: "critical",
  enableMemory: true,
  learningRate: 0.12
})

// SYNTHESIS PHASE AGENTS (Systems)
mcp__ruv-swarm__daa_agent_create({
  id: "theory-builder",
  capabilities: ["framework-construction", "concept-integration", "theoretical-modeling"],
  cognitivePattern: "systems",
  enableMemory: true,
  learningRate: 0.1
})

mcp__ruv-swarm__daa_agent_create({
  id: "thematic-synthesizer",
  capabilities: ["theme-identification", "pattern-recognition", "conceptual-clustering"],
  cognitivePattern: "systems",
  enableMemory: true,
  learningRate: 0.1
})

mcp__ruv-swarm__daa_agent_create({
  id: "synthesis-specialist",
  capabilities: ["cross-arc-synthesis", "strategic-integration", "positioning"],
  cognitivePattern: "systems",
  enableMemory: true,
  learningRate: 0.1
})

// GENERATION PHASE AGENTS (Divergent)
mcp__ruv-swarm__daa_agent_create({
  id: "hypothesis-generator",
  capabilities: ["hypothesis-formation", "testable-predictions", "theoretical-translation"],
  cognitivePattern: "divergent",
  enableMemory: true,
  learningRate: 0.1
})

mcp__ruv-swarm__daa_agent_create({
  id: "opportunity-identifier",
  capabilities: ["gap-to-opportunity", "research-question-generation", "novelty-detection"],
  cognitivePattern: "divergent",
  enableMemory: true,
  learningRate: 0.1
})

// EXECUTION PHASE AGENTS (Convergent)
mcp__ruv-swarm__daa_agent_create({
  id: "methodology-writer",
  capabilities: ["method-design", "protocol-writing", "replicability"],
  cognitivePattern: "convergent",
  enableMemory: true,
  learningRate: 0.08
})

mcp__ruv-swarm__daa_agent_create({
  id: "results-writer",
  capabilities: ["findings-presentation", "statistical-reporting", "data-visualization"],
  cognitivePattern: "convergent",
  enableMemory: true,
  learningRate: 0.08
})

mcp__ruv-swarm__daa_agent_create({
  id: "discussion-writer",
  capabilities: ["interpretation", "implications", "limitations-analysis"],
  cognitivePattern: "convergent",
  enableMemory: true,
  learningRate: 0.08
})

mcp__ruv-swarm__daa_agent_create({
  id: "conclusion-writer",
  capabilities: ["synthesis", "contribution-articulation", "future-directions"],
  cognitivePattern: "convergent",
  enableMemory: true,
  learningRate: 0.08
})

// QUALITY ASSURANCE AGENTS (Critical)
mcp__ruv-swarm__daa_agent_create({
  id: "adversarial-reviewer",
  capabilities: ["critique", "assumption-challenging", "weakness-identification"],
  cognitivePattern: "critical",
  enableMemory: true,
  learningRate: 0.15
})

mcp__ruv-swarm__daa_agent_create({
  id: "quality-assessor",
  capabilities: ["bias-detection", "validity-assessment", "rigor-evaluation"],
  cognitivePattern: "critical",
  enableMemory: true,
  learningRate: 0.12
})

mcp__ruv-swarm__daa_agent_create({
  id: "bias-detector",
  capabilities: ["publication-bias", "selection-bias", "systematic-bias-identification"],
  cognitivePattern: "critical",
  enableMemory: true,
  learningRate: 0.12
})

mcp__ruv-swarm__daa_agent_create({
  id: "validity-guardian",
  capabilities: ["internal-validity", "external-validity", "construct-validity"],
  cognitivePattern: "critical",
  enableMemory: true,
  learningRate: 0.12
})
```

### Step 2.2: Business Research Agent Cognitive Assignments

```javascript
// INTELLIGENCE GATHERING (Systems + Lateral)
mcp__ruv-swarm__daa_agent_create({
  id: "company-intelligence-researcher",
  capabilities: ["business-analysis", "market-positioning", "technology-assessment"],
  cognitivePattern: "systems",
  enableMemory: true,
  learningRate: 0.1
})

mcp__ruv-swarm__daa_agent_create({
  id: "leadership-profiler",
  capabilities: ["executive-analysis", "stakeholder-mapping", "influence-assessment"],
  cognitivePattern: "lateral",
  enableMemory: true,
  learningRate: 0.1
})

mcp__ruv-swarm__daa_agent_create({
  id: "competitive-intelligence",
  capabilities: ["competitor-analysis", "market-structure", "positioning-gaps"],
  cognitivePattern: "critical",
  enableMemory: true,
  learningRate: 0.12
})

// STRATEGY DEVELOPMENT (Systems + Convergent)
mcp__ruv-swarm__daa_agent_create({
  id: "strategic-positioning-analyst",
  capabilities: ["value-proposition", "differentiation", "market-fit"],
  cognitivePattern: "systems",
  enableMemory: true,
  learningRate: 0.1
})

mcp__ruv-swarm__daa_agent_create({
  id: "positioning-strategist",
  capabilities: ["positioning-development", "refinement", "validation"],
  cognitivePattern: "convergent",
  enableMemory: true,
  learningRate: 0.08
})

// COMMUNICATION (Divergent + Convergent)
mcp__ruv-swarm__daa_agent_create({
  id: "conversation-script-writer",
  capabilities: ["dialogue-crafting", "key-phrases", "discovery-questions"],
  cognitivePattern: "divergent",
  enableMemory: true,
  learningRate: 0.1
})

mcp__ruv-swarm__daa_agent_create({
  id: "sales-enablement-specialist",
  capabilities: ["cheat-sheets", "preparation-checklists", "objection-handling"],
  cognitivePattern: "convergent",
  enableMemory: true,
  learningRate: 0.08
})

mcp__ruv-swarm__daa_agent_create({
  id: "executive-brief-writer",
  capabilities: ["synthesis", "executive-summary", "actionable-deliverables"],
  cognitivePattern: "convergent",
  enableMemory: true,
  learningRate: 0.08
})

// ORCHESTRATION (Adaptive)
mcp__ruv-swarm__daa_agent_create({
  id: "research-orchestrator",
  capabilities: ["workflow-coordination", "agent-direction", "synthesis-management"],
  cognitivePattern: "adaptive",
  enableMemory: true,
  learningRate: 0.1
})
```

### Step 2.3: Business Strategy Agent Cognitive Assignments

```javascript
// ANALYSIS AGENTS (Critical + Systems)
mcp__ruv-swarm__daa_agent_create({
  id: "problem-validator",
  capabilities: ["problem-assessment", "severity-analysis", "market-validation"],
  cognitivePattern: "critical",
  enableMemory: true,
  learningRate: 0.12
})

mcp__ruv-swarm__daa_agent_create({
  id: "risk-analyst",
  capabilities: ["fmea", "failure-mode-analysis", "risk-quantification"],
  cognitivePattern: "critical",
  enableMemory: true,
  learningRate: 0.12
})

mcp__ruv-swarm__daa_agent_create({
  id: "gap-analyzer",
  capabilities: ["gap-identification", "opportunity-assessment", "priority-ranking"],
  cognitivePattern: "critical",
  enableMemory: true,
  learningRate: 0.12
})

// EXPLORATION AGENTS (Divergent + Lateral)
mcp__ruv-swarm__daa_agent_create({
  id: "opportunity-generator",
  capabilities: ["opportunity-synthesis", "innovation-identification", "strategic-options"],
  cognitivePattern: "divergent",
  enableMemory: true,
  learningRate: 0.1
})

mcp__ruv-swarm__daa_agent_create({
  id: "strategic-researcher",
  capabilities: ["web-research", "data-collection", "trend-analysis"],
  cognitivePattern: "divergent",
  enableMemory: true,
  learningRate: 0.1
})

// MAPPING AGENTS (Systems)
mcp__ruv-swarm__daa_agent_create({
  id: "structural-mapper",
  capabilities: ["architecture-mapping", "component-analysis", "relationship-identification"],
  cognitivePattern: "systems",
  enableMemory: true,
  learningRate: 0.1
})

mcp__ruv-swarm__daa_agent_create({
  id: "flow-analyst",
  capabilities: ["data-flow", "process-flow", "bottleneck-identification"],
  cognitivePattern: "systems",
  enableMemory: true,
  learningRate: 0.1
})

// META AGENTS (Adaptive)
mcp__ruv-swarm__daa_agent_create({
  id: "meta-learning-orchestrator",
  capabilities: ["principle-extraction", "pattern-transfer", "meta-analysis"],
  cognitivePattern: "adaptive",
  enableMemory: true,
  learningRate: 0.1
})

mcp__ruv-swarm__daa_agent_create({
  id: "step-back-analyzer",
  capabilities: ["principle-extraction", "high-level-analysis", "criteria-establishment"],
  cognitivePattern: "systems",
  enableMemory: true,
  learningRate: 0.1
})
```

---

## PHASE 3: VERIFICATION

### Step 3.1: Verify All Agents Created

```javascript
mcp__ruv-swarm__agent_list({
  filter: "all"
})
```

**Expected**: List showing all created agents with their cognitive patterns.

### Step 3.2: Verify Learning Status

```javascript
mcp__ruv-swarm__daa_learning_status({
  detailed: true
})
```

**Expected**:
- `total_learning_cycles`: 0 (fresh start)
- `knowledge_domains`: Should include general, coordination, adaptation, neural, optimization
- All agents should appear in detailed metrics

### Step 3.3: Verify Cognitive Pattern Effectiveness

For each agent category, run pattern analysis:

```javascript
mcp__ruv-swarm__daa_cognitive_pattern({
  agentId: "adversarial-reviewer",
  action: "analyze"
})
```

**Expected**: `pattern_effectiveness` should be > 0.7

---

## PHASE 3.5: ERROR RECOVERY AND CLEANUP PROCEDURES

### Step 3.5.1: Agent Cleanup Strategy

**When to cleanup**: After research project completes, failed initialization, or testing

```javascript
// Function to cleanup agents by project ID
async function cleanupProject(projectId) {
  // 1. List all agents for this project
  const agents = await mcp__ruv-swarm__agent_list({ filter: "all" });

  // 2. Filter agents belonging to this project
  const projectAgents = agents.filter(a => a.id.includes(projectId));

  // 3. Store cleanup record BEFORE deletion
  await npx claude-flow memory store `cleanup-record-${projectId}` JSON.stringify({
    project_id: projectId,
    cleanup_started: new Date().toISOString(),
    agents_to_delete: projectAgents.map(a => a.id),
    reason: "project-completion"
  }) --namespace `projects/${projectId}/lifecycle`;

  // 4. Delete agents one by one
  for (const agent of projectAgents) {
    try {
      // Note: Add agent deletion when available, currently store as "deleted"
      await npx claude-flow memory store `agent-deleted-${agent.id}` JSON.stringify({
        agent_id: agent.id,
        deleted_at: new Date().toISOString(),
        project_id: projectId
      }) --namespace `projects/${projectId}/deleted-agents`;

      console.log(`✓ Marked for deletion: ${agent.id}`);
    } catch (error) {
      console.error(`✗ Failed to delete: ${agent.id}`);
    }
  }

  // 5. Destroy swarm if empty
  const remainingAgents = await mcp__ruv-swarm__agent_list({ filter: "active" });
  if (remainingAgents.length === 0) {
    await mcp__ruv-swarm__swarm_destroy();
  }

  // 6. Update project status
  await npx claude-flow memory store `project-status-${projectId}` JSON.stringify({
    project_id: projectId,
    status: "cleaned-up",
    completed_at: new Date().toISOString()
  }) --namespace `projects/${projectId}`;
}
```

### Step 3.5.2: Rollback Procedure

**If agent creation fails midway:**

```bash
# 1. Stop all ongoing operations
# 2. List created agents
mcp__ruv-swarm__agent_list({ filter: "all" })

# 3. Store failure state
npx claude-flow memory store "rollback-initiated" "{
  \"project_id\": \"$PROJECT_ID\",
  \"rollback_time\": \"$(date -Iseconds)\",
  \"reason\": \"agent-creation-failure\",
  \"partial_agents_created\": \"<count>\"
}" --namespace "projects/$PROJECT_ID/rollback"

# 4. Cleanup partial agents
# Execute cleanupProject(PROJECT_ID) function above

# 5. Mark project as failed
npx claude-flow memory store "project-status" "{
  \"project_id\": \"$PROJECT_ID\",
  \"status\": \"failed-rolled-back\",
  \"timestamp\": \"$(date -Iseconds)\"
}" --namespace "projects/$PROJECT_ID"
```

### Step 3.5.3: Project Isolation Verification

**Verify agents are properly isolated:**

```javascript
// Check agent IDs contain project ID
const agents = await mcp__ruv-swarm__agent_list({ filter: "all" });
const isolatedAgents = agents.filter(a => a.id.includes(PROJECT_ID));
const contaminatedAgents = agents.filter(a => !a.id.includes(PROJECT_ID));

if (contaminatedAgents.length > 0) {
  console.warn(`WARNING: ${contaminatedAgents.length} agents without project isolation found`);
  console.warn("These may interfere with other projects:", contaminatedAgents.map(a => a.id));
}

// Store isolation check
await npx claude-flow memory store `isolation-check-${PROJECT_ID}` JSON.stringify({
  project_id: PROJECT_ID,
  isolated_count: isolatedAgents.length,
  contaminated_count: contaminatedAgents.length,
  check_time: new Date().toISOString(),
  status: contaminatedAgents.length === 0 ? "clean" : "contaminated"
}) --namespace `projects/${PROJECT_ID}/quality-checks`;
```

---

## PHASE 4: STORE CONFIGURATION IN MEMORY

After all agents are created, store the configuration for future reference (WITH PROJECT ISOLATION):

```bash
npx claude-flow memory store "neural-agent-config" "{
  \"project_id\": \"$PROJECT_ID\",
  \"phd_agents\": {
    \"divergent\": [\"literature-review-writer-$PROJECT_ID\", \"literature-mapper-$PROJECT_ID\", \"hypothesis-generator-$PROJECT_ID\", \"opportunity-identifier-$PROJECT_ID\"],
    \"critical\": [\"gap-hunter-$PROJECT_ID\", \"contradiction-analyzer-$PROJECT_ID\", \"adversarial-reviewer-$PROJECT_ID\", \"quality-assessor-$PROJECT_ID\", \"bias-detector-$PROJECT_ID\", \"validity-guardian-$PROJECT_ID\"],
    \"systems\": [\"theory-builder-$PROJECT_ID\", \"thematic-synthesizer-$PROJECT_ID\", \"synthesis-specialist-$PROJECT_ID\"],
    \"convergent\": [\"methodology-writer-$PROJECT_ID\", \"results-writer-$PROJECT_ID\", \"discussion-writer-$PROJECT_ID\", \"conclusion-writer-$PROJECT_ID\"]
  },
  "business_research_agents": {
    "systems": ["company-intelligence-researcher", "strategic-positioning-analyst"],
    "lateral": ["leadership-profiler"],
    "critical": ["competitive-intelligence"],
    "divergent": ["conversation-script-writer"],
    "convergent": ["positioning-strategist", "sales-enablement-specialist", "executive-brief-writer"],
    "adaptive": ["research-orchestrator"]
  },
  "business_strategy_agents": {
    "critical": ["problem-validator", "risk-analyst", "gap-analyzer"],
    "divergent": ["opportunity-generator", "strategic-researcher"],
    "systems": ["structural-mapper", "flow-analyst", "step-back-analyzer"],
    "adaptive": ["meta-learning-orchestrator"]
  },
  \"initialized_at\": \"$(date -Iseconds)\",
  \"daa_enabled\": true,
  \"learning_enabled\": true,
  \"isolation_mode\": \"project-scoped\",
  \"cleanup_strategy\": \"automatic-on-completion\"
}" --namespace "projects/$PROJECT_ID/config"

# Also store in global config for cross-project reference
npx claude-flow memory store "active-projects" "{
  \"projects\": [\"$PROJECT_ID\"],
  \"last_updated\": \"$(date -Iseconds)\"
}" --namespace "config/neural/active-projects"
```

---

## SUCCESS CRITERIA

Before marking this implementation complete, verify:

### Core Implementation
- [ ] **Baseline metrics captured** BEFORE neural enhancement
- [ ] **Project ID generated** and stored in all agent IDs
- [ ] **Error recovery checkpoints** created
- [ ] DAA initialized with `autonomousLearning: true`
- [ ] Swarm initialized with `cognitive_diversity: true`
- [ ] All PhD research agents created (17 agents) **in batches**
- [ ] All business research agents created (9 agents) **in batches**
- [ ] All business strategy agents created (9 agents) **in batches**
- [ ] Each agent has correct cognitive pattern assigned
- [ ] Configuration stored in memory at `projects/$PROJECT_ID/config`
- [ ] `daa_learning_status` shows all agents

### Safety & Quality
- [ ] **Agent isolation verified** (all IDs contain project ID)
- [ ] **Batch creation logs** stored for each batch
- [ ] **Cleanup procedure** tested and documented
- [ ] **Rollback procedure** documented and ready
- [ ] **Performance comparison** baseline vs neural (after usage)
- [ ] **Resource monitoring** shows acceptable memory/CPU usage
- [ ] **No contamination** from other projects detected

### Post-Implementation
- [ ] **Implementation log** created in `docs2/neural-implementation-log.md`
- [ ] **Actual metrics** captured after first research cycle
- [ ] **Effectiveness scores** calculated (target: >0.7 for all agents)
- [ ] **Knowledge flow test** passed (see Phase 3.5.3)

---

## TROUBLESHOOTING

### Issue: Agent creation fails
**Root Cause**: DAA not initialized, resource exhaustion, or network issues
**Solution**:
1. Check DAA status: `mcp__ruv-swarm__daa_learning_status({})`
2. Re-run `daa_init` if needed
3. If resource issues, reduce batch size to 3-5 agents
4. Check system resources: `mcp__ruv-swarm__memory_usage({ detail: "detailed" })`

### Issue: Batch creation >50% failure rate
**Root Cause**: System overload, configuration errors, or MCP connection issues
**Solution**: Execute rollback procedure (Step 3.5.2), investigate logs, retry with smaller batch size

### Issue: Cognitive pattern not applied
**Root Cause**: Agent doesn't exist or pattern name typo
**Solution**:
1. Verify agent exists: `agent_list({ filter: "all" })`
2. Check pattern name (exact: convergent, divergent, lateral, systems, critical, adaptive)
3. Reassign: `daa_cognitive_pattern({ agentId: "<id>", action: "change", pattern: "<pattern>" })`

### Issue: Memory store fails
**Root Cause**: ReasoningBank not initialized or namespace collision
**Solution**:
1. Initialize: `npx claude-flow agent memory init`
2. Check namespace doesn't exist: `npx claude-flow memory retrieve --key "<namespace>/<key>"`
3. Use unique keys with timestamps if needed

### Issue: Agents from different projects interfering
**Root Cause**: Project isolation not implemented correctly
**Solution**:
1. Run isolation check (Step 3.5.3)
2. Cleanup contaminated agents
3. Ensure all new agents include `${PROJECT_ID}` in ID

### Issue: Memory/CPU usage too high
**Root Cause**: Too many agents created simultaneously
**Solution**:
1. Check metrics: `daa_performance_metrics({ category: "system" })`
2. Destroy unused swarms: `swarm_destroy({ swarmId: "<id>" })`
3. Cleanup completed projects: `cleanupProject("<project-id>")`
4. Reduce batch size in future creations

### Issue: Can't measure neural enhancement effectiveness
**Root Cause**: No baseline metrics captured
**Solution**:
1. If possible, run same research task WITHOUT neural agents
2. Compare results qualitatively
3. For future: ALWAYS capture baselines (Step 0.2)

### Issue: Pattern staleness (old patterns contaminating new research)
**Root Cause**: No pattern expiry implemented
**Solution**: (Temporary mitigation until short-term prompt adds expiry)
1. Manual review: `npx claude-flow memory retrieve --key "patterns/<domain>/successful/*"`
2. Delete outdated: `npx claude-flow memory delete --key "<key>"`
3. Add creation dates to all patterns going forward

---

## RESOURCE MONITORING

After implementation, continuously monitor:

```bash
# System health check
mcp__ruv-swarm__daa_performance_metrics({ category: "system" })

# Memory usage
mcp__ruv-swarm__memory_usage({ detail: "by-agent" })

# Agent effectiveness
mcp__ruv-swarm__daa_learning_status({ detailed: true })

# Swarm health
mcp__ruv-swarm__swarm_status({ verbose: true })
```

**Warning Thresholds:**
- Memory usage >80%: Cleanup old projects
- Agent effectiveness <0.6: Review cognitive pattern assignment
- Swarm response time >5s: Reduce agent count
- Learning rate drift >0.05: Reassess adaptation feedback

---

## NEXT STEPS

After completing this prompt:

1. **Immediate (30 min)**: Document implementation in `docs2/neural-implementation-log.md`
2. **First Research Cycle (1-2 hours)**: Run pilot project, capture actual performance
3. **Performance Review (15 min)**: Compare baseline vs neural-enhanced metrics
4. **Optimization (30 min)**: Adjust learning rates, cognitive patterns based on results
5. **Proceed to Short-term**: Only after successful pilot - `neural-enhancement-short-term.md` for:
   - Knowledge sharing hooks between agents
   - Successful research pattern storage
   - Cross-agent learning workflows
   - Pattern expiry mechanisms
   - Cross-project isolation improvements

**DO NOT proceed to short-term implementation until:**
- ✅ All agents created successfully
- ✅ Baseline metrics captured and stored
- ✅ Pilot research completed
- ✅ Neural enhancement shows measurable benefit (>10% improvement)
- ✅ Resource usage within acceptable limits (<70% memory/CPU)
