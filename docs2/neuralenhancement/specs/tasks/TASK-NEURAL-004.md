# TASK-NEURAL-004: Cognitive Pattern Assignment & Verification

## Metadata

| Field | Value |
|-------|-------|
| **Task ID** | TASK-NEURAL-004 |
| **Title** | Cognitive Pattern Assignment & Verification |
| **Status** | Pending |
| **Priority** | High |
| **Complexity** | LOW |
| **Estimated Time** | 15 minutes |
| **Implements** | REQ-NEURAL-09, REQ-NEURAL-10, REQ-NEURAL-11 |
| **Depends On** | TASK-NEURAL-003 (Agent Creation) |
| **Blocks** | TASK-NEURAL-005 (Error Recovery), TASK-NEURAL-007 (Testing), TASK-NEURAL-008 (Integration) |

## Context

After all 35 agents are created in TASK-003, this task verifies that each agent has been assigned the correct cognitive pattern based on its role. The cognitive patterns determine how agents think and process information, directly impacting their effectiveness in specialized tasks.

**Purpose**: Ensure all agents have appropriate cognitive patterns and are functioning effectively before proceeding to error recovery testing and baseline metric collection.

**Key Goals**:
- Verify all 35 agents exist and are active
- Confirm correct cognitive pattern assignment for each agent
- Validate pattern effectiveness scores (target: >0.7)
- Store verification results in memory for monitoring
- Identify and reassign any incorrect patterns

## Pseudo-code

