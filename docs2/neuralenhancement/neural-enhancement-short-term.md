# Neural Enhancement Implementation Prompt - SHORT-TERM (2-3 hours)

## PREREQUISITE

This prompt REQUIRES completion of `neural-enhancement-immediate.md` first. Verify by running:

```javascript
mcp__ruv-swarm__daa_learning_status({ detailed: true })
```

**Required State**: All agents from immediate prompt should exist with cognitive patterns assigned.

## ⚠️ CRITICAL ADDITIONS TO SHORT-TERM

This updated prompt now includes:
1. **Pattern Expiry Mechanisms** - Prevent stale patterns from contaminating research
2. **Concurrent Project Isolation** - Support multiple simultaneous research streams
3. **Advanced Error Recovery** - Handle knowledge sharing failures gracefully
4. **Performance Degradation Detection** - Alert on declining agent effectiveness
5. **Cross-Domain Transfer Safety** - Prevent inappropriate pattern transfers

---

## OBJECTIVE

You are implementing knowledge sharing infrastructure and pattern storage for research agent swarms. This prompt covers:
1. Creating knowledge sharing hooks between related agents
2. Defining knowledge flow topologies for each swarm type
3. Implementing successful research pattern storage
4. Setting up meta-learning for cross-domain transfer
5. Creating feedback loops for continuous improvement

---

## PHASE 0: CONCURRENT PROJECT ISOLATION SETUP

### Step 0.1: Retrieve Active Project ID

```bash
# Get project ID from immediate implementation
PROJECT_ID=$(npx claude-flow memory retrieve --key "projects/*/project-metadata" | jq -r '.project_id' | tail -1)
echo "Active Project ID: $PROJECT_ID"

# Verify this is YOUR project
npx claude-flow memory retrieve --key "projects/$PROJECT_ID/project-metadata"
```

### Step 0.2: Create Project-Specific Knowledge Namespaces

```bash
# Create isolated knowledge namespaces for this project
npx claude-flow memory store "knowledge-namespaces" "{
  \"project_id\": \"$PROJECT_ID\",
  \"namespaces\": [
    \"projects/$PROJECT_ID/knowledge/literature-corpus\",
    \"projects/$PROJECT_ID/knowledge/research-gaps\",
    \"projects/$PROJECT_ID/knowledge/contradictions\",
    \"projects/$PROJECT_ID/knowledge/theoretical-framework\",
    \"projects/$PROJECT_ID/knowledge/hypotheses\",
    \"projects/$PROJECT_ID/knowledge/company-intelligence\",
    \"projects/$PROJECT_ID/knowledge/leadership-intelligence\",
    \"projects/$PROJECT_ID/knowledge/competitive-landscape\",
    \"projects/$PROJECT_ID/knowledge/positioning-strategy\"
  ],
  \"isolation_mode\": \"strict\",
  \"created_at\": \"$(date -Iseconds)\"
}" --namespace "projects/$PROJECT_ID/config"
```

### Step 0.3: Establish Pattern Expiry Policy

```bash
# Define pattern lifecycle rules
npx claude-flow memory store "pattern-expiry-policy" "{
  \"policy_version\": \"1.0\",
  \"project_id\": \"$PROJECT_ID\",
  \"expiry_rules\": {
    \"phd_patterns\": {
      \"max_age_days\": 180,
      \"reason\": \"Research methodologies evolve, 6-month refresh cycle\"
    },
    \"business_research_patterns\": {
      \"max_age_days\": 90,
      \"reason\": \"Market dynamics change rapidly, quarterly refresh\"
    },
    \"business_strategy_patterns\": {
      \"max_age_days\": 60,
      \"reason\": \"Competitive landscape shifts fast, bi-monthly refresh\"
    },
    \"industry_patterns\": {
      \"max_age_days\": 120,
      \"reason\": \"Industry trends evolve moderately, 4-month refresh\"
    }
  },
  \"auto_archive\": true,
  \"archive_namespace\": \"patterns/archived\",
  \"created_at\": \"$(date -Iseconds)\"
}" --namespace "config/patterns/expiry"
```

---

## PHASE 1: KNOWLEDGE SHARING INFRASTRUCTURE

### Understanding Knowledge Flow

Knowledge flows between agents in three patterns:

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Sequential** | A → B → C | Pipeline workflows where each step builds on previous |
| **Broadcast** | A → [B, C, D] | One agent's findings needed by multiple downstream agents |
| **Mesh** | A ↔ B ↔ C | Collaborative agents that need real-time sync |

### Step 1.1: Define PhD Research Knowledge Flow Topology

The PhD research workflow has this knowledge dependency structure:

```
EXPLORATION PHASE
┌─────────────────────┐
│ literature-mapper   │──┬──→ gap-hunter
│ (divergent)         │  │
└─────────────────────┘  ├──→ contradiction-analyzer
                         │
                         └──→ literature-review-writer
                                      │
SYNTHESIS PHASE                       ▼
┌─────────────────────┐    ┌─────────────────────┐
│ theory-builder      │◄───│ thematic-synthesizer │
│ (systems)           │    │ (systems)            │
└─────────────────────┘    └─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ hypothesis-generator │──→ opportunity-identifier
│ (divergent)          │
└─────────────────────┘
         │
EXECUTION PHASE       ▼
┌─────────────────────┐
│ methodology-writer  │──→ results-writer ──→ discussion-writer ──→ conclusion-writer
│ (convergent)        │
└─────────────────────┘
         │
QA OVERLAY (parallel) ▼
┌─────────────────────────────────────────────────────────────┐
│ adversarial-reviewer ←→ quality-assessor ←→ bias-detector  │
│ validity-guardian                                           │
└─────────────────────────────────────────────────────────────┘
```

