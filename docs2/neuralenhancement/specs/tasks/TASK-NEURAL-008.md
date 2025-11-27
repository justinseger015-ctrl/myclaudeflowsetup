# TASK-NEURAL-008: Knowledge Sharing Infrastructure

## Metadata

- **Implements**: REQ-NEURAL-21 (Cross-Agent Knowledge), REQ-NEURAL-22 (Knowledge Topologies), REQ-NEURAL-23 (Domain Isolation), REQ-NEURAL-24 (Knowledge Expiry), REQ-NEURAL-25 (Sharing Hooks)
- **Depends On**: TASK-007 (Verification & Monitoring)
- **Complexity**: MEDIUM
- **Estimated Time**: 25 minutes
- **Phase**: SHORT-TERM (First task in 90-day implementation phase)
- **Priority**: HIGH

## Context

This is the **FIRST SHORT-TERM TASK** marking the transition from immediate stability (TASK-001 to TASK-007) to advanced features. Implements knowledge flow topologies and sharing hooks between agents, enabling:

1. **Knowledge Flows**: Directional information sharing between specialized agents
2. **Domain Isolation**: Separate knowledge domains for different research workflows
3. **Time-To-Live**: Automatic expiry of time-sensitive knowledge
4. **Retry Logic**: Robust failure handling with exponential backoff
5. **Audit Trail**: Comprehensive logging of all knowledge transfers

## Pseudo-code

### Core Knowledge Sharing with Retry

```javascript
// Knowledge sharing with retry and exponential backoff
async function shareKnowledgeWithRetry(config, maxRetries = 3) {
  const PROJECT_ID = process.env.PROJECT_ID || 'neural-enhancement';

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      // Execute knowledge share via MCP
      await mcp__ruv_swarm__daa_knowledge_share({
        sourceAgentId: `${config.source}-${PROJECT_ID}`,
        targetAgentIds: config.targets.map(t => `${t}-${PROJECT_ID}`),
        knowledgeDomain: config.domain,
        knowledgeContent: {
          ...config.content,
          project_id: PROJECT_ID,
          created_at: new Date().toISOString(),
          expires_at: new Date(Date.now() + config.ttl).toISOString(),
          version: '1.0.0',
          metadata: {
            source: config.source,
            targets: config.targets,
            attempt: attempt
          }
        }
      });

      // Log success
      await bash(`npx claude-flow memory store "knowledge-share-success-${Date.now()}" --value '${JSON.stringify({
        source: config.source,
        targets: config.targets,
        domain: config.domain,
        timestamp: new Date().toISOString(),
        attempt: attempt
      })}'`);

      console.log(`✓ Knowledge shared: ${config.source} → ${config.targets.join(', ')}`);
      return;

    } catch (error) {
      console.warn(`⚠ Knowledge share attempt ${attempt}/${maxRetries} failed:`, error.message);

      if (attempt === maxRetries) {
        // Log failure after all retries exhausted
        await bash(`npx claude-flow memory store "knowledge-share-failure-${Date.now()}" --value '${JSON.stringify({
          source: config.source,
          targets: config.targets,
          domain: config.domain,
          error: error.message,
          attempts: maxRetries,
          timestamp: new Date().toISOString()
        })}'`);

        throw new Error(`Knowledge sharing failed after ${maxRetries} attempts: ${error.message}`);
      }

      // Exponential backoff: 2s, 4s, 8s
      const delay = 1000 * Math.pow(2, attempt);
      await sleep(delay);
    }
  }
}

// Utility sleep function
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

### PhD Research Knowledge Flows