```javascript
// Configuration: Expected cognitive patterns by agent type
const PROJECT_ID = "neural-enhancement-20250127";
const expectedPatterns = {
  // Researcher Agents (4 total)
  [`literature-mapper-${PROJECT_ID}`]: "divergent",      // Creative research
  [`gap-hunter-${PROJECT_ID}`]: "critical",              // Analytical gap finding
  [`methodology-validator-${PROJECT_ID}`]: "systems",    // Holistic validation
  [`trend-scout-${PROJECT_ID}`]: "adaptive",             // Versatile trend tracking

  // Coder Agents (4 total)
  [`core-architect-${PROJECT_ID}`]: "systems",           // System design
  [`feature-smith-${PROJECT_ID}`]: "convergent",         // Focused implementation
  [`refactor-wizard-${PROJECT_ID}`]: "critical",         // Code analysis
  [`integration-master-${PROJECT_ID}`]: "adaptive",      // Flexible integration

  // Tester Agents (3 total)
  [`unit-guardian-${PROJECT_ID}`]: "convergent",         // Focused unit testing
  [`integration-sentinel-${PROJECT_ID}`]: "systems",     // System integration
  [`e2e-validator-${PROJECT_ID}`]: "critical",           // End-to-end analysis

  // Optimizer Agents (3 total)
  [`performance-tuner-${PROJECT_ID}`]: "convergent",     // Performance focus
  [`memory-warden-${PROJECT_ID}`]: "critical",           // Memory analysis
  [`bottleneck-hunter-${PROJECT_ID}`]: "critical",       // Bottleneck detection

  // Analyst Agents (4 total)
  [`code-cartographer-${PROJECT_ID}`]: "divergent",      // Creative mapping
  [`pattern-detective-${PROJECT_ID}`]: "lateral",        // Cross-domain patterns
  [`quality-oracle-${PROJECT_ID}`]: "critical",          // Quality analysis
  [`metric-sage-${PROJECT_ID}`]: "adaptive",             // Metric interpretation

  // Coordinator Agents (17 total - all adaptive)
  [`orchestrator-prime-${PROJECT_ID}`]: "adaptive",
  [`task-nexus-${PROJECT_ID}`]: "adaptive",
  [`resource-balancer-${PROJECT_ID}`]: "adaptive",
  [`conflict-mediator-${PROJECT_ID}`]: "adaptive",
  [`priority-arbiter-${PROJECT_ID}`]: "adaptive",
  [`progress-sentinel-${PROJECT_ID}`]: "adaptive",
  [`sync-harmonizer-${PROJECT_ID}`]: "adaptive",
  [`dependency-navigator-${PROJECT_ID}`]: "adaptive",
  [`bottleneck-resolver-${PROJECT_ID}`]: "adaptive",
  [`quality-gatekeeper-${PROJECT_ID}`]: "adaptive",
  [`communication-bridge-${PROJECT_ID}`]: "adaptive",
  [`knowledge-curator-${PROJECT_ID}`]: "adaptive",
  [`risk-assessor-${PROJECT_ID}`]: "adaptive",
  [`compliance-guardian-${PROJECT_ID}`]: "adaptive",
  [`innovation-catalyst-${PROJECT_ID}`]: "adaptive",
  [`feedback-synthesizer-${PROJECT_ID}`]: "adaptive",
  [`handoff-coordinator-${PROJECT_ID}`]: "adaptive"
};

// Pattern distribution
const patternDistribution = {
  convergent: 4,   // Focused, goal-oriented
  divergent: 4,    // Creative, exploratory
  lateral: 1,      // Cross-domain thinking
  systems: 3,      // Holistic, architectural
  critical: 6,     // Analytical, evaluative
  adaptive: 17     // Versatile, flexible
};

async function verifyAndAssignCognitivePatterns() {
  console.log("Starting cognitive pattern verification...");

  // Step 1: Retrieve all active agents
  const agentListResponse = await mcp__ruv_swarm__agent_list({
    filter: "all"
  });

  if (!agentListResponse.success || !agentListResponse.agents) {
    throw new Error("Failed to retrieve agent list");
  }

  const agents = agentListResponse.agents;
  console.log(`Found ${agents.length} agents`);

  // Step 2: Verify all 35 agents exist
  if (agents.length !== 35) {
    throw new Error(`Expected 35 agents, found ${agents.length}`);
  }

  // Step 3: Verify and reassign patterns
  const verificationResults = {
    verified: [],
    reassigned: [],
    lowEffectiveness: [],
    errors: []
  };

  for (const [agentId, expectedPattern] of Object.entries(expectedPatterns)) {
    try {
      // Find agent in list
      const agent = agents.find(a => a.id === agentId);
      if (!agent) {
        verificationResults.errors.push({
          agentId,
          error: "Agent not found in active list"
        });
        continue;
      }

      // Analyze current cognitive pattern
      const analysis = await mcp__ruv_swarm__daa_cognitive_pattern({
        agent_id: agentId,
        action: "analyze"
      });

      if (!analysis.success) {
        verificationResults.errors.push({
          agentId,
          error: "Pattern analysis failed",
          details: analysis.error
        });
        continue;
      }

      // Check if pattern matches expected
      if (analysis.pattern !== expectedPattern) {
        console.log(`Reassigning ${agentId}: ${analysis.pattern} → ${expectedPattern}`);

        // Reassign to correct pattern
        const reassignResult = await mcp__ruv_swarm__daa_cognitive_pattern({
          agent_id: agentId,
          action: "change",
          pattern: expectedPattern
        });

        if (reassignResult.success) {
          verificationResults.reassigned.push({
            agentId,
            oldPattern: analysis.pattern,
            newPattern: expectedPattern
          });
        } else {
          verificationResults.errors.push({
            agentId,
            error: "Pattern reassignment failed",
            details: reassignResult.error
          });
        }
      } else {
        // Pattern is correct
        verificationResults.verified.push({
          agentId,
          pattern: expectedPattern,
          effectiveness: analysis.pattern_effectiveness || 0
        });
      }

      // Check effectiveness score
      const effectiveness = analysis.pattern_effectiveness || 0;
      if (effectiveness < 0.7) {
        verificationResults.lowEffectiveness.push({
          agentId,
          pattern: expectedPattern,
          effectiveness,
          warning: "Pattern effectiveness below threshold (0.7)"
        });
      }

    } catch (error) {
      verificationResults.errors.push({
        agentId,
        error: error.message,
        stack: error.stack
      });
    }
  }

  // Step 4: Validate pattern distribution
  const actualDistribution = {};
  for (const pattern of Object.values(expectedPatterns)) {
    actualDistribution[pattern] = (actualDistribution[pattern] || 0) + 1;
  }

  const distributionMatch = JSON.stringify(actualDistribution) ===
                           JSON.stringify(patternDistribution);

  if (!distributionMatch) {
    console.warn("Pattern distribution mismatch detected");
    console.log("Expected:", patternDistribution);
    console.log("Actual:", actualDistribution);
  }

  // Step 5: Store results in memory
  await mcp__ruv_swarm__memory_usage({
    action: "store",
    key: `neural-enhancement/task-004/verification-results`,
    namespace: "coordination",
    value: JSON.stringify({
      timestamp: Date.now(),
      totalAgents: 35,
      verified: verificationResults.verified.length,
      reassigned: verificationResults.reassigned.length,
      lowEffectiveness: verificationResults.lowEffectiveness.length,
      errors: verificationResults.errors.length,
      patternDistribution: actualDistribution,
      details: verificationResults
    })
  });

  // Step 6: Generate summary report
  const summary = {
    success: verificationResults.errors.length === 0,
    totalAgents: 35,
    verified: verificationResults.verified.length,
    reassigned: verificationResults.reassigned.length,
    lowEffectiveness: verificationResults.lowEffectiveness.length,
    errors: verificationResults.errors.length,
    averageEffectiveness: calculateAverageEffectiveness(verificationResults.verified),
    distributionMatch
  };

  console.log("Verification Summary:", summary);

  return {
    success: summary.success,
    summary,
    details: verificationResults
  };
}

function calculateAverageEffectiveness(verifiedAgents) {
  if (verifiedAgents.length === 0) return 0;
  const total = verifiedAgents.reduce((sum, a) => sum + a.effectiveness, 0);
  return (total / verifiedAgents.length).toFixed(3);
}
```