### Step 1.2: Implement PhD Research Knowledge Sharing Hooks

Execute these knowledge sharing configurations:

```javascript
// EXPLORATION → SYNTHESIS knowledge flow
// literature-mapper broadcasts to analysis agents
// WITH PROJECT ISOLATION AND ERROR RECOVERY

async function shareKnowledgeWithRetry(config, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = await mcp__ruv-swarm__daa_knowledge_share(config);

      // Store success log
      await npx claude-flow memory store `knowledge-share-success-${Date.now()}` JSON.stringify({
        project_id: PROJECT_ID,
        source: config.sourceAgentId,
        targets: config.targetAgentIds,
        domain: config.knowledgeDomain,
        timestamp: new Date().toISOString(),
        attempt: attempt
      }) --namespace `projects/${PROJECT_ID}/knowledge-logs`;

      return result;
    } catch (error) {
      console.error(`Attempt ${attempt}/${maxRetries} failed:`, error.message);

      if (attempt === maxRetries) {
        // Store failure log
        await npx claude-flow memory store `knowledge-share-failure-${Date.now()}` JSON.stringify({
          project_id: PROJECT_ID,
          source: config.sourceAgentId,
          targets: config.targetAgentIds,
          error: error.message,
          timestamp: new Date().toISOString()
        }) --namespace `projects/${PROJECT_ID}/errors`;

        throw new Error(`Knowledge sharing failed after ${maxRetries} attempts`);
      }

      // Exponential backoff
      await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, attempt)));
    }
  }
}

// Execute with project isolation
await shareKnowledgeWithRetry({
  sourceAgentId: `literature-mapper-${PROJECT_ID}`,
  targetAgentIds: [
    `gap-hunter-${PROJECT_ID}`,
    `contradiction-analyzer-${PROJECT_ID}`,
    `literature-review-writer-${PROJECT_ID}`,
    `thematic-synthesizer-${PROJECT_ID}`
  ],
  knowledgeDomain: "literature-corpus",
  knowledgeContent: {
    description: "Complete literature corpus with categorization",
    includes: ["source-list", "categorization-schema", "citation-network", "theme-clusters"],
    format: "structured-json",
    retrieval_key: `projects/${PROJECT_ID}/knowledge/literature-corpus`,
    project_id: PROJECT_ID,
    created_at: new Date().toISOString(),
    expires_at: new Date(Date.now() + 180 * 24 * 60 * 60 * 1000).toISOString() // 180 days
  }
})

// gap-hunter → theory-builder knowledge flow
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "gap-hunter",
  targetAgentIds: ["theory-builder", "opportunity-identifier", "hypothesis-generator"],
  knowledgeDomain: "research-gaps",
  knowledgeContent: {
    description: "Identified gaps in existing literature",
    includes: ["gap-list", "gap-severity", "gap-opportunities", "unexplored-areas"],
    format: "structured-json",
    retrieval_key: "project/analysis/gaps"
  }
})

// contradiction-analyzer → theory-builder knowledge flow
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "contradiction-analyzer",
  targetAgentIds: ["theory-builder", "thematic-synthesizer", "adversarial-reviewer"],
  knowledgeDomain: "contradictions",
  knowledgeContent: {
    description: "Contradictions and conflicts in literature",
    includes: ["contradiction-list", "reconciliation-attempts", "unresolved-conflicts"],
    format: "structured-json",
    retrieval_key: "project/analysis/contradictions"
  }
})

// theory-builder → hypothesis-generator knowledge flow
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "theory-builder",
  targetAgentIds: ["hypothesis-generator", "methodology-writer", "discussion-writer"],
  knowledgeDomain: "theoretical-framework",
  knowledgeContent: {
    description: "Constructed theoretical framework",
    includes: ["framework-structure", "key-constructs", "relationships", "propositions"],
    format: "structured-json",
    retrieval_key: "project/theory/framework"
  }
})

// hypothesis-generator → methodology-writer knowledge flow
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "hypothesis-generator",
  targetAgentIds: ["methodology-writer", "results-writer", "adversarial-reviewer"],
  knowledgeDomain: "hypotheses",
  knowledgeContent: {
    description: "Testable hypotheses derived from theory",
    includes: ["hypothesis-list", "variables", "expected-relationships", "testability-criteria"],
    format: "structured-json",
    retrieval_key: "project/hypotheses/list"
  }
})

// QA agents mesh network (bidirectional sharing)
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "adversarial-reviewer",
  targetAgentIds: ["quality-assessor", "bias-detector", "validity-guardian"],
  knowledgeDomain: "quality-concerns",
  knowledgeContent: {
    description: "Quality issues and concerns identified",
    includes: ["weaknesses", "assumptions-challenged", "recommendations"],
    format: "structured-json",
    retrieval_key: "project/qa/adversarial-findings"
  }
})

mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "quality-assessor",
  targetAgentIds: ["adversarial-reviewer", "bias-detector", "validity-guardian"],
  knowledgeDomain: "quality-assessment",
  knowledgeContent: {
    description: "Formal quality assessment results",
    includes: ["casp-scores", "jbi-assessment", "quality-grades"],
    format: "structured-json",
    retrieval_key: "project/qa/quality-scores"
  }
})
```

### Step 1.3: Implement Business Research Knowledge Sharing Hooks