```javascript
// 1. Literature Corpus → Multiple Analysts
await shareKnowledgeWithRetry({
  source: "literature-mapper",
  targets: ["gap-hunter", "contradiction-analyzer", "thematic-synthesizer"],
  domain: "literature-corpus",
  content: {
    papers: [...],
    citations: {...},
    themes: [...]
  },
  ttl: 180 * 24 * 60 * 60 * 1000 // 180 days
});

// 2. Research Gaps → Theory Builder
await shareKnowledgeWithRetry({
  source: "gap-hunter",
  targets: ["theory-builder"],
  domain: "research-gaps",
  content: {
    identified_gaps: [...],
    novelty_score: 0.85,
    justification: "..."
  },
  ttl: 180 * 24 * 60 * 60 * 1000
});

// 3. Contradictions → Literature Mapper
await shareKnowledgeWithRetry({
  source: "contradiction-analyzer",
  targets: ["literature-mapper"],
  domain: "contradictions",
  content: {
    conflicts: [...],
    resolution_strategies: [...],
    citations: [...]
  },
  ttl: 180 * 24 * 60 * 60 * 1000
});

// 4. Theoretical Framework → Hypothesis Generator
await shareKnowledgeWithRetry({
  source: "theory-builder",
  targets: ["hypothesis-generator"],
  domain: "theoretical-framework",
  content: {
    framework: {...},
    constructs: [...],
    relationships: [...]
  },
  ttl: 180 * 24 * 60 * 60 * 1000
});

// 5. Hypotheses → Methods Designer
await shareKnowledgeWithRetry({
  source: "hypothesis-generator",
  targets: ["methods-designer"],
  domain: "hypotheses",
  content: {
    hypotheses: [...],
    variables: [...],
    expected_outcomes: [...]
  },
  ttl: 180 * 24 * 60 * 60 * 1000
});

// 6. Research Methods → Pilot Study Designer
await shareKnowledgeWithRetry({
  source: "methods-designer",
  targets: ["pilot-study-designer"],
  domain: "research-methods",
  content: {
    methodology: {...},
    instruments: [...],
    procedures: [...]
  },
  ttl: 180 * 24 * 60 * 60 * 1000
});

// 7. All Components → Dissertation Architect
await shareKnowledgeWithRetry({
  source: "pilot-study-designer",
  targets: ["dissertation-architect"],
  domain: "phd-integration",
  content: {
    pilot_results: {...},
    validated_methods: [...],
    timeline: {...}
  },
  ttl: 180 * 24 * 60 * 60 * 1000
});
```

### Business Research Knowledge Flows

```javascript
// 1. Company Analyzer → Leadership Profiler
await shareKnowledgeWithRetry({
  source: "company-analyzer",
  targets: ["leadership-profiler"],
  domain: "company-data",
  content: {
    company_profile: {...},
    financials: {...},
    market_position: {...}
  },
  ttl: 90 * 24 * 60 * 60 * 1000 // 90 days
});

// 2. Leadership → Positioning Mapper
await shareKnowledgeWithRetry({
  source: "leadership-profiler",
  targets: ["positioning-mapper"],
  domain: "leadership-insights",
  content: {
    leaders: [...],
    styles: [...],
    capabilities: [...]
  },
  ttl: 90 * 24 * 60 * 60 * 1000
});

// 3. Competitive Intelligence → Positioning Mapper
await shareKnowledgeWithRetry({
  source: "competitive-intel",
  targets: ["positioning-mapper"],
  domain: "competitive-landscape",
  content: {
    competitors: [...],
    market_shares: {...},
    trends: [...]
  },
  ttl: 90 * 24 * 60 * 60 * 1000
});

// 4. Market Trends → Positioning Mapper
await shareKnowledgeWithRetry({
  source: "market-trends",
  targets: ["positioning-mapper"],
  domain: "market-dynamics",
  content: {
    trends: [...],
    forecasts: {...},
    disruptions: [...]
  },
  ttl: 90 * 24 * 60 * 60 * 1000
});

// 5. All Business Research → Integration
await shareKnowledgeWithRetry({
  source: "positioning-mapper",
  targets: ["business-integrator"],
  domain: "business-integration",
  content: {
    positioning: {...},
    opportunities: [...],
    recommendations: [...]
  },
  ttl: 90 * 24 * 60 * 60 * 1000
});
```

### Business Strategy Knowledge Flows