## Cognitive Patterns

### Pattern Definitions

| Pattern | Description | Agent Count | Use Cases |
|---------|-------------|-------------|-----------|
| **Convergent** | Focused, goal-oriented thinking | 4 | Feature implementation, unit testing, performance tuning |
| **Divergent** | Creative, exploratory thinking | 4 | Research, code mapping, brainstorming |
| **Lateral** | Cross-domain, analogical thinking | 1 | Pattern detection across domains |
| **Systems** | Holistic, architectural thinking | 3 | System design, validation, integration |
| **Critical** | Analytical, evaluative thinking | 6 | Gap finding, code analysis, quality assessment |
| **Adaptive** | Versatile, flexible thinking | 17 | Coordination, resource management, communication |

### Pattern Assignment by Role

**Researcher Agents** (4):
- `literature-mapper`: Divergent (creative research exploration)
- `gap-hunter`: Critical (analytical gap identification)
- `methodology-validator`: Systems (holistic validation)
- `trend-scout`: Adaptive (flexible trend tracking)

**Coder Agents** (4):
- `core-architect`: Systems (architectural design)
- `feature-smith`: Convergent (focused implementation)
- `refactor-wizard`: Critical (code analysis)
- `integration-master`: Adaptive (flexible integration)

**Tester Agents** (3):
- `unit-guardian`: Convergent (focused unit testing)
- `integration-sentinel`: Systems (system-level testing)
- `e2e-validator`: Critical (analytical validation)

**Optimizer Agents** (3):
- `performance-tuner`: Convergent (performance focus)
- `memory-warden`: Critical (memory analysis)
- `bottleneck-hunter`: Critical (bottleneck detection)

**Analyst Agents** (4):
- `code-cartographer`: Divergent (creative mapping)
- `pattern-detective`: Lateral (cross-domain patterns)
- `quality-oracle`: Critical (quality analysis)
- `metric-sage`: Adaptive (metric interpretation)

**Coordinator Agents** (17):
- All 17 coordinators: Adaptive (versatile coordination)

## Validation Criteria

### Success Criteria
- ✅ All 35 agents exist and are active
- ✅ Each agent has correct cognitive pattern assigned
- ✅ Pattern distribution matches expected: {convergent: 4, divergent: 4, lateral: 1, systems: 3, critical: 6, adaptive: 17}
- ✅ Average pattern effectiveness score ≥ 0.7
- ✅ Verification results stored in memory
- ✅ Zero reassignment failures

### Acceptance Thresholds
- **Pattern Match Rate**: 100% (all agents have correct patterns)
- **Effectiveness Score**: ≥0.7 (minimum for production use)
- **Error Rate**: 0% (no pattern assignment failures)
- **Reassignment Success**: 100% (if needed)

### Monitoring Points
- Agents with effectiveness <0.7 flagged for monitoring
- Pattern distribution verified against expected
- All errors logged with full context
- Results available for TASK-005 and TASK-007

## Forward Dependencies

**TASK-NEURAL-005 (Error Recovery)**:
- Requires all agents to have verified cognitive patterns
- Uses pattern-specific error handling strategies
- Tests pattern effectiveness under error conditions

**TASK-NEURAL-007 (Testing)**:
- Tests cognitive pattern effectiveness
- Validates pattern-based decision making
- Measures pattern impact on performance

**TASK-NEURAL-008 (Integration)**:
- Integrates pattern-aware coordination
- Implements pattern-based task routing
- Monitors pattern effectiveness in production

## Implementation Notes

1. **Pattern Analysis**: Use `daa_cognitive_pattern` with `action: "analyze"` to check current patterns
2. **Pattern Reassignment**: Use `daa_cognitive_pattern` with `action: "change"` if patterns don't match
3. **Effectiveness Monitoring**: Track effectiveness scores for each agent
4. **Memory Storage**: Store complete verification results for audit trail
5. **Error Handling**: Log all errors but continue verification for all agents

## References

- **Requirements**: REQ-NEURAL-09 (Cognitive Patterns), REQ-NEURAL-10 (Pattern Assignment), REQ-NEURAL-11 (Pattern Effectiveness)
- **Dependencies**: TASK-NEURAL-003 (Agent Creation)
- **Blocks**: TASK-NEURAL-005, TASK-NEURAL-007, TASK-NEURAL-008
- **MCP Tools**: `mcp__ruv_swarm__agent_list`, `mcp__ruv_swarm__daa_cognitive_pattern`, `mcp__ruv_swarm__memory_usage`