```javascript
// company-intelligence → all downstream agents
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "company-intelligence-researcher",
  targetAgentIds: ["leadership-profiler", "strategic-positioning-analyst", "competitive-intelligence", "conversation-script-writer"],
  knowledgeDomain: "company-intelligence",
  knowledgeContent: {
    description: "Complete company intelligence package",
    includes: ["business-model", "market-position", "technology-stack", "recent-developments", "key-metrics"],
    format: "structured-json",
    retrieval_key: "project/research/company-intel"
  }
})

// leadership-profiler → conversation and positioning agents
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "leadership-profiler",
  targetAgentIds: ["conversation-script-writer", "strategic-positioning-analyst", "sales-enablement-specialist"],
  knowledgeDomain: "leadership-intelligence",
  knowledgeContent: {
    description: "Decision-maker profiles and stakeholder map",
    includes: ["executive-profiles", "priorities", "communication-styles", "influence-map", "decision-process"],
    format: "structured-json",
    retrieval_key: "project/research/leadership"
  }
})

// competitive-intelligence → positioning agents
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "competitive-intelligence",
  targetAgentIds: ["strategic-positioning-analyst", "positioning-strategist", "conversation-script-writer"],
  knowledgeDomain: "competitive-landscape",
  knowledgeContent: {
    description: "Competitive analysis and market structure",
    includes: ["competitor-profiles", "positioning-gaps", "differentiation-opportunities", "market-dynamics"],
    format: "structured-json",
    retrieval_key: "project/research/competitive"
  }
})

// strategic-positioning-analyst → communication agents
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "strategic-positioning-analyst",
  targetAgentIds: ["positioning-strategist", "conversation-script-writer", "sales-enablement-specialist", "executive-brief-writer"],
  knowledgeDomain: "positioning-strategy",
  knowledgeContent: {
    description: "Strategic positioning and value proposition",
    includes: ["value-proposition", "differentiation-points", "target-angles", "messaging-framework"],
    format: "structured-json",
    retrieval_key: "project/strategy/positioning"
  }
})

// All intelligence → executive-brief-writer (synthesis)
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "research-orchestrator",
  targetAgentIds: ["executive-brief-writer"],
  knowledgeDomain: "complete-research-package",
  knowledgeContent: {
    description: "All research findings for final synthesis",
    includes: ["company-intel", "leadership-profiles", "competitive-analysis", "positioning-strategy", "conversation-scripts"],
    format: "structured-json",
    retrieval_key: "project/research/complete-package"
  }
})
```

### Step 1.4: Implement Business Strategy Knowledge Sharing Hooks

```javascript
// structural-mapper → analysis agents
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "structural-mapper",
  targetAgentIds: ["flow-analyst", "gap-analyzer", "risk-analyst", "problem-validator"],
  knowledgeDomain: "structural-map",
  knowledgeContent: {
    description: "Complete structural architecture map",
    includes: ["component-hierarchy", "interfaces", "dependencies", "architecture-patterns"],
    format: "structured-json",
    retrieval_key: "project/structure/map"
  }
})

// flow-analyst → optimization agents
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "flow-analyst",
  targetAgentIds: ["gap-analyzer", "opportunity-generator", "risk-analyst"],
  knowledgeDomain: "flow-analysis",
  knowledgeContent: {
    description: "Data and process flow analysis",
    includes: ["data-flows", "process-flows", "bottlenecks", "critical-paths"],
    format: "structured-json",
    retrieval_key: "project/flows/analysis"
  }
})

// gap-analyzer + risk-analyst → opportunity-generator
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "gap-analyzer",
  targetAgentIds: ["opportunity-generator", "strategic-researcher"],
  knowledgeDomain: "identified-gaps",
  knowledgeContent: {
    description: "Gaps and improvement opportunities",
    includes: ["gap-list", "severity-scores", "improvement-potential", "priority-ranking"],
    format: "structured-json",
    retrieval_key: "project/gaps/identified"
  }
})

mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "risk-analyst",
  targetAgentIds: ["opportunity-generator", "problem-validator"],
  knowledgeDomain: "risk-assessment",
  knowledgeContent: {
    description: "Risk analysis and FMEA results",
    includes: ["failure-modes", "risk-scores", "mitigation-strategies", "rpn-rankings"],
    format: "structured-json",
    retrieval_key: "project/risks/assessment"
  }
})

// step-back-analyzer → all agents (principles broadcast)
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "step-back-analyzer",
  targetAgentIds: ["structural-mapper", "flow-analyst", "gap-analyzer", "risk-analyst", "opportunity-generator", "problem-validator"],
  knowledgeDomain: "guiding-principles",
  knowledgeContent: {
    description: "High-level guiding principles for analysis",
    includes: ["core-principles", "success-criteria", "anti-patterns", "evaluation-framework"],
    format: "structured-json",
    retrieval_key: "project/principles/core"
  }
})
```

---

## PHASE 2: SUCCESSFUL RESEARCH PATTERN STORAGE

### Understanding Pattern Storage

Patterns are reusable templates learned from successful research outcomes. They include:
- **Process patterns**: Sequence of steps that worked well
- **Quality patterns**: Indicators that predicted high-quality output
- **Failure patterns**: Anti-patterns to avoid
- **Adaptation patterns**: How agents adjusted to different contexts

### Step 2.1: Create Pattern Storage Namespaces

```bash
# Initialize pattern storage namespaces
npx claude-flow memory store "namespace-init" '{
  "namespaces": [
    "patterns/phd/successful",
    "patterns/phd/failed",
    "patterns/business-research/successful",
    "patterns/business-research/failed",
    "patterns/business-strategy/successful",
    "patterns/business-strategy/failed",
    "patterns/cross-domain/transfers"
  ],
  "created_at": "'"$(date -Iseconds)"'"
}' --namespace "config/patterns"
```

### Step 2.2: Define PhD Research Success Pattern Template

Store this template for capturing successful PhD research patterns WITH EXPIRY:

```bash
npx claude-flow memory store "phd-success-template" "{
  \"pattern_type\": \"phd-research-success\",
  \"version\": \"2.0\",
  \"template\": {
    \"research_id\": \"<unique-identifier>\",
    \"project_id\": \"$PROJECT_ID\",
    \"created_at\": \"<ISO-date>\",
    \"expires_at\": \"<ISO-date-plus-180-days>\",
    \"archived\": false,
    "topic_domain": "<research-domain>",
    "completion_date": "<ISO-date>",
    "quality_score": "<0-100>",
    "process_metrics": {
      "total_sources_analyzed": "<number>",
      "gaps_identified": "<number>",
      "contradictions_resolved": "<number>",
      "hypotheses_generated": "<number>",
      "hypotheses_validated": "<number>"
    },
    "agent_performance": {
      "literature-mapper": {
        "effectiveness": "<0-1>",
        "cognitive_pattern_fit": "<0-1>",
        "key_decisions": ["<decision-1>", "<decision-2>"]
      },
      "gap-hunter": {
        "effectiveness": "<0-1>",
        "cognitive_pattern_fit": "<0-1>",
        "key_findings": ["<finding-1>", "<finding-2>"]
      },
      "theory-builder": {
        "effectiveness": "<0-1>",
        "cognitive_pattern_fit": "<0-1>",
        "framework_quality": "<0-1>"
      },
      "adversarial-reviewer": {
        "effectiveness": "<0-1>",
        "issues_caught": "<number>",
        "false_positives": "<number>"
      }
    },
    "knowledge_flow_effectiveness": {
      "literature_to_gaps": "<0-1>",
      "gaps_to_theory": "<0-1>",
      "theory_to_hypotheses": "<0-1>",
      "hypotheses_to_methodology": "<0-1>"
    },
    "lessons_learned": ["<lesson-1>", "<lesson-2>"],
    "reusable_components": {
      "search_strategy": "<description>",
      "gap_identification_criteria": "<description>",
      "theoretical_framework_structure": "<description>"
    }
  }
}' --namespace "patterns/templates"
```

### Step 2.3: Define Business Research Success Pattern Template

```bash
npx claude-flow memory store "business-research-success-template" '{
  "pattern_type": "business-research-success",
  "template": {
    "research_id": "<unique-identifier>",
    "target_company": "<company-name>",
    "research_objective": "<objective>",
    "completion_date": "<ISO-date>",
    "outcome": {
      "deal_closed": "<boolean>",
      "relationship_established": "<boolean>",
      "quality_score": "<0-100>"
    },
    "intelligence_quality": {
      "company_intel_accuracy": "<0-1>",
      "leadership_profile_depth": "<0-1>",
      "competitive_analysis_usefulness": "<0-1>",
      "positioning_resonance": "<0-1>"
    },
    "agent_performance": {
      "company-intelligence-researcher": {
        "effectiveness": "<0-1>",
        "key_insights": ["<insight-1>", "<insight-2>"]
      },
      "leadership-profiler": {
        "effectiveness": "<0-1>",
        "lateral_thinking_value": "<0-1>",
        "non_obvious_findings": ["<finding-1>"]
      },
      "strategic-positioning-analyst": {
        "effectiveness": "<0-1>",
        "positioning_accuracy": "<0-1>"
      },
      "conversation-script-writer": {
        "effectiveness": "<0-1>",
        "scripts_used": "<number>",
        "scripts_effective": "<number>"
      }
    },
    "what_worked": ["<success-factor-1>", "<success-factor-2>"],
    "what_didnt_work": ["<failure-factor-1>"],
    "transferable_patterns": {
      "industry_specific": "<pattern-description>",
      "executive_type_specific": "<pattern-description>",
      "deal_size_specific": "<pattern-description>"
    }
  }
}' --namespace "patterns/templates"
```

### Step 2.4: Create Pattern Recording Workflow with Expiry Check

This workflow should be executed after EVERY completed research project:

**NEW: Includes automatic pattern expiry checking and cleanup**

```javascript
// Create a DAA workflow for pattern recording
mcp__ruv-swarm__daa_workflow_create({
  id: "pattern-recording-workflow",
  name: "Research Pattern Recording",
  strategy: "sequential",
  steps: [
    {
      id: "collect-metrics",
      name: "Collect Performance Metrics",
      agent: "meta-learning-orchestrator",
      action: "Gather all agent performance metrics and knowledge flow effectiveness scores"
    },
    {
      id: "analyze-success-factors",
      name: "Analyze Success Factors",
      agent: "step-back-analyzer",
      action: "Identify what worked well and what didn't in this research cycle"
    },
    {
      id: "extract-patterns",
      name: "Extract Reusable Patterns",
      agent: "synthesis-specialist",
      action: "Synthesize learnings into reusable pattern templates"
    },
    {
      id: "check-expiry",
      name: "Check for Expired Patterns",
      agent: "meta-learning-orchestrator",
      action: "Scan all pattern namespaces for expired patterns based on expiry policy"
    },
    {
      id: "archive-expired",
      name: "Archive Expired Patterns",
      agent: "meta-learning-orchestrator",
      action: "Move expired patterns to archive namespace, update indexes"
    },
    {
      id: "store-patterns",
      name: "Store Patterns in Memory",
      agent: "meta-learning-orchestrator",
      action: "Store extracted patterns with creation date and calculated expiry date"
    },
    {
      id: "update-agent-learning",
      name: "Update Agent Learning",
      agent: "meta-learning-orchestrator",
      action: "Feed learnings back to agents via daa_agent_adapt"
    }
  ],
  dependencies: {
    "analyze-success-factors": ["collect-metrics"],
    "extract-patterns": ["analyze-success-factors"],
    "store-patterns": ["extract-patterns"],
    "update-agent-learning": ["store-patterns"]
  }
})
```

### Step 2.5: Implement Feedback Loop for Agent Adaptation

After each research project, execute feedback for each agent:

```javascript
// Example: PhD research completed successfully
// Execute for each agent that participated

// Literature mapper feedback
mcp__ruv-swarm__daa_agent_adapt({
  agentId: "literature-mapper",
  performanceScore: 0.92,  // Based on quality assessment
  feedback: "Divergent pattern worked well for broad exploration. Found 47 sources, 12 were highly relevant.",
  suggestions: ["Consider adding temporal filtering for recent publications", "Citation network analysis was valuable"]
})

// Gap hunter feedback
mcp__ruv-swarm__daa_agent_adapt({
  agentId: "gap-hunter",
  performanceScore: 0.88,
  feedback: "Critical pattern effectively identified 8 significant gaps. 6 led to novel hypotheses.",
  suggestions: ["Gap severity scoring helped prioritization", "Cross-domain gap identification needs improvement"]
})

// Theory builder feedback
mcp__ruv-swarm__daa_agent_adapt({
  agentId: "theory-builder",
  performanceScore: 0.85,
  feedback: "Systems pattern built coherent framework. Integration with existing theories was strong.",
  suggestions: ["Earlier integration of contradictions would improve framework robustness"]
})

// Adversarial reviewer feedback
mcp__ruv-swarm__daa_agent_adapt({
  agentId: "adversarial-reviewer",
  performanceScore: 0.95,
  feedback: "Critical pattern caught 3 major issues before finalization. Zero false positives.",
  suggestions: ["Increase learning rate due to high performance", "Pattern matching for common weakness types"]
})
```

---

## PHASE 3: META-LEARNING FOR CROSS-DOMAIN TRANSFER

### Understanding Meta-Learning

Meta-learning enables agents to transfer knowledge between different research domains:
- PhD research patterns → Business research applications
- Successful business deals → New target research
- One industry vertical → Another industry vertical

### Step 3.1: Configure Cross-Domain Transfer Rules with Safety Checks

**NEW: Transfer safety validation prevents inappropriate cross-domain contamination**

```javascript
// Transfer safety validator
async function validateMetaLearningTransfer(config) {
  const { sourceDomain, targetDomain, transferMode, agentIds } = config;

  // Define transfer compatibility matrix
  const transferCompatibility = {
    "phd-literature-analysis": ["business-competitive-intelligence", "market-research"],
    "business-stakeholder-analysis": ["phd-methodology-design", "sampling-strategy"],
    "successful-deal-patterns": ["new-target-research", "similar-vertical-research"],
    "tech-industry-patterns": ["saas-industry-patterns"], // NOT healthcare - too different
    "healthcare-industry-patterns": ["medical-device-patterns"], // NOT fintech
    "finserv-industry-patterns": ["banking-patterns", "insurance-patterns"]
  };

  // Check if transfer is safe
  const allowedTargets = transferCompatibility[sourceDomain] || [];

  if (!allowedTargets.includes(targetDomain)) {
    const warning = {
      source: sourceDomain,
      target: targetDomain,
      warning: "UNSAFE_TRANSFER",
      reason: `${sourceDomain} patterns may not be applicable to ${targetDomain}`,
      recommendation: "Use 'gradual' mode with manual review, or avoid transfer",
      timestamp: new Date().toISOString()
    };

    await npx claude-flow memory store `transfer-warning-${Date.now()}` JSON.stringify(warning) --namespace `projects/${PROJECT_ID}/warnings`;

    console.warn(`⚠️  WARNING: Unsafe cross-domain transfer detected`);
    console.warn(`   Source: ${sourceDomain}`);
    console.warn(`   Target: ${targetDomain}`);
    console.warn(`   Recommendation: ${warning.recommendation}`);

    // Allow override with explicit confirmation
    if (transferMode !== "gradual") {
      throw new Error("Unsafe transfer blocked. Use transferMode='gradual' to proceed with caution.");
    }
  }

  return true;
}

// PhD → Business Research transfer (VALIDATED)
const phdToBusinessConfig = {
  sourceDomain: "phd-literature-analysis",
  targetDomain: "business-competitive-intelligence",
  transferMode: "adaptive",
  agentIds: [
    `literature-mapper-${PROJECT_ID}`,
    `company-intelligence-researcher-${PROJECT_ID}`,
    `competitive-intelligence-${PROJECT_ID}`
  ],
  project_id: PROJECT_ID
};

await validateMetaLearningTransfer(phdToBusinessConfig);
await mcp__ruv-swarm__daa_meta_learning(phdToBusinessConfig);

// Business Research → PhD transfer
mcp__ruv-swarm__daa_meta_learning({
  sourceDomain: "business-stakeholder-analysis",
  targetDomain: "phd-methodology-design",
  transferMode: "gradual",
  agentIds: ["leadership-profiler", "methodology-writer", "sampling-strategist"]
})

// Successful deals → New research transfer
mcp__ruv-swarm__daa_meta_learning({
  sourceDomain: "successful-deal-patterns",
  targetDomain: "new-target-research",
  transferMode: "direct",
  agentIds: ["company-intelligence-researcher", "leadership-profiler", "strategic-positioning-analyst"]
})

// Cross-industry pattern transfer
mcp__ruv-swarm__daa_meta_learning({
  sourceDomain: "tech-industry-patterns",
  targetDomain: "healthcare-industry-patterns",
  transferMode: "gradual",
  agentIds: ["company-intelligence-researcher", "competitive-intelligence", "strategic-positioning-analyst"]
})
```

### Step 3.2: Store Domain-Specific Pattern Libraries