```javascript
// 1. Business Structure → SWOT Analyzer
await shareKnowledgeWithRetry({
  source: "business-structure",
  targets: ["swot-analyzer"],
  domain: "structure-data",
  content: {
    org_structure: {...},
    processes: [...],
    systems: [...]
  },
  ttl: 90 * 24 * 60 * 60 * 1000
});

// 2. SWOT Analysis → Porter's Forces Analyzer
await shareKnowledgeWithRetry({
  source: "swot-analyzer",
  targets: ["porters-forces"],
  domain: "swot-analysis",
  content: {
    strengths: [...],
    weaknesses: [...],
    opportunities: [...],
    threats: [...]
  },
  ttl: 90 * 24 * 60 * 60 * 1000
});

// 3. Porter's Forces → PESTLE Analyzer
await shareKnowledgeWithRetry({
  source: "porters-forces",
  targets: ["pestle-analyzer"],
  domain: "industry-forces",
  content: {
    competitive_rivalry: {...},
    supplier_power: {...},
    buyer_power: {...}
  },
  ttl: 90 * 24 * 60 * 60 * 1000
});

// 4. PESTLE → Strategy Synthesizer
await shareKnowledgeWithRetry({
  source: "pestle-analyzer",
  targets: ["strategy-synthesizer"],
  domain: "external-factors",
  content: {
    political: [...],
    economic: [...],
    social: [...],
    technological: [...],
    legal: [...],
    environmental: [...]
  },
  ttl: 90 * 24 * 60 * 60 * 1000
});

// 5. Strategy Synthesis → Initiative Planner
await shareKnowledgeWithRetry({
  source: "strategy-synthesizer",
  targets: ["initiative-planner"],
  domain: "strategy-synthesis",
  content: {
    strategic_options: [...],
    recommendations: [...],
    priorities: [...]
  },
  ttl: 90 * 24 * 60 * 60 * 1000
});
```

### Knowledge Flow Orchestrator

```javascript
// Master orchestration function
async function orchestrateKnowledgeFlows(workflow) {
  const flows = {
    'phd-research': [
      { source: 'literature-mapper', targets: ['gap-hunter', 'contradiction-analyzer', 'thematic-synthesizer'], domain: 'literature-corpus' },
      { source: 'gap-hunter', targets: ['theory-builder'], domain: 'research-gaps' },
      { source: 'contradiction-analyzer', targets: ['literature-mapper'], domain: 'contradictions' },
      { source: 'theory-builder', targets: ['hypothesis-generator'], domain: 'theoretical-framework' },
      { source: 'hypothesis-generator', targets: ['methods-designer'], domain: 'hypotheses' },
      { source: 'methods-designer', targets: ['pilot-study-designer'], domain: 'research-methods' },
      { source: 'pilot-study-designer', targets: ['dissertation-architect'], domain: 'phd-integration' }
    ],
    'business-research': [
      { source: 'company-analyzer', targets: ['leadership-profiler'], domain: 'company-data' },
      { source: 'leadership-profiler', targets: ['positioning-mapper'], domain: 'leadership-insights' },
      { source: 'competitive-intel', targets: ['positioning-mapper'], domain: 'competitive-landscape' },
      { source: 'market-trends', targets: ['positioning-mapper'], domain: 'market-dynamics' },
      { source: 'positioning-mapper', targets: ['business-integrator'], domain: 'business-integration' }
    ],
    'business-strategy': [
      { source: 'business-structure', targets: ['swot-analyzer'], domain: 'structure-data' },
      { source: 'swot-analyzer', targets: ['porters-forces'], domain: 'swot-analysis' },
      { source: 'porters-forces', targets: ['pestle-analyzer'], domain: 'industry-forces' },
      { source: 'pestle-analyzer', targets: ['strategy-synthesizer'], domain: 'external-factors' },
      { source: 'strategy-synthesizer', targets: ['initiative-planner'], domain: 'strategy-synthesis' }
    ]
  };

  const workflowFlows = flows[workflow];
  if (!workflowFlows) {
    throw new Error(`Unknown workflow: ${workflow}`);
  }

  const results = [];
  for (const flow of workflowFlows) {
    try {
      await shareKnowledgeWithRetry({
        ...flow,
        content: {}, // Populated at runtime
        ttl: workflow === 'phd-research' ? 180 * 24 * 60 * 60 * 1000 : 90 * 24 * 60 * 60 * 1000
      });
      results.push({ flow, status: 'success' });
    } catch (error) {
      results.push({ flow, status: 'failed', error: error.message });
    }
  }

  return results;
}
```

