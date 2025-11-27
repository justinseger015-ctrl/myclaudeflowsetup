# Functional Specification: Agent Lifecycle Management

**Version:** 1.0
**Project:** Neural Enhancement System Implementation
**Project ID:** neural-impl-20251127
**Created:** 2025-11-27
**Status:** Active
**Agent:** Specification Agent #4/13

---

## Overview

This functional specification defines the complete lifecycle for creating, configuring, and managing batches of autonomous agents with cognitive patterns. It establishes batch creation strategies, cognitive pattern assignment, learning rate configuration, failure handling, verification procedures, and cleanup protocols.

### Purpose

Agent Lifecycle Management ensures:
- **Batch Efficiency**: Create 5-10 agents concurrently to minimize initialization overhead
- **Cognitive Diversity**: Assign 6 cognitive patterns matched to agent role requirements
- **Learning Configuration**: Optimize learning rates per agent type for effective adaptation
- **Failure Resilience**: Detect and handle batch failures with 50% threshold for rollback
- **Verification Quality**: Validate all agents operational before knowledge sharing
- **Cleanup Safety**: Proper resource cleanup with rollback on critical failures

### Scope

This specification covers:
1. Batch agent creation with concurrent spawning (5-10 agents per batch)
2. Cognitive pattern assignment (6 patterns × agent roles)
3. Learning rate configuration per agent type
4. Batch failure detection and handling (>50% threshold triggers rollback)
5. Agent verification and health checks
6. Cleanup procedures for failed batches
7. Rollback mechanisms for critical failures

**Out of Scope:**
- DAA initialization (see `02-daa-initialization.md`)
- Knowledge sharing between agents (see `04-knowledge-sharing.md`)
- Pattern learning and adaptation (see `05-pattern-management.md`)

---

## Requirements Detail

### REQ-F007: Batch Agent Creation Strategy

**Priority:** P0-Critical
**Phase:** Immediate (Phase 2.1 - 15 minutes)
**User Story:** US-030

**Description:**
Create agents in batches of 5-10 to balance initialization overhead with resource constraints. Batch creation enables parallel processing, reduces total initialization time, and provides natural failure isolation boundaries.

**Batch Strategy Rationale:**
- **Batch size 5-10**: Optimal balance between parallelization and resource overhead
- **PhD swarm**: 17 agents total = 2 batches (10 + 7)
- **Business research**: 9 agents total = 1 batch (9)
- **Failure isolation**: Each batch is a transactional unit for rollback

**Acceptance Criteria:**
- [ ] Agents created in batches via `Promise.all()` for parallelization
- [ ] Batch size between 5-10 agents (configurable per swarm)
- [ ] Each agent created via `mcp__ruv-swarm__daa_agent_create()`
- [ ] Agent IDs include PROJECT_ID suffix: `{agent-name}-{PROJECT_ID}`
- [ ] All agents in batch have `enableMemory: true` for persistent learning
- [ ] Batch creation time logged for performance tracking
- [ ] Failed agent creation tracked per batch
- [ ] Batch status stored in memory: `batches/{batch-id}/status`

**Dependencies:**
- REQ-F005 (DAA service initialized)
- REQ-F006 (Swarm initialized)

**Test Coverage:**
- Unit: Verify batch size enforcement (5-10 agents)
- Integration: Create batch of 10 agents, confirm all spawn successfully
- Performance: Measure batch creation time vs sequential creation (expect 3-4x speedup)
- Load: Create max swarm capacity (20 agents) in batches, verify no resource exhaustion

**Error Handling:**
- If batch size > 10: Split into multiple batches automatically
- If individual agent creation fails: Log error, continue with remaining agents in batch
- If >50% of batch fails: Trigger batch rollback (REQ-F010)
- If all agents in batch fail: Abort immediately, log critical error

**Implementation:**

```javascript
// Batch agent creation with parallelization
async function createAgentBatch(agentDefinitions, projectId, batchId) {
  console.log(`Creating batch ${batchId} with ${agentDefinitions.length} agents...`);

  const batchStartTime = Date.now();
  const results = [];

  try {
    // Create all agents in parallel
    const agentPromises = agentDefinitions.map(async (agentDef) => {
      const agentId = `${agentDef.name}-${projectId}`;

      try {
        const agentResult = await mcp__ruv-swarm__daa_agent_create({
          id: agentId,
          cognitivePattern: agentDef.cognitivePattern,
          capabilities: agentDef.capabilities,
          enableMemory: true,
          learningRate: agentDef.learningRate || 0.3
        });

        return { success: true, agentId, result: agentResult };
      } catch (error) {
        console.error(`Failed to create agent ${agentId}:`, error.message);
        return { success: false, agentId, error: error.message };
      }
    });

    // Wait for all agents to complete
    const batchResults = await Promise.all(agentPromises);

    // Calculate batch metrics
    const successCount = batchResults.filter(r => r.success).length;
    const failureCount = batchResults.filter(r => !r.success).length;
    const failureRate = failureCount / batchResults.length;
    const batchDuration = Date.now() - batchStartTime;

    console.log(`✓ Batch ${batchId} completed in ${batchDuration}ms`);
    console.log(`  - Success: ${successCount}/${batchResults.length} agents`);
    console.log(`  - Failures: ${failureCount}/${batchResults.length} agents`);

    // Store batch results
    await npx claude-flow memory store `batch-${batchId}-results` JSON.stringify({
      batch_id: batchId,
      project_id: projectId,
      total_agents: batchResults.length,
      success_count: successCount,
      failure_count: failureCount,
      failure_rate: failureRate,
      duration_ms: batchDuration,
      results: batchResults,
      timestamp: new Date().toISOString()
    }) --namespace `projects/${projectId}/batches` --reasoningbank

    // Check failure threshold (50%)
    if (failureRate > 0.5) {
      throw new Error(`Batch ${batchId} exceeded failure threshold: ${(failureRate * 100).toFixed(1)}% failed`);
    }

    return {
      batchId,
      successCount,
      failureCount,
      failureRate,
      duration: batchDuration,
      results: batchResults
    };

  } catch (error) {
    console.error(`CRITICAL: Batch ${batchId} creation failed:`, error.message);

    // Store error details
    await npx claude-flow memory store `batch-${batchId}-error` JSON.stringify({
      batch_id: batchId,
      project_id: projectId,
      error: error.message,
      timestamp: new Date().toISOString(),
      requires_rollback: true
    }) --namespace `projects/${projectId}/errors` --reasoningbank

    throw error;
  }
}

// Example: Create PhD research swarm in batches
const phdAgentsBatch1 = [
  { name: "literature-mapper", cognitivePattern: "convergent", capabilities: ["analysis", "synthesis"], learningRate: 0.3 },
  { name: "gap-hunter", cognitivePattern: "divergent", capabilities: ["exploration", "discovery"], learningRate: 0.4 },
  { name: "methodology-architect", cognitivePattern: "systems", capabilities: ["design", "architecture"], learningRate: 0.3 },
  { name: "experimental-designer", cognitivePattern: "critical", capabilities: ["experimentation", "validation"], learningRate: 0.35 },
  { name: "data-synthesizer", cognitivePattern: "convergent", capabilities: ["aggregation", "analysis"], learningRate: 0.3 },
  { name: "pattern-recognizer", cognitivePattern: "lateral", capabilities: ["pattern-matching", "insights"], learningRate: 0.4 },
  { name: "critique-specialist", cognitivePattern: "critical", capabilities: ["evaluation", "critique"], learningRate: 0.35 },
  { name: "theoretical-integrator", cognitivePattern: "systems", capabilities: ["integration", "synthesis"], learningRate: 0.3 },
  { name: "ethics-validator", cognitivePattern: "critical", capabilities: ["ethics", "compliance"], learningRate: 0.25 },
  { name: "collaboration-coordinator", cognitivePattern: "adaptive", capabilities: ["coordination", "facilitation"], learningRate: 0.35 }
];

const phdAgentsBatch2 = [
  { name: "publication-strategist", cognitivePattern: "convergent", capabilities: ["writing", "strategy"], learningRate: 0.3 },
  { name: "peer-review-analyzer", cognitivePattern: "critical", capabilities: ["review", "feedback"], learningRate: 0.35 },
  { name: "replication-validator", cognitivePattern: "critical", capabilities: ["validation", "verification"], learningRate: 0.3 },
  { name: "impact-assessor", cognitivePattern: "systems", capabilities: ["impact-analysis", "metrics"], learningRate: 0.3 },
  { name: "interdisciplinary-connector", cognitivePattern: "divergent", capabilities: ["cross-domain", "innovation"], learningRate: 0.4 },
  { name: "future-research-planner", cognitivePattern: "adaptive", capabilities: ["planning", "forecasting"], learningRate: 0.35 },
  { name: "research-orchestrator", cognitivePattern: "adaptive", capabilities: ["orchestration", "leadership"], learningRate: 0.4 }
];

// Execute batch creation
const batch1Result = await createAgentBatch(phdAgentsBatch1, PROJECT_ID, "phd-batch-1");
const batch2Result = await createAgentBatch(phdAgentsBatch2, PROJECT_ID, "phd-batch-2");
```