```bash
# Tech industry patterns
npx claude-flow memory store "tech-industry-patterns" '{
  "domain": "technology",
  "common_patterns": {
    "decision_makers": ["CTO-led", "product-led", "engineering-led"],
    "evaluation_criteria": ["technical-fit", "scalability", "integration-ease", "developer-experience"],
    "sales_cycle": "3-6 months typical",
    "key_differentiators": ["performance", "security", "extensibility"]
  },
  "successful_approaches": [
    "Technical deep-dive with engineering team",
    "POC/pilot before commitment",
    "Developer advocacy approach"
  ],
  "anti_patterns": [
    "Skipping technical validation",
    "Overselling capabilities",
    "Ignoring integration complexity"
  ]
}' --namespace "patterns/industries/tech"

# Healthcare industry patterns
npx claude-flow memory store "healthcare-industry-patterns" '{
  "domain": "healthcare",
  "common_patterns": {
    "decision_makers": ["CMIO-led", "compliance-led", "procurement-led"],
    "evaluation_criteria": ["HIPAA-compliance", "interoperability", "clinical-workflow-fit", "EHR-integration"],
    "sales_cycle": "12-18 months typical",
    "key_differentiators": ["compliance", "clinical-validation", "workflow-efficiency"]
  },
  "successful_approaches": [
    "Compliance-first positioning",
    "Clinical champion identification",
    "Pilot with measurable outcomes"
  ],
  "anti_patterns": [
    "Underestimating compliance requirements",
    "Ignoring clinical workflow impact",
    "Rushing procurement process"
  ]
}' --namespace "patterns/industries/healthcare"

# Financial services patterns
npx claude-flow memory store "finserv-industry-patterns" '{
  "domain": "financial-services",
  "common_patterns": {
    "decision_makers": ["CISO-led", "risk-led", "operations-led"],
    "evaluation_criteria": ["security", "regulatory-compliance", "audit-trail", "reliability"],
    "sales_cycle": "6-12 months typical",
    "key_differentiators": ["security-certifications", "uptime-SLA", "regulatory-expertise"]
  },
  "successful_approaches": [
    "Security and compliance emphasis",
    "Risk mitigation positioning",
    "Reference customers in same vertical"
  ],
  "anti_patterns": [
    "Downplaying security concerns",
    "Insufficient audit capabilities",
    "Ignoring regulatory landscape"
  ]
}' --namespace "patterns/industries/finserv"
```

### Step 3.3: Create Pattern Retrieval Workflow

Before starting any new research, agents should retrieve relevant patterns:

```javascript
// Create workflow for pattern-informed research start
mcp__ruv-swarm__daa_workflow_create({
  id: "pattern-informed-research-start",
  name: "Pattern-Informed Research Initialization",
  strategy: "sequential",
  steps: [
    {
      id: "identify-domain",
      name: "Identify Research Domain",
      agent: "meta-learning-orchestrator",
      action: "Determine which domain patterns are most relevant to this research"
    },
    {
      id: "retrieve-patterns",
      name: "Retrieve Relevant Patterns",
      agent: "meta-learning-orchestrator",
      action: "Retrieve successful patterns from identified domain and related domains"
    },
    {
      id: "distribute-patterns",
      name: "Distribute Patterns to Agents",
      agent: "meta-learning-orchestrator",
      action: "Share relevant patterns with each participating agent via knowledge_share"
    },
    {
      id: "configure-agents",
      name: "Configure Agent Parameters",
      agent: "meta-learning-orchestrator",
      action: "Adjust agent cognitive patterns and learning rates based on domain requirements"
    }
  ],
  dependencies: {
    "retrieve-patterns": ["identify-domain"],
    "distribute-patterns": ["retrieve-patterns"],
    "configure-agents": ["distribute-patterns"]
  }
})
```

---

## PHASE 4: CONTINUOUS IMPROVEMENT HOOKS

### Step 4.1: Create Post-Research Hook

This hook should execute after every research completion:

```bash
# Store the post-research hook configuration
npx claude-flow memory store "post-research-hook" '{
  "hook_name": "post-research-completion",
  "trigger": "research-completion",
  "actions": [
    {
      "order": 1,
      "action": "collect-performance-metrics",
      "command": "mcp__ruv-swarm__daa_performance_metrics({ category: \"all\" })"
    },
    {
      "order": 2,
      "action": "analyze-cognitive-pattern-effectiveness",
      "command": "For each agent: mcp__ruv-swarm__daa_cognitive_pattern({ agentId: \"<id>\", action: \"analyze\" })"
    },
    {
      "order": 3,
      "action": "record-success-pattern",
      "command": "Store pattern in patterns/<type>/successful namespace"
    },
    {
      "order": 4,
      "action": "update-agent-learning",
      "command": "For each agent: mcp__ruv-swarm__daa_agent_adapt({ agentId: \"<id>\", ... })"
    },
    {
      "order": 5,
      "action": "update-meta-learning",
      "command": "mcp__ruv-swarm__daa_meta_learning({ sourceDomain: \"<completed>\", targetDomain: \"<similar>\", ... })"
    }
  ]
}' --namespace "config/hooks"
```

### Step 4.2: Create Quality Threshold Alerts

```bash
npx claude-flow memory store "quality-thresholds" '{
  "thresholds": {
    "agent_effectiveness_minimum": 0.7,
    "knowledge_flow_effectiveness_minimum": 0.75,
    "cognitive_pattern_fit_minimum": 0.8,
    "overall_research_quality_minimum": 0.85
  },
  "actions_on_breach": {
    "agent_effectiveness_low": "Review cognitive pattern assignment, consider pattern change",
    "knowledge_flow_low": "Review knowledge sharing configuration, check retrieval paths",
    "cognitive_pattern_fit_low": "Reassign cognitive pattern via daa_cognitive_pattern change action",
    "overall_quality_low": "Full workflow review, pattern analysis, potential restructure"
  }
}' --namespace "config/quality"
```