## Implementation Steps

1. **Create Knowledge Sharing Module** (`src/knowledge-sharing.ts`)
   - Implement `shareKnowledgeWithRetry()` with exponential backoff
   - Add domain isolation and TTL management
   - Implement audit logging

2. **Define Knowledge Flow Topologies** (`src/knowledge-flows.ts`)
   - PhD Research flows (7 flows)
   - Business Research flows (5 flows)
   - Business Strategy flows (5 flows)

3. **Create Orchestrator** (`src/knowledge-orchestrator.ts`)
   - Master function to execute all flows for a workflow
   - Error aggregation and reporting
   - Success rate tracking

4. **Add Integration Hooks** (`src/hooks/knowledge-hooks.ts`)
   - Pre-share validation
   - Post-share verification
   - Failure recovery

5. **Create Test Suite** (`tests/knowledge-sharing.test.ts`)
   - Test retry logic with simulated failures
   - Verify TTL enforcement
   - Test domain isolation
   - Validate all 17 knowledge flows

## Validation Criteria

- [ ] All 17 knowledge flows configured and tested
- [ ] Knowledge sharing failure rate <5%
- [ ] Retry logic works with exponential backoff
- [ ] TTL correctly applied (180 days PhD, 90 days Business)
- [ ] Domain isolation prevents cross-contamination
- [ ] Audit trail captures all transfers
- [ ] Success metrics logged to memory
- [ ] Integration with TASK-007 monitoring

## Test Cases

```typescript
describe('Knowledge Sharing Infrastructure', () => {
  test('shares knowledge with retry on transient failure', async () => {
    // Simulate 2 failures then success
    const result = await shareKnowledgeWithRetry(mockConfig);
    expect(result).toBeDefined();
  });

  test('fails after max retries exhausted', async () => {
    // Simulate persistent failure
    await expect(shareKnowledgeWithRetry(mockConfig, 2))
      .rejects.toThrow('failed after 2 attempts');
  });

  test('applies correct TTL for PhD workflow', async () => {
    const ttl = 180 * 24 * 60 * 60 * 1000;
    await shareKnowledgeWithRetry({ ...mockConfig, ttl });
    // Verify expires_at timestamp
  });

  test('isolates knowledge domains', async () => {
    await shareKnowledgeWithRetry({ domain: 'literature-corpus', ... });
    await shareKnowledgeWithRetry({ domain: 'company-data', ... });
    // Verify no cross-contamination
  });

  test('orchestrates complete PhD workflow', async () => {
    const results = await orchestrateKnowledgeFlows('phd-research');
    expect(results.filter(r => r.status === 'success')).toHaveLength(7);
  });
});
```

## Forward Compatibility

This task enables:
- **TASK-009**: Pattern storage will use knowledge domains
- **TASK-010**: Feedback loops will leverage knowledge sharing
- **TASK-011**: Continuous learning will aggregate shared knowledge
- **TASK-012**: Learning objectives will be derived from knowledge flows
- **TASK-013**: Adaptive workflows will optimize based on knowledge transfer metrics

## Success Metrics

- All 17 knowledge flows operational
- <5% sharing failure rate
- Retry logic recovers from 95%+ transient failures
- TTL enforcement prevents stale data
- Domain isolation verified
- Audit trail complete

---

**Status**: PENDING
**Assigned To**: TBD
**Created**: 2025-11-27
**Phase**: SHORT-TERM (90-day milestone)