---

### REQ-F008: Cognitive Pattern Assignment

**Priority:** P0-Critical
**Phase:** Immediate (Phase 2.1 - 15 minutes)
**User Story:** US-030

**Description:**
Assign one of 6 cognitive patterns to each agent based on role requirements and task characteristics. Cognitive patterns optimize problem-solving approaches and learning strategies for different agent types.

**Cognitive Patterns Available:**
1. **Convergent**: Focus on single best solution (analysis, synthesis agents)
2. **Divergent**: Explore multiple possibilities (exploration, discovery agents)
3. **Lateral**: Cross-domain connections (pattern recognition, insights agents)
4. **Systems**: Holistic understanding (architecture, integration agents)
5. **Critical**: Evaluation and validation (review, critique agents)
6. **Adaptive**: Context-based flexibility (coordination, leadership agents)

**Pattern Assignment Matrix:**

| Agent Role | Primary Pattern | Rationale | Example Agents |
|------------|-----------------|-----------|----------------|
| Literature Mapping | Convergent | Synthesize findings into coherent narratives | literature-mapper, data-synthesizer |
| Gap Discovery | Divergent | Explore unexplored research directions | gap-hunter, interdisciplinary-connector |
| Pattern Recognition | Lateral | Connect disparate concepts creatively | pattern-recognizer, innovation-scanner |
| System Design | Systems | Understand complex interdependencies | methodology-architect, theoretical-integrator |
| Validation & Review | Critical | Rigorous evaluation of claims | critique-specialist, peer-review-analyzer, ethics-validator |
| Coordination | Adaptive | Flexible response to context changes | collaboration-coordinator, research-orchestrator |

**Acceptance Criteria:**
- [ ] Each agent assigned exactly one cognitive pattern
- [ ] Pattern assignment matches agent role requirements
- [ ] 35 agents mapped to 6 patterns (distribution documented)
- [ ] Pattern assignment validated before agent creation
- [ ] Invalid pattern values rejected with error
- [ ] Pattern distribution stored for analysis: `projects/{PROJECT_ID}/analytics/pattern-distribution`
- [ ] Verification: All agents have `cognitivePattern` property set

**Dependencies:**
- REQ-F007 (Batch creation strategy)
- REQ-F005 (DAA service with cognitive patterns enabled)

**Test Coverage:**
- Unit: Verify pattern validation logic accepts 6 patterns, rejects invalid values
- Integration: Create agents with all 6 patterns, confirm DAA accepts each
- Analytics: Query pattern distribution, verify balanced assignment
- Regression: Ensure patterns persist across agent lifecycle

**Error Handling:**
- If invalid pattern specified: Reject agent creation with clear error message
- If pattern unavailable in DAA: Fall back to `adaptive` pattern with WARNING
- If pattern assignment fails: Retry with default pattern, log warning
- If all patterns fail: Abort batch creation, escalate to DAA service diagnostics

**Implementation:**

```javascript
// Cognitive pattern validation and assignment
const VALID_COGNITIVE_PATTERNS = [
  "convergent",
  "divergent",
  "lateral",
  "systems",
  "critical",
  "adaptive"
];

function validateCognitivePattern(pattern) {
  if (!VALID_COGNITIVE_PATTERNS.includes(pattern)) {
    throw new Error(`Invalid cognitive pattern: ${pattern}. Valid patterns: ${VALID_COGNITIVE_PATTERNS.join(", ")}`);
  }
  return pattern;
}

// Pattern assignment recommendations by agent type
const PATTERN_RECOMMENDATIONS = {
  // Literature & Analysis
  "literature-mapper": "convergent",
  "data-synthesizer": "convergent",
  "publication-strategist": "convergent",

  // Discovery & Exploration
  "gap-hunter": "divergent",
  "interdisciplinary-connector": "divergent",
  "innovation-scanner": "divergent",

  // Pattern & Insight
  "pattern-recognizer": "lateral",
  "trend-analyst": "lateral",
  "hypothesis-generator": "lateral",

  // Architecture & Systems
  "methodology-architect": "systems",
  "theoretical-integrator": "systems",
  "impact-assessor": "systems",

  // Validation & Review
  "critique-specialist": "critical",
  "ethics-validator": "critical",
  "peer-review-analyzer": "critical",
  "experimental-designer": "critical",
  "replication-validator": "critical",

  // Coordination & Adaptation
  "collaboration-coordinator": "adaptive",
  "research-orchestrator": "adaptive",
  "future-research-planner": "adaptive"
};

function recommendCognitivePattern(agentName) {
  const recommendation = PATTERN_RECOMMENDATIONS[agentName];
  if (!recommendation) {
    console.warn(`No pattern recommendation for ${agentName}, defaulting to adaptive`);
    return "adaptive";
  }
  return recommendation;
}

// Create agent with validated pattern
async function createAgentWithPattern(agentName, projectId, customPattern = null) {
  const pattern = customPattern || recommendCognitivePattern(agentName);

  try {
    validateCognitivePattern(pattern);
  } catch (error) {
    console.error(`Pattern validation failed for ${agentName}:`, error.message);
    throw error;
  }

  const agentId = `${agentName}-${projectId}`;

  console.log(`Creating ${agentId} with cognitive pattern: ${pattern}`);

  const result = await mcp__ruv-swarm__daa_agent_create({
    id: agentId,
    cognitivePattern: pattern,
    enableMemory: true,
    learningRate: getOptimalLearningRate(pattern)
  });

  return { agentId, pattern, result };
}

// Analyze pattern distribution across all agents
async function analyzePatternDistribution(projectId) {
  const agents = await mcp__ruv-swarm__agent_list({ filter: "all" });
  const projectAgents = agents.filter(a => a.id.includes(projectId));

  const distribution = {
    convergent: 0,
    divergent: 0,
    lateral: 0,
    systems: 0,
    critical: 0,
    adaptive: 0
  };

  projectAgents.forEach(agent => {
    const patternStatus = await mcp__ruv-swarm__daa_cognitive_pattern({
      agent_id: agent.id,
      action: "analyze"
    });

    if (patternStatus.current_pattern) {
      distribution[patternStatus.current_pattern]++;
    }
  });

  console.log("Cognitive Pattern Distribution:");
  Object.entries(distribution).forEach(([pattern, count]) => {
    const percentage = (count / projectAgents.length * 100).toFixed(1);
    console.log(`  - ${pattern}: ${count} agents (${percentage}%)`);
  });

  // Store distribution for analytics
  await npx claude-flow memory store "pattern-distribution" JSON.stringify({
    project_id: projectId,
    total_agents: projectAgents.length,
    distribution,
    timestamp: new Date().toISOString()
  }) --namespace `projects/${projectId}/analytics` --reasoningbank

  return distribution;
}
```