### Step 4.3: Create Learning Rate Adjustment Rules

```bash
npx claude-flow memory store "learning-rate-rules" '{
  "adjustment_rules": {
    "high_performance_sustained": {
      "condition": "effectiveness > 0.9 for 3+ consecutive projects",
      "action": "Increase learning rate by 0.02 (max 0.2)",
      "rationale": "Agent has proven reliable, can learn faster"
    },
    "performance_decline": {
      "condition": "effectiveness dropped > 0.1 from previous project",
      "action": "Decrease learning rate by 0.02 (min 0.05)",
      "rationale": "Agent may be overfitting, slow down adaptation"
    },
    "new_domain_entry": {
      "condition": "First project in new domain",
      "action": "Set learning rate to 0.15",
      "rationale": "Higher learning rate for new territory"
    },
    "critical_agent_boost": {
      "condition": "Agent is adversarial-reviewer or quality-assessor",
      "action": "Maintain learning rate at 0.12-0.15",
      "rationale": "Critical agents need to stay sharp and adapt quickly"
    }
  }
}' --namespace "config/learning"
```

---

## PHASE 5: VERIFICATION AND TESTING

### Step 5.1: Verify Knowledge Sharing Configuration

```javascript
// Check all knowledge sharing is configured
mcp__ruv-swarm__daa_learning_status({
  detailed: true
})
```

**Expected**: Should show knowledge domains including all configured shares.

### Step 5.2: Test Knowledge Flow

Run a test knowledge share and verify retrieval:

```javascript
// Test: Share test knowledge
mcp__ruv-swarm__daa_knowledge_share({
  sourceAgentId: "literature-mapper",
  targetAgentIds: ["gap-hunter"],
  knowledgeDomain: "test-knowledge-flow",
  knowledgeContent: {
    test: true,
    message: "Knowledge flow test successful",
    timestamp: new Date().toISOString()
  }
})
```

### Step 5.3: Test Meta-Learning Configuration

```javascript
// Verify meta-learning is active
mcp__ruv-swarm__daa_performance_metrics({
  category: "neural"
})
```

### Step 5.4: Verify Pattern Storage

```bash
# Verify all pattern namespaces exist
npx claude-flow memory retrieve --key "config/patterns/namespace-init"
npx claude-flow memory retrieve --key "patterns/templates/phd-success-template"
npx claude-flow memory retrieve --key "patterns/templates/business-research-success-template"
npx claude-flow memory retrieve --key "patterns/industries/tech"
```

---

## PHASE 6: PERFORMANCE DEGRADATION DETECTION

### Step 6.1: Create Degradation Alert System

```bash
# Store degradation thresholds
npx claude-flow memory store "degradation-thresholds" "{
  \"project_id\": \"$PROJECT_ID\",
  \"thresholds\": {
    \"agent_effectiveness_drop\": 0.15,
    \"knowledge_flow_failure_rate\": 0.25,
    \"pattern_reuse_success_rate\": 0.70,
    \"learning_rate_drift\": 0.05,
    \"response_time_increase\": 2.0
  },
  \"check_frequency_hours\": 24,
  \"alert_actions\": [
    \"log_to_namespace\",
    \"email_admin\",
    \"pause_meta_learning\"
  ],
  \"created_at\": \"$(date -Iseconds)\"
}" --namespace "projects/$PROJECT_ID/monitoring"
```

### Step 6.2: Implement Weekly Health Check