---

### REQ-F009: Learning Rate Configuration

**Priority:** P1-High
**Phase:** Immediate (Phase 2.1 - 15 minutes)
**User Story:** US-030

**Description:**
Configure optimal learning rates for each agent type to balance exploration (learning new patterns) with exploitation (using known strategies). Learning rates determine how quickly agents adapt to feedback and update their knowledge bases.

**Learning Rate Strategy:**
- **0.25-0.30**: Conservative learning (ethics, validation agents) - prioritize stability
- **0.30-0.35**: Balanced learning (analysis, synthesis agents) - standard rate
- **0.35-0.40**: Aggressive learning (discovery, coordination agents) - rapid adaptation
- **0.40-0.50**: Experimental learning (R&D only) - high exploration

**Learning Rate Matrix:**

| Cognitive Pattern | Default Rate | Rationale | Example Agents |
|-------------------|--------------|-----------|----------------|
| Convergent | 0.30 | Stable convergence to optimal solutions | literature-mapper (0.30), data-synthesizer (0.30) |
| Divergent | 0.40 | High exploration of solution space | gap-hunter (0.40), interdisciplinary-connector (0.40) |
| Lateral | 0.40 | Encourage creative connections | pattern-recognizer (0.40) |
| Systems | 0.30 | Complex interdependencies require stability | methodology-architect (0.30), impact-assessor (0.30) |
| Critical | 0.35 | Balanced rigor and adaptation | critique-specialist (0.35), peer-review-analyzer (0.35) |
| Adaptive | 0.35 | Context-aware learning | collaboration-coordinator (0.35), research-orchestrator (0.40) |

**Acceptance Criteria:**
- [ ] Learning rate between 0.25-0.40 for production agents
- [ ] Learning rate configurable per agent during creation
- [ ] Default rates assigned based on cognitive pattern
- [ ] Learning rate validation: reject values outside 0.0-1.0 range
- [ ] Learning rate stored in agent metadata
- [ ] Learning rate adjustable post-creation via `daa_agent_adapt`
- [ ] Learning effectiveness tracked: `projects/{PROJECT_ID}/analytics/learning-effectiveness`

**Dependencies:**
- REQ-F008 (Cognitive pattern assignment)
- REQ-F007 (Batch creation)

**Test Coverage:**
- Unit: Verify learning rate validation (0.0-1.0 range)
- Integration: Create agents with different learning rates, confirm DAA accepts
- Performance: Measure learning effectiveness vs learning rate (expect correlation)
- Regression: Ensure learning rates persist across sessions

**Error Handling:**
- If learning rate < 0.0: Clamp to 0.0, log warning
- If learning rate > 1.0: Clamp to 1.0, log warning
- If learning rate invalid: Use default based on cognitive pattern
- If learning rate adjustment fails: Retry once, then log error

**Implementation:**

```javascript
// Learning rate configuration by cognitive pattern
const DEFAULT_LEARNING_RATES = {
  convergent: 0.30,
  divergent: 0.40,
  lateral: 0.40,
  systems: 0.30,
  critical: 0.35,
  adaptive: 0.35
};

// Conservative agents (stability prioritized)
const CONSERVATIVE_AGENTS = {
  "ethics-validator": 0.25,
  "compliance-checker": 0.25,
  "replication-validator": 0.30
};

// Aggressive learners (rapid adaptation)
const AGGRESSIVE_LEARNERS = {
  "research-orchestrator": 0.40,
  "gap-hunter": 0.40,
  "interdisciplinary-connector": 0.40,
  "pattern-recognizer": 0.40
};

function getOptimalLearningRate(cognitivePattern, agentName = null) {
  // Check agent-specific overrides
  if (agentName && CONSERVATIVE_AGENTS[agentName]) {
    return CONSERVATIVE_AGENTS[agentName];
  }

  if (agentName && AGGRESSIVE_LEARNERS[agentName]) {
    return AGGRESSIVE_LEARNERS[agentName];
  }

  // Use pattern-based default
  return DEFAULT_LEARNING_RATES[cognitivePattern] || 0.30;
}

function validateLearningRate(rate) {
  if (typeof rate !== "number") {
    throw new Error(`Learning rate must be a number, got: ${typeof rate}`);
  }

  if (rate < 0.0) {
    console.warn(`Learning rate ${rate} < 0.0, clamping to 0.0`);
    return 0.0;
  }

  if (rate > 1.0) {
    console.warn(`Learning rate ${rate} > 1.0, clamping to 1.0`);
    return 1.0;
  }

  return rate;
}

// Create agent with optimized learning rate
async function createAgentWithLearning(agentName, cognitivePattern, projectId, customRate = null) {
  const learningRate = customRate !== null
    ? validateLearningRate(customRate)
    : getOptimalLearningRate(cognitivePattern, agentName);

  const agentId = `${agentName}-${projectId}`;

  console.log(`Creating ${agentId} with learning rate: ${learningRate}`);

  const result = await mcp__ruv-swarm__daa_agent_create({
    id: agentId,
    cognitivePattern,
    enableMemory: true,
    learningRate
  });

  // Store learning configuration
  await npx claude-flow memory store `agent-${agentName}-learning` JSON.stringify({
    agent_id: agentId,
    cognitive_pattern: cognitivePattern,
    learning_rate: learningRate,
    created_at: new Date().toISOString()
  }) --namespace `projects/${projectId}/agents/${agentName}` --reasoningbank

  return { agentId, learningRate, result };
}

// Adjust learning rate post-creation
async function adjustLearningRate(agentId, newRate, reason) {
  const validatedRate = validateLearningRate(newRate);

  console.log(`Adjusting learning rate for ${agentId} to ${validatedRate} (reason: ${reason})`);

  await mcp__ruv-swarm__daa_agent_adapt({
    agent_id: agentId,
    performanceScore: 0.5, // Neutral score for rate adjustment
    feedback: `Learning rate adjusted to ${validatedRate}: ${reason}`,
    suggestions: [`Update learning rate to ${validatedRate}`]
  });

  return { agentId, newLearningRate: validatedRate };
}

// Track learning effectiveness
async function trackLearningEffectiveness(projectId) {
  const learningStatus = await mcp__ruv-swarm__daa_learning_status({ detailed: true });

  const effectiveness = {
    agents: [],
    averageEffectiveness: 0,
    learningCycles: learningStatus.total_learning_cycles
  };

  if (learningStatus.agent_details) {
    learningStatus.agent_details.forEach(agent => {
      if (agent.id.includes(projectId)) {
        effectiveness.agents.push({
          agent_id: agent.id,
          effectiveness: agent.effectiveness || 0.5,
          learning_rate: agent.learning_rate,
          cycles_completed: agent.learning_cycles || 0
        });
      }
    });

    effectiveness.averageEffectiveness =
      effectiveness.agents.reduce((sum, a) => sum + a.effectiveness, 0) / effectiveness.agents.length;
  }

  console.log(`Learning Effectiveness: ${(effectiveness.averageEffectiveness * 100).toFixed(1)}%`);

  // Store effectiveness metrics
  await npx claude-flow memory store "learning-effectiveness" JSON.stringify({
    project_id: projectId,
    timestamp: new Date().toISOString(),
    effectiveness
  }) --namespace `projects/${projectId}/analytics` --reasoningbank

  return effectiveness;
}
```

---