```javascript
async function weeklyNeuralHealthCheck(projectId) {
  const report = {
    check_time: new Date().toISOString(),
    project_id: projectId,
    issues_found: [],
    warnings: [],
    recommendations: []
  };

  // 1. Check agent effectiveness trends
  const learningStatus = await mcp__ruv-swarm__daa_learning_status({ detailed: true });

  for (const agent of learningStatus.agents) {
    if (agent.effectiveness < 0.6) {
      report.issues_found.push({
        type: "low_effectiveness",
        agent: agent.id,
        value: agent.effectiveness,
        action: "Review cognitive pattern assignment"
      });
    }
  }

  // 2. Check pattern staleness
  const expiryCheck = await execSync(
    `node docs2/neural-pattern-expiry-checker.js`
  ).toString();

  report.pattern_expiry_results = expiryCheck;

  // 3. Check knowledge flow success rate
  const knowledgeLogs = await npx claude-flow memory retrieve --key `projects/${projectId}/knowledge-logs/*`;
  const successCount = knowledgeLogs.filter(l => l.includes('success')).length;
  const totalCount = Object.keys(knowledgeLogs).length;
  const successRate = totalCount > 0 ? successCount / totalCount : 0;

  if (successRate < 0.75) {
    report.warnings.push({
      type: "knowledge_flow_degradation",
      success_rate: successRate,
      recommendation: "Review knowledge sharing configurations"
    });
  }

  // 4. Check resource usage
  const resourceMetrics = await mcp__ruv-swarm__memory_usage({ detail: "detailed" });

  if (resourceMetrics.usage_percent > 80) {
    report.warnings.push({
      type: "high_resource_usage",
      usage: resourceMetrics.usage_percent,
      recommendation: "Cleanup old projects or scale resources"
    });
  }

  // 5. Store health check report
  await npx claude-flow memory store `health-check-${Date.now()}` JSON.stringify(report) --namespace `projects/${projectId}/health-checks`;

  console.log("\n📊 Weekly Neural Health Check Report:");
  console.log(`   Issues found: ${report.issues_found.length}`);
  console.log(`   Warnings: ${report.warnings.length}`);
  console.log(`   Knowledge flow success rate: ${(successRate * 100).toFixed(1)}%`);

  return report;
}
```

---

## SUCCESS CRITERIA

Before marking this implementation complete, verify:

### Knowledge Sharing
- [ ] **Project ID used in all knowledge shares**
- [ ] PhD research knowledge flows configured (7+ sharing rules) **with retry logic**
- [ ] Business research knowledge flows configured (5+ sharing rules) **with retry logic**
- [ ] Business strategy knowledge flows configured (5+ sharing rules) **with retry logic**
- [ ] QA agent mesh network configured
- [ ] **Knowledge sharing error logs** empty or minimal (<5% failure rate)

### Pattern Storage
- [ ] Pattern namespace structure created **with project isolation**
- [ ] PhD success pattern template stored **with expiry dates**
- [ ] Business research success pattern template stored **with expiry dates**
- [ ] Pattern recording workflow created **with expiry checking**
- [ ] Industry-specific patterns stored (tech, healthcare, finserv) **with expiry dates**
- [ ] **Pattern expiry checker script** (`neural-pattern-expiry-checker.js`) created
- [ ] **Weekly pattern cleanup** scheduled (cron/task scheduler)
- [ ] **Pattern archive namespace** created and verified

### Meta-Learning
- [ ] Cross-domain transfer rules configured (4+ rules) **with safety validation**
- [ ] **Transfer compatibility matrix** defined and enforced
- [ ] **Unsafe transfer warnings** logged
- [ ] Pattern-informed research start workflow created **with project isolation**
- [ ] Learning rate adjustment rules stored
- [ ] **Degradation alert system** configured

### Continuous Improvement
- [ ] Post-research hook configured
- [ ] Quality thresholds defined
- [ ] Feedback loop for agent adaptation documented

### Verification
- [ ] Knowledge flow test passed **with retry verification**
- [ ] Pattern retrieval test passed **with expiry check**
- [ ] All memory stores verified **with project isolation**
- [ ] **Weekly health check** executed successfully
- [ ] **Pattern expiry checker** run without errors
- [ ] **No cross-project contamination** detected
- [ ] **Transfer safety validator** tested

---

## USAGE INSTRUCTIONS

### Starting a New Research Project

1. Execute pattern-informed research start workflow
2. Verify agents have retrieved relevant patterns
3. Confirm cognitive patterns are appropriate for domain
4. Begin research workflow

### After Research Completion

1. Execute post-research hook actions
2. Record success/failure patterns
3. Update agent learning via daa_agent_adapt
4. Configure meta-learning for future transfers

### Periodic Maintenance (Weekly)

1. Review daa_performance_metrics
2. Check quality threshold breaches
3. Adjust learning rates per rules
4. Update industry pattern libraries with new learnings

---

## TROUBLESHOOTING

### Knowledge sharing not working
**Root Cause**: Agent doesn't exist, memory disabled, or network timeout
**Solution**:
1. Verify source agent exists: `agent_list({ filter: "all" })` and ID includes PROJECT_ID
2. Ensure enableMemory: true in agent config
3. Check retry logic executed (review knowledge-logs namespace)
4. Increase retry attempts in `shareKnowledgeWithRetry()`

### Pattern retrieval returns empty
**Root Cause**: Namespace typo, pattern expired, or project isolation mismatch
**Solution**:
1. Verify namespace path includes PROJECT_ID: `projects/$PROJECT_ID/knowledge/...`
2. Check if pattern expired: Run `node docs2/neural-pattern-expiry-checker.js`
3. Look in archive: `patterns/archived/<type>/*`
4. List all namespaces: `npx claude-flow memory retrieve --key "projects/$PROJECT_ID/*"`

### Agent not adapting
**Root Cause**: Learning disabled, low learning rate, or insufficient feedback
**Solution**:
1. Verify enableMemory: true and learningRate > 0.05
2. Check learning status: `daa_learning_status({ agentId: "<id>", detailed: true })`
3. Increase learning rate: `daa_agent_adapt({ agentId: "<id>", learningRate: 0.12 })`
4. Provide explicit feedback via `daa_agent_adapt()`

### Meta-learning transfer failing
**Root Cause**: Unsafe transfer blocked, no source patterns, or compatibility mismatch
**Solution**:
1. Check transfer compatibility matrix in `validateMetaLearningTransfer()`
2. Review warnings: `npx claude-flow memory retrieve --key "projects/$PROJECT_ID/warnings/*"`
3. Use transferMode: "gradual" for questionable transfers
4. Verify source patterns exist and not expired

### Patterns becoming stale
**Root Cause**: Expiry checker not run regularly
**Solution**:
1. Run manually: `node docs2/neural-pattern-expiry-checker.js`
2. Schedule weekly cron job: `0 0 * * 0 node /path/to/neural-pattern-expiry-checker.js`
3. Check archived patterns: `patterns/archived/<type>/*`

### Performance degrading over time
**Root Cause**: Resource accumulation, stale patterns, or agent fatigue
**Solution**:
1. Run weekly health check: `weeklyNeuralHealthCheck(PROJECT_ID)`
2. Review health check reports: `projects/$PROJECT_ID/health-checks/*`
3. Cleanup old projects: Execute cleanup procedures from immediate prompt
4. Reset learning rates to baseline values

### Cross-project contamination detected
**Root Cause**: Agent IDs missing PROJECT_ID or knowledge sharing to wrong project
**Solution**:
1. Run isolation check from immediate prompt Step 3.5.3
2. Cleanup contaminated agents
3. Verify all knowledge shares include `project_id: PROJECT_ID` in content
4. Review active projects: `config/neural/active-projects`

---

## NEXT STEPS

After completing this prompt:

1. Run a pilot research project using the new configuration
2. Execute the post-research hook to capture patterns
3. Review agent performance metrics
4. Iterate on cognitive pattern assignments based on results
5. Build industry-specific pattern libraries as you complete more research