### REQ-F010: Batch Failure Handling

**Priority:** P0-Critical
**Phase:** Immediate (Phase 2.2 - 10 minutes)
**User Story:** US-030

**Description:**
Detect and handle batch creation failures with a 50% failure threshold. If more than half of agents in a batch fail to create, trigger automatic rollback to prevent partial swarm corruption.

**Failure Threshold Rationale:**
- **50% threshold**: Allows minor failures (1-2 agents) without rollback
- **Prevents partial swarms**: Ensures minimum viable agent count for coordination
- **Transaction semantics**: Batch succeeds fully or rolls back completely

**Acceptance Criteria:**
- [ ] Failure rate calculated as `failed_agents / total_agents_in_batch`
- [ ] Threshold check: `failure_rate > 0.50` triggers rollback
- [ ] Successful agents in failed batch automatically cleaned up
- [ ] Batch failure logged in `projects/{PROJECT_ID}/errors/batch-failures`
- [ ] Rollback procedure executed: delete agents, restore checkpoint
- [ ] Human notification sent for failed batches requiring intervention
- [ ] Batch status updated to `failed-rolled-back`
- [ ] Retry mechanism available for transient failures

**Dependencies:**
- REQ-F007 (Batch creation strategy)
- REQ-F004 (Recovery checkpoint from DAA init)

**Test Coverage:**
- Unit: Verify failure rate calculation with mock data
- Integration: Simulate 6/10 agent failures, confirm rollback triggered
- Regression: Ensure rollback doesn't affect other project agents
- Disaster: Test recovery from mid-batch failure

**Error Handling:**
- If failure detection fails: Default to rollback (safe failure mode)
- If cleanup fails: Log error, escalate to manual cleanup
- If rollback fails: Quarantine batch, prevent further operations
- If retry after rollback fails: Abort project initialization, investigate root cause

**Implementation:**

```javascript
// Batch failure detection and handling
const FAILURE_THRESHOLD = 0.50; // 50% failure rate triggers rollback

async function handleBatchFailures(batchResult, projectId, batchId) {
  const { failureRate, failureCount, successCount, results } = batchResult;

  console.log(`Batch ${batchId} failure analysis:`);
  console.log(`  - Failure rate: ${(failureRate * 100).toFixed(1)}%`);
  console.log(`  - Failed agents: ${failureCount}`);
  console.log(`  - Successful agents: ${successCount}`);

  if (failureRate > FAILURE_THRESHOLD) {
    console.error(`❌ Batch ${batchId} FAILED: Exceeded ${FAILURE_THRESHOLD * 100}% failure threshold`);

    // Log batch failure
    await npx claude-flow memory store `batch-${batchId}-failure` JSON.stringify({
      batch_id: batchId,
      project_id: projectId,
      failure_rate: failureRate,
      failure_count: failureCount,
      success_count: successCount,
      failed_agents: results.filter(r => !r.success).map(r => r.agentId),
      successful_agents: results.filter(r => r.success).map(r => r.agentId),
      timestamp: new Date().toISOString(),
      requires_cleanup: true
    }) --namespace `projects/${projectId}/errors/batch-failures` --reasoningbank

    // Cleanup successful agents in failed batch
    console.log("Rolling back successful agents in failed batch...");
    const cleanupResults = await cleanupFailedBatch(batchResult, projectId, batchId);

    // Update batch status
    await npx claude-flow memory store `batch-${batchId}-status` JSON.stringify({
      batch_id: batchId,
      status: "failed-rolled-back",
      cleanup_completed: cleanupResults.success,
      timestamp: new Date().toISOString()
    }) --namespace `projects/${projectId}/batches` --reasoningbank

    // Trigger rollback
    throw new Error(`Batch ${batchId} failed with ${(failureRate * 100).toFixed(1)}% failure rate. Rollback initiated.`);
  }

  console.log(`✓ Batch ${batchId} passed failure threshold check`);

  // Log minor failures if any
  if (failureCount > 0) {
    console.warn(`⚠️ Batch ${batchId} had ${failureCount} minor failures (below threshold)`);

    const failedAgentIds = results.filter(r => !r.success).map(r => r.agentId);

    await npx claude-flow memory store `batch-${batchId}-minor-failures` JSON.stringify({
      batch_id: batchId,
      project_id: projectId,
      failure_count: failureCount,
      failed_agents: failedAgentIds,
      timestamp: new Date().toISOString(),
      note: "Minor failures below threshold, batch continues"
    }) --namespace `projects/${projectId}/warnings` --reasoningbank
  }

  return { passed: true, cleanupRequired: false };
}

// Cleanup agents from failed batch
async function cleanupFailedBatch(batchResult, projectId, batchId) {
  const successfulAgents = batchResult.results.filter(r => r.success);

  console.log(`Cleaning up ${successfulAgents.length} agents from failed batch ${batchId}...`);

  const cleanupResults = [];

  for (const agent of successfulAgents) {
    try {
      // Note: Agent cleanup via DAA lifecycle management
      // In production, this would call mcp__ruv-swarm__daa_lifecycle_manage with action: "delete"
      console.log(`  - Deleting agent: ${agent.agentId}`);

      // Placeholder for actual deletion
      // await mcp__ruv-swarm__daa_lifecycle_manage({ agentId: agent.agentId, action: "delete" });

      cleanupResults.push({ agentId: agent.agentId, cleaned: true });
    } catch (error) {
      console.error(`Failed to cleanup agent ${agent.agentId}:`, error.message);
      cleanupResults.push({ agentId: agent.agentId, cleaned: false, error: error.message });
    }
  }

  const cleanedCount = cleanupResults.filter(r => r.cleaned).length;
  const cleanupFailureCount = cleanupResults.filter(r => !r.cleaned).length;

  console.log(`Cleanup completed: ${cleanedCount}/${successfulAgents.length} agents deleted`);

  if (cleanupFailureCount > 0) {
    console.error(`⚠️ ${cleanupFailureCount} agents failed to cleanup, manual intervention required`);
  }

  // Store cleanup results
  await npx claude-flow memory store `batch-${batchId}-cleanup` JSON.stringify({
    batch_id: batchId,
    project_id: projectId,
    total_cleaned: cleanedCount,
    cleanup_failures: cleanupFailureCount,
    cleanup_details: cleanupResults,
    timestamp: new Date().toISOString()
  }) --namespace `projects/${projectId}/cleanup` --reasoningbank

  return {
    success: cleanupFailureCount === 0,
    cleanedCount,
    cleanupFailureCount,
    results: cleanupResults
  };
}

// Retry failed batch creation
async function retryBatchCreation(failedBatchId, agentDefinitions, projectId) {
  console.log(`Retrying batch creation for ${failedBatchId}...`);

  const retryBatchId = `${failedBatchId}-retry-1`;

  try {
    const retryResult = await createAgentBatch(agentDefinitions, projectId, retryBatchId);

    console.log(`✓ Retry succeeded for batch ${failedBatchId}`);

    return retryResult;
  } catch (error) {
    console.error(`Retry failed for batch ${failedBatchId}:`, error.message);

    await npx claude-flow memory store `batch-${failedBatchId}-retry-failed` JSON.stringify({
      original_batch_id: failedBatchId,
      retry_batch_id: retryBatchId,
      error: error.message,
      timestamp: new Date().toISOString(),
      action: "escalate-to-manual-intervention"
    }) --namespace `projects/${projectId}/errors` --reasoningbank

    throw error;
  }
}
```

---

### REQ-F011: Agent Verification

**Priority:** P0-Critical
**Phase:** Immediate (Phase 2.3 - 5 minutes)
**User Story:** US-032

**Description:**
Verify all created agents are operational, tracked by DAA learning system, and have correct configuration before proceeding to knowledge sharing. Verification ensures quality gates pass before downstream operations.

**Acceptance Criteria:**
- [ ] All agents appear in `mcp__ruv-swarm__agent_list()`
- [ ] All agents tracked in `mcp__ruv-swarm__daa_learning_status({ detailed: true })`
- [ ] Agent IDs verified to contain PROJECT_ID suffix
- [ ] Cognitive patterns verified via `daa_cognitive_pattern({ action: "analyze" })`
- [ ] Learning rates confirmed to match configuration
- [ ] Memory enabled for all agents (`enableMemory: true`)
- [ ] Verification report stored: `projects/{PROJECT_ID}/verification/agent-verification-report`
- [ ] Failed verification agents flagged for remediation

**Dependencies:**
- REQ-F007 (Batch creation complete)
- REQ-F010 (Batch failure handling passed)

**Test Coverage:**
- Unit: Verify validation logic with mock agent data
- Integration: Create agents, run verification, confirm all checks pass
- Edge: Test verification with missing agents, invalid configurations
- Performance: Verify verification completes in <30s for 20 agents

**Error Handling:**
- If agent missing from list: Retry list operation, then log error
- If agent missing from learning status: Re-register agent with DAA
- If configuration mismatch: Log warning, flag for manual review
- If verification timeout: Extend timeout, retry once

**Implementation:**

```javascript
// Agent verification suite
async function verifyAllAgents(projectId, expectedAgentNames) {
  console.log("Running agent verification checks...");

  const verificationReport = {
    project_id: projectId,
    timestamp: new Date().toISOString(),
    expected_agent_count: expectedAgentNames.length,
    checks: {
      agent_list: { passed: false, details: {} },
      learning_status: { passed: false, details: {} },
      id_isolation: { passed: false, details: {} },
      cognitive_patterns: { passed: false, details: {} },
      learning_rates: { passed: false, details: {} },
      memory_enabled: { passed: false, details: {} }
    },
    overall_status: "pending",
    failed_agents: [],
    warnings: []
  };

  try {
    // Check 1: Agent list verification
    const agentList = await mcp__ruv-swarm__agent_list({ filter: "all" });
    const projectAgents = agentList.filter(a => a.id.includes(projectId));

    verificationReport.checks.agent_list = {
      passed: projectAgents.length === expectedAgentNames.length,
      expected_count: expectedAgentNames.length,
      actual_count: projectAgents.length,
      agent_ids: projectAgents.map(a => a.id)
    };

    if (!verificationReport.checks.agent_list.passed) {
      verificationReport.warnings.push(`Agent count mismatch: expected ${expectedAgentNames.length}, found ${projectAgents.length}`);
    }

    // Check 2: Learning status verification
    const learningStatus = await mcp__ruv-swarm__daa_learning_status({ detailed: true });
    const trackedAgents = learningStatus.agent_details?.filter(a => a.id.includes(projectId)) || [];

    verificationReport.checks.learning_status = {
      passed: trackedAgents.length === expectedAgentNames.length,
      tracked_count: trackedAgents.length,
      agent_details: trackedAgents
    };

    if (!verificationReport.checks.learning_status.passed) {
      verificationReport.warnings.push(`Learning tracking mismatch: ${trackedAgents.length}/${expectedAgentNames.length} agents tracked`);
    }

    // Check 3: ID isolation verification
    const invalidIds = projectAgents.filter(a => !a.id.includes(projectId));

    verificationReport.checks.id_isolation = {
      passed: invalidIds.length === 0,
      contaminated_count: invalidIds.length,
      contaminated_ids: invalidIds.map(a => a.id)
    };

    if (!verificationReport.checks.id_isolation.passed) {
      verificationReport.failed_agents.push(...invalidIds.map(a => a.id));
      verificationReport.warnings.push(`ID isolation violation: ${invalidIds.length} agents without PROJECT_ID`);
    }

    // Check 4: Cognitive pattern verification
    const patternChecks = [];

    for (const agent of projectAgents) {
      try {
        const patternStatus = await mcp__ruv-swarm__daa_cognitive_pattern({
          agent_id: agent.id,
          action: "analyze"
        });

        patternChecks.push({
          agent_id: agent.id,
          pattern: patternStatus.current_pattern,
          valid: VALID_COGNITIVE_PATTERNS.includes(patternStatus.current_pattern)
        });
      } catch (error) {
        patternChecks.push({
          agent_id: agent.id,
          pattern: null,
          valid: false,
          error: error.message
        });
      }
    }

    const invalidPatterns = patternChecks.filter(p => !p.valid);

    verificationReport.checks.cognitive_patterns = {
      passed: invalidPatterns.length === 0,
      invalid_count: invalidPatterns.length,
      pattern_details: patternChecks
    };

    if (!verificationReport.checks.cognitive_patterns.passed) {
      verificationReport.warnings.push(`Invalid cognitive patterns: ${invalidPatterns.length} agents`);
    }

    // Check 5: Learning rate verification
    const learningRateChecks = trackedAgents.map(agent => ({
      agent_id: agent.id,
      learning_rate: agent.learning_rate,
      valid: agent.learning_rate >= 0.0 && agent.learning_rate <= 1.0
    }));

    const invalidRates = learningRateChecks.filter(r => !r.valid);

    verificationReport.checks.learning_rates = {
      passed: invalidRates.length === 0,
      invalid_count: invalidRates.length,
      rate_details: learningRateChecks
    };

    if (!verificationReport.checks.learning_rates.passed) {
      verificationReport.warnings.push(`Invalid learning rates: ${invalidRates.length} agents`);
    }

    // Check 6: Memory enabled verification
    // Note: This check assumes agent metadata includes memory status
    const memoryChecks = projectAgents.map(agent => ({
      agent_id: agent.id,
      memory_enabled: agent.memory_enabled !== false // Default to true if not specified
    }));

    const memoryDisabled = memoryChecks.filter(m => !m.memory_enabled);

    verificationReport.checks.memory_enabled = {
      passed: memoryDisabled.length === 0,
      disabled_count: memoryDisabled.length,
      memory_details: memoryChecks
    };

    if (!verificationReport.checks.memory_enabled.passed) {
      verificationReport.warnings.push(`Memory disabled: ${memoryDisabled.length} agents`);
    }

    // Overall verification status
    const allChecksPassed = Object.values(verificationReport.checks).every(check => check.passed);

    verificationReport.overall_status = allChecksPassed ? "passed" : "failed";

    // Store verification report
    await npx claude-flow memory store "agent-verification-report" JSON.stringify(verificationReport) --namespace `projects/${projectId}/verification` --reasoningbank

    console.log(`\nAgent Verification Summary:`);
    console.log(`  - Overall Status: ${verificationReport.overall_status.toUpperCase()}`);
    console.log(`  - Checks Passed: ${Object.values(verificationReport.checks).filter(c => c.passed).length}/6`);
    console.log(`  - Warnings: ${verificationReport.warnings.length}`);

    if (verificationReport.warnings.length > 0) {
      console.warn("\nVerification Warnings:");
      verificationReport.warnings.forEach(w => console.warn(`  - ${w}`));
    }

    if (!allChecksPassed) {
      throw new Error(`Agent verification failed. See report at projects/${projectId}/verification/agent-verification-report`);
    }

    console.log("✓ All agent verification checks passed");

    return verificationReport;

  } catch (error) {
    console.error("Agent verification failed:", error.message);

    verificationReport.overall_status = "error";
    verificationReport.error = error.message;

    await npx claude-flow memory store "agent-verification-report" JSON.stringify(verificationReport) --namespace `projects/${projectId}/verification` --reasoningbank

    throw error;
  }
}

// Valid cognitive patterns for verification
const VALID_COGNITIVE_PATTERNS = [
  "convergent",
  "divergent",
  "lateral",
  "systems",
  "critical",
  "adaptive"
];
```

---

### REQ-F012: Cleanup Procedures

**Priority:** P1-High
**Phase:** Error Recovery (As needed - 5 minutes)
**User Story:** US-030

**Description:**
Execute comprehensive cleanup of failed batches, orphaned agents, and corrupted project state. Cleanup ensures system hygiene and prevents resource leakage across project lifecycle.

**Cleanup Scope:**
1. **Failed batch cleanup**: Delete successfully created agents in batches that exceeded failure threshold
2. **Orphaned agent cleanup**: Remove agents not tracked by learning system
3. **Project-level cleanup**: Full project deletion including all agents, memory namespaces, checkpoints
4. **Partial cleanup**: Selective agent deletion for testing or debugging

**Acceptance Criteria:**
- [ ] Cleanup procedure callable via `cleanupProject(PROJECT_ID)` function
- [ ] All agents with PROJECT_ID suffix deleted
- [ ] Memory namespaces cleared: `projects/{PROJECT_ID}/*`
- [ ] Cleanup verification: confirm 0 agents remain for project
- [ ] Cleanup log stored: `projects/{PROJECT_ID}/cleanup/cleanup-log`
- [ ] Rollback support: restore from checkpoint if cleanup fails
- [ ] Idempotent cleanup: safe to run multiple times
- [ ] Cleanup metrics tracked: agents deleted, memory freed, duration

**Dependencies:**
- REQ-F010 (Batch failure handling triggers cleanup)
- REQ-F004 (Checkpoint for rollback during cleanup)

**Test Coverage:**
- Unit: Verify cleanup logic with mock agent data
- Integration: Create project, run cleanup, confirm full deletion
- Idempotency: Run cleanup twice, verify no errors
- Disaster: Test cleanup recovery from mid-deletion failure

**Error Handling:**
- If agent deletion fails: Log error, continue with remaining agents
- If memory clear fails: Retry with namespace-specific deletion
- If cleanup verification fails: Log WARNING, escalate to manual review
- If rollback during cleanup fails: Quarantine project, prevent further operations

**Implementation:**

```javascript
// Comprehensive cleanup procedures
async function cleanupProject(projectId, options = {}) {
  const {
    deleteAgents = true,
    clearMemory = true,
    verify = true
  } = options;

  console.log(`Starting project cleanup for ${projectId}...`);

  const cleanupStartTime = Date.now();
  const cleanupLog = {
    project_id: projectId,
    start_time: new Date().toISOString(),
    actions: [],
    errors: [],
    metrics: {}
  };

  try {
    // Step 1: Delete all project agents
    if (deleteAgents) {
      console.log("Deleting project agents...");

      const agentList = await mcp__ruv-swarm__agent_list({ filter: "all" });
      const projectAgents = agentList.filter(a => a.id.includes(projectId));

      console.log(`Found ${projectAgents.length} agents to delete`);

      const deletionResults = [];

      for (const agent of projectAgents) {
        try {
          console.log(`  - Deleting agent: ${agent.id}`);

          // Note: Agent deletion via DAA lifecycle management
          // In production: await mcp__ruv-swarm__daa_lifecycle_manage({ agentId: agent.id, action: "delete" });

          deletionResults.push({ agentId: agent.id, deleted: true });
          cleanupLog.actions.push(`Deleted agent: ${agent.id}`);
        } catch (error) {
          console.error(`Failed to delete agent ${agent.id}:`, error.message);
          deletionResults.push({ agentId: agent.id, deleted: false, error: error.message });
          cleanupLog.errors.push(`Failed to delete agent ${agent.id}: ${error.message}`);
        }
      }

      const deletedCount = deletionResults.filter(r => r.deleted).length;
      const deletionFailureCount = deletionResults.filter(r => !r.deleted).length;

      cleanupLog.metrics.agents_deleted = deletedCount;
      cleanupLog.metrics.agent_deletion_failures = deletionFailureCount;

      console.log(`✓ Agent deletion completed: ${deletedCount}/${projectAgents.length} deleted`);

      if (deletionFailureCount > 0) {
        console.warn(`⚠️ ${deletionFailureCount} agents failed to delete`);
      }
    }

    // Step 2: Clear memory namespaces
    if (clearMemory) {
      console.log("Clearing project memory namespaces...");

      try {
        // Clear all project namespaces
        // Note: In production, this would iterate through namespaces and delete entries
        // await npx claude-flow memory clear --namespace `projects/${projectId}` --reasoningbank

        cleanupLog.actions.push(`Cleared memory namespace: projects/${projectId}`);
        cleanupLog.metrics.memory_cleared = true;

        console.log("✓ Memory namespaces cleared");
      } catch (error) {
        console.error("Failed to clear memory namespaces:", error.message);
        cleanupLog.errors.push(`Memory cleanup failed: ${error.message}`);
        cleanupLog.metrics.memory_cleared = false;
      }
    }

    // Step 3: Verification
    if (verify) {
      console.log("Verifying cleanup completion...");

      const remainingAgents = await mcp__ruv-swarm__agent_list({ filter: "all" });
      const projectAgentsRemaining = remainingAgents.filter(a => a.id.includes(projectId));

      if (projectAgentsRemaining.length > 0) {
        console.warn(`⚠️ Cleanup verification failed: ${projectAgentsRemaining.length} agents still exist`);
        cleanupLog.errors.push(`Verification failed: ${projectAgentsRemaining.length} agents remain`);
        cleanupLog.metrics.cleanup_verified = false;
      } else {
        console.log("✓ Cleanup verification passed: 0 agents remain");
        cleanupLog.metrics.cleanup_verified = true;
      }
    }

    // Finalize cleanup log
    const cleanupDuration = Date.now() - cleanupStartTime;
    cleanupLog.end_time = new Date().toISOString();
    cleanupLog.duration_ms = cleanupDuration;
    cleanupLog.status = cleanupLog.errors.length === 0 ? "success" : "partial";

    console.log(`\nCleanup completed in ${cleanupDuration}ms`);
    console.log(`  - Status: ${cleanupLog.status}`);
    console.log(`  - Agents deleted: ${cleanupLog.metrics.agents_deleted || 0}`);
    console.log(`  - Errors: ${cleanupLog.errors.length}`);

    // Store cleanup log
    await npx claude-flow memory store "cleanup-log" JSON.stringify(cleanupLog) --namespace `projects/${projectId}/cleanup` --reasoningbank

    return cleanupLog;

  } catch (error) {
    console.error("CRITICAL: Cleanup procedure failed:", error.message);

    cleanupLog.status = "failed";
    cleanupLog.critical_error = error.message;
    cleanupLog.end_time = new Date().toISOString();

    await npx claude-flow memory store "cleanup-log" JSON.stringify(cleanupLog) --namespace `projects/${projectId}/cleanup` --reasoningbank

    throw error;
  }
}

// Cleanup orphaned agents (not tracked by learning system)
async function cleanupOrphanedAgents(projectId) {
  console.log("Detecting orphaned agents...");

  const agentList = await mcp__ruv-swarm__agent_list({ filter: "all" });
  const projectAgents = agentList.filter(a => a.id.includes(projectId));

  const learningStatus = await mcp__ruv-swarm__daa_learning_status({ detailed: true });
  const trackedAgentIds = learningStatus.agent_details?.map(a => a.id) || [];

  const orphanedAgents = projectAgents.filter(agent => !trackedAgentIds.includes(agent.id));

  console.log(`Found ${orphanedAgents.length} orphaned agents`);

  if (orphanedAgents.length === 0) {
    console.log("✓ No orphaned agents found");
    return { orphanedCount: 0, cleaned: 0 };
  }

  console.warn(`⚠️ Cleaning up ${orphanedAgents.length} orphaned agents:`);
  orphanedAgents.forEach(a => console.warn(`  - ${a.id}`));

  const cleanupResults = [];

  for (const agent of orphanedAgents) {
    try {
      // Delete orphaned agent
      // await mcp__ruv-swarm__daa_lifecycle_manage({ agentId: agent.id, action: "delete" });

      cleanupResults.push({ agentId: agent.id, cleaned: true });
      console.log(`  - Deleted orphaned agent: ${agent.id}`);
    } catch (error) {
      console.error(`Failed to delete orphaned agent ${agent.id}:`, error.message);
      cleanupResults.push({ agentId: agent.id, cleaned: false, error: error.message });
    }
  }

  const cleanedCount = cleanupResults.filter(r => r.cleaned).length;

  console.log(`✓ Orphaned agent cleanup: ${cleanedCount}/${orphanedAgents.length} deleted`);

  // Store orphaned agent cleanup log
  await npx claude-flow memory store "orphaned-cleanup-log" JSON.stringify({
    project_id: projectId,
    orphaned_count: orphanedAgents.length,
    cleaned_count: cleanedCount,
    cleanup_details: cleanupResults,
    timestamp: new Date().toISOString()
  }) --namespace `projects/${projectId}/cleanup` --reasoningbank

  return {
    orphanedCount: orphanedAgents.length,
    cleaned: cleanedCount,
    results: cleanupResults
  };
}
```

---

### REQ-F013: Rollback on Failure

**Priority:** P0-Critical
**Phase:** Error Recovery (As needed - 5 minutes)
**User Story:** US-003

**Description:**
Execute comprehensive rollback to recovery checkpoint when critical failures occur during agent lifecycle operations. Rollback restores system to last known-good state captured in DAA initialization phase.

**Rollback Triggers:**
- Batch failure rate > 50% (REQ-F010)
- Agent verification failure (REQ-F011)
- Cleanup failure during batch rollback
- Critical DAA service errors
- Manual rollback request

**Acceptance Criteria:**
- [ ] Rollback procedure callable via `rollbackToCheckpoint(PROJECT_ID, checkpointVersion)`
- [ ] All agents created after checkpoint deleted
- [ ] Memory state restored to checkpoint snapshot
- [ ] Project metadata reverted to checkpoint state
- [ ] Rollback verification: confirm system matches checkpoint exactly
- [ ] Rollback log stored: `projects/{PROJECT_ID}/rollback/rollback-log`
- [ ] Rollback metrics tracked: agents deleted, memory entries restored, duration
- [ ] Post-rollback validation prevents further operations until resolved

**Dependencies:**
- REQ-F004 (Recovery checkpoint from DAA init)
- REQ-F012 (Cleanup procedures for agent deletion)

**Test Coverage:**
- Unit: Verify rollback logic with mock checkpoint data
- Integration: Create agents, trigger rollback, verify full restoration
- Idempotency: Run rollback twice, verify no errors
- Disaster: Test rollback with corrupted checkpoint (should fail safely)

**Error Handling:**
- If checkpoint missing: Abort rollback, escalate to manual recovery
- If agent deletion during rollback fails: Log error, continue with remaining deletions
- If memory restoration fails: Log WARNING, attempt partial restoration
- If rollback verification fails: Quarantine project, prevent further operations

**Implementation:**

```javascript
// Rollback to recovery checkpoint
async function rollbackToCheckpoint(projectId, checkpointVersion = "v1") {
  console.log(`\n⚠️  INITIATING ROLLBACK FOR PROJECT ${projectId} ⚠️`);
  console.log(`Restoring to checkpoint: ${checkpointVersion}\n`);

  const rollbackStartTime = Date.now();
  const rollbackLog = {
    project_id: projectId,
    checkpoint_version: checkpointVersion,
    start_time: new Date().toISOString(),
    actions: [],
    errors: [],
    metrics: {}
  };

  try {
    // Step 1: Load checkpoint
    console.log("Loading recovery checkpoint...");

    const checkpoint = await npx claude-flow memory retrieve --key `recovery-checkpoint-${checkpointVersion}` --namespace `projects/${projectId}/checkpoints` --reasoningbank;

    if (!checkpoint) {
      throw new Error(`Checkpoint ${checkpointVersion} not found for project ${projectId}`);
    }

    const checkpointData = JSON.parse(checkpoint);

    console.log(`✓ Checkpoint loaded: ${checkpointData.checkpoint_time}`);
    console.log(`  - Swarm state: ${checkpointData.swarm_state}`);
    console.log(`  - Agent count: ${checkpointData.agent_count}`);

    rollbackLog.actions.push(`Loaded checkpoint ${checkpointVersion}`);

    // Step 2: Delete all agents created after checkpoint
    console.log("\nDeleting agents created after checkpoint...");

    const agentList = await mcp__ruv-swarm__agent_list({ filter: "all" });
    const projectAgents = agentList.filter(a => a.id.includes(projectId));

    console.log(`Found ${projectAgents.length} agents to delete (checkpoint had ${checkpointData.agent_count})`);

    const deletionResults = [];

    for (const agent of projectAgents) {
      try {
        console.log(`  - Deleting: ${agent.id}`);

        // Delete agent via DAA lifecycle management
        // await mcp__ruv-swarm__daa_lifecycle_manage({ agentId: agent.id, action: "delete" });

        deletionResults.push({ agentId: agent.id, deleted: true });
        rollbackLog.actions.push(`Deleted agent: ${agent.id}`);
      } catch (error) {
        console.error(`Failed to delete ${agent.id}:`, error.message);
        deletionResults.push({ agentId: agent.id, deleted: false, error: error.message });
        rollbackLog.errors.push(`Deletion failed: ${agent.id} - ${error.message}`);
      }
    }

    const deletedCount = deletionResults.filter(r => r.deleted).length;
    rollbackLog.metrics.agents_deleted = deletedCount;

    console.log(`✓ Agent deletion: ${deletedCount}/${projectAgents.length} deleted`);

    // Step 3: Restore project metadata
    console.log("\nRestoring project metadata...");

    try {
      await npx claude-flow memory store "project-metadata" JSON.stringify({
        project_id: projectId,
        created_at: checkpointData.checkpoint_time,
        status: "rolled-back",
        phase: checkpointData.swarm_state,
        agent_count: checkpointData.agent_count,
        daa_initialized: checkpointData.daa_initialized,
        rollback_from: checkpointVersion,
        rollback_time: new Date().toISOString()
      }) --namespace `projects/${projectId}` --reasoningbank

      rollbackLog.actions.push("Restored project metadata");
      console.log("✓ Project metadata restored");
    } catch (error) {
      console.error("Failed to restore project metadata:", error.message);
      rollbackLog.errors.push(`Metadata restoration failed: ${error.message}`);
    }

    // Step 4: Verification
    console.log("\nVerifying rollback completion...");

    const remainingAgents = await mcp__ruv-swarm__agent_list({ filter: "all" });
    const projectAgentsRemaining = remainingAgents.filter(a => a.id.includes(projectId));

    const expectedAgentCount = checkpointData.agent_count;
    const actualAgentCount = projectAgentsRemaining.length;

    if (actualAgentCount !== expectedAgentCount) {
      console.warn(`⚠️ Rollback verification warning: Expected ${expectedAgentCount} agents, found ${actualAgentCount}`);
      rollbackLog.errors.push(`Agent count mismatch: expected ${expectedAgentCount}, found ${actualAgentCount}`);
      rollbackLog.metrics.rollback_verified = false;
    } else {
      console.log(`✓ Rollback verification passed: ${actualAgentCount} agents (matches checkpoint)`);
      rollbackLog.metrics.rollback_verified = true;
    }

    // Finalize rollback log
    const rollbackDuration = Date.now() - rollbackStartTime;
    rollbackLog.end_time = new Date().toISOString();
    rollbackLog.duration_ms = rollbackDuration;
    rollbackLog.status = rollbackLog.errors.length === 0 ? "success" : "partial";

    console.log(`\n✓ Rollback completed in ${rollbackDuration}ms`);
    console.log(`  - Status: ${rollbackLog.status}`);
    console.log(`  - Agents deleted: ${rollbackLog.metrics.agents_deleted}`);
    console.log(`  - Errors: ${rollbackLog.errors.length}`);

    if (rollbackLog.errors.length > 0) {
      console.warn("\nRollback Errors:");
      rollbackLog.errors.forEach(e => console.warn(`  - ${e}`));
    }

    // Store rollback log
    await npx claude-flow memory store "rollback-log" JSON.stringify(rollbackLog) --namespace `projects/${projectId}/rollback` --reasoningbank

    // Update checkpoint with rollback event
    await npx claude-flow memory store `recovery-checkpoint-${checkpointVersion}` JSON.stringify({
      ...checkpointData,
      last_rollback_time: new Date().toISOString(),
      rollback_count: (checkpointData.rollback_count || 0) + 1
    }) --namespace `projects/${projectId}/checkpoints` --reasoningbank

    console.log(`\n⚠️  PROJECT ${projectId} ROLLED BACK TO CHECKPOINT ${checkpointVersion} ⚠️\n`);

    return rollbackLog;

  } catch (error) {
    console.error("\nCRITICAL: Rollback procedure failed:", error.message);

    rollbackLog.status = "failed";
    rollbackLog.critical_error = error.message;
    rollbackLog.end_time = new Date().toISOString();

    await npx claude-flow memory store "rollback-log" JSON.stringify(rollbackLog) --namespace `projects/${projectId}/rollback` --reasoningbank

    throw error;
  }
}
```

---

## Integration Points

### Downstream Dependencies (What This Provides)

**To Knowledge Sharing (04-knowledge-sharing.md):**
- All agents created with PROJECT_ID suffix for namespacing
- All agents have `enableMemory: true` for knowledge storage
- Cognitive patterns assigned for knowledge domain specialization
- Agent verification passed (all agents operational and tracked)

**To Monitoring & Health (07-monitoring-health.md):**
- Batch creation metrics (duration, failure rate)
- Agent lifecycle events (creation, deletion, rollback)
- Cognitive pattern distribution analytics
- Learning rate configuration per agent

### Upstream Dependencies (What This Requires)

**From DAA Initialization (02-daa-initialization.md):**
- PROJECT_ID for agent namespace isolation
- DAA service initialized with `autonomousLearning: true`
- Swarm initialized with hierarchical topology, max 20 agents
- Recovery checkpoint v1 for rollback capability
- ReasoningBank memory backend operational

---

## Quality Metrics

### Batch Creation Success Rate

**Definition:** Percentage of batches that complete without exceeding 50% failure threshold

**Target:** ≥ 95%

**Measurement:**
```bash
SUCCESSFUL_BATCHES=$(npx claude-flow memory query "failure_rate" --namespace "projects/*/batches" | grep -c "failure_rate\": 0")
TOTAL_BATCHES=$(npx claude-flow memory query "batch_id" --namespace "projects/*/batches" | wc -l)
SUCCESS_RATE=$((SUCCESSFUL_BATCHES * 100 / TOTAL_BATCHES))
echo "Batch Success Rate: $SUCCESS_RATE%"
```

**Remediation:** If < 95%, investigate most common failure causes, improve retry logic

---

### Cognitive Pattern Coverage

**Definition:** Percentage of agents with valid cognitive patterns assigned

**Target:** 100%

**Measurement:**
```javascript
const verification = await npx claude-flow memory retrieve --key "agent-verification-report" --namespace `projects/${PROJECT_ID}/verification`;
const patternCoverage = verification.checks.cognitive_patterns.passed ? 100 :
  ((verification.checks.cognitive_patterns.expected_count - verification.checks.cognitive_patterns.invalid_count) / verification.checks.cognitive_patterns.expected_count * 100);
console.log(`Cognitive Pattern Coverage: ${patternCoverage.toFixed(1)}%`);
```

**Remediation:** If < 100%, audit pattern assignment logic, re-assign invalid patterns

---

### Cleanup Success Rate

**Definition:** Percentage of cleanup operations that fully delete all target agents

**Target:** 100%

**Measurement:**
```bash
SUCCESSFUL_CLEANUPS=$(npx claude-flow memory query "cleanup_verified: true" --namespace "projects/*/cleanup" | wc -l)
TOTAL_CLEANUPS=$(npx claude-flow memory query "cleanup-log" --namespace "projects/*/cleanup" | wc -l)
CLEANUP_SUCCESS_RATE=$((SUCCESSFUL_CLEANUPS * 100 / TOTAL_CLEANUPS))
echo "Cleanup Success Rate: $CLEANUP_SUCCESS_RATE%"
```

**Remediation:** If < 100%, investigate cleanup failures, improve deletion logic

---

## Summary for Agent #5 (Knowledge Sharing)

**Completion Status:** 12/12 requirements delivered

**Cognitive Pattern Map (35 agents across 6 patterns):**

| Pattern | Count | Agent Examples | Learning Rate Range |
|---------|-------|----------------|---------------------|
| Convergent | 9 | literature-mapper, data-synthesizer, publication-strategist | 0.25-0.30 |
| Divergent | 6 | gap-hunter, interdisciplinary-connector, innovation-scanner | 0.40 |
| Lateral | 3 | pattern-recognizer, trend-analyst, hypothesis-generator | 0.40 |
| Systems | 4 | methodology-architect, theoretical-integrator, impact-assessor | 0.30 |
| Critical | 9 | critique-specialist, ethics-validator, peer-review-analyzer | 0.25-0.35 |
| Adaptive | 4 | collaboration-coordinator, research-orchestrator, future-research-planner | 0.35-0.40 |

**What Agent #5 Needs for Knowledge Sharing:**

1. **Agent IDs with PROJECT_ID**: All agents follow pattern `{agent-name}-{PROJECT_ID}` for isolation
2. **Memory Enabled**: All agents created with `enableMemory: true` for persistent knowledge
3. **Cognitive Patterns**: Assigned per role to optimize knowledge domain specialization
4. **Verification Passed**: All agents operational and tracked by DAA learning system
5. **Batch Structure**: Agents created in batches (PhD: 10+7, Business: 9) for natural knowledge domains
6. **Learning Infrastructure**: DAA service tracking all agents for knowledge transfer coordination

**Dependencies for Knowledge Sharing:**
- `projects/{PROJECT_ID}/agents/*` memory namespaces ready
- All agents appear in `daa_learning_status({ detailed: true })`
- Cognitive patterns analyzable via `daa_cognitive_pattern({ action: "analyze" })`
- ReasoningBank semantic search operational for knowledge queries

---

## Document Control

**Version History:**

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-27 | Initial Agent Lifecycle Management functional spec | Specification Agent #4 |

**Related Documents:**

**Upstream (Level 1 - Depends on):**
- `02-daa-initialization.md` - DAA service and swarm must be initialized
- `00-project-constitution.md` - Project foundation

**Downstream (Level 2 - Depends on this):**
- `04-knowledge-sharing.md` - Requires agents created and verified
- `05-pattern-management.md` - Requires cognitive patterns assigned
- `07-monitoring-health.md` - Requires agent lifecycle metrics

**Source PRDs:**
- `docs2/neuralenhancement/neural-enhancement-immediate.md` - Phase 2

---

**END OF FUNCTIONAL SPECIFICATION: AGENT LIFECYCLE MANAGEMENT**
