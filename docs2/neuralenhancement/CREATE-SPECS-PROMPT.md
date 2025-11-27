# Complete Specification Generation Prompt for Neural Enhancement System

**Purpose**: Generate comprehensive, machine-executable specifications for the Neural Enhancement System following the PRD-to-Spec conversion methodology.

---

## CONTEXT FOR AI AGENT

You are a specification architect tasked with creating a complete specification package for a **Neural Enhancement System for AI Agent Swarms**. This system enables AI research agents to learn from experience, share knowledge, and improve performance over time through cognitive patterns, meta-learning, and pattern storage.

---

## INPUT DOCUMENTS TO READ

**CRITICAL**: Read these files in this exact order before generating specifications:

1. **Methodology Blueprint**:
   - `/home/cabdru/claudeflowblueprint/docs2/prdtospec.md`
   - This defines the exact structure, formatting, and requirements for all specifications

2. **Neural Enhancement PRDs** (Implementation Guides):
   - `/home/cabdru/claudeflowblueprint/docs2/neuralenhancement/neural-enhancement-immediate.md`
   - `/home/cabdru/claudeflowblueprint/docs2/neuralenhancement/neural-enhancement-short-term.md`
   - `/home/cabdru/claudeflowblueprint/docs2/neuralenhancement/NEURAL-ENHANCEMENT-FIXES-SUMMARY.md`

3. **Supporting Artifact**:
   - `/home/cabdru/claudeflowblueprint/docs2/neuralenhancement/neural-pattern-expiry-checker.js`

---

## YOUR TASK

Create a **complete specification directory structure** in:
```
/home/cabdru/claudeflowblueprint/docs2/neuralenhancement/specs/
```

Following the exact structure from `prdtospec.md`, generate these files:

### 1. PROJECT CONSTITUTION (Level 1)
**File**: `specs/constitution.md`

**Must Include**:
- Project metadata (Neural Enhancement System v1.0)
- Tech stack:
  - Runtime: Node.js with ruv-swarm (v1.0.20+), claude-flow (v2.7.31+)
  - MCP Tools: ruv-swarm, claude-flow@alpha, flow-nexus
  - Memory: AgentDB/ReasoningBank with SQLite persistence
  - Language: JavaScript/TypeScript
- Directory structure (from actual project)
- Coding standards:
  - Agent ID format: `{agent-name}-{PROJECT_ID}`
  - Namespace format: `projects/{PROJECT_ID}/{domain}/{key}`
  - Memory key format: `{namespace}/{key}`
  - Error handling: Retry logic with exponential backoff
  - Batch operations: 5-10 items max per batch
- Anti-patterns:
  - NEVER create all 35 agents at once
  - NEVER skip project ID isolation
  - NEVER skip baseline metric capture
  - NEVER use agent IDs without project scope
  - NEVER share knowledge without retry logic
  - NEVER create patterns without expiry dates
- Security requirements:
  - SEC-01: Project isolation mandatory (unique PROJECT_ID)
  - SEC-02: Memory namespaces must include project_id
  - SEC-03: Agent IDs must be globally unique
  - SEC-04: Cross-domain transfers require safety validation
- Performance budgets:
  - Agent creation: <5s per agent
  - Knowledge sharing: <2s per share
  - Pattern retrieval: <1s
  - Baseline metrics: <30s total
  - Memory operations: <500ms
- Testing requirements:
  - Unit tests for all core functions
  - Integration tests for MCP tool chains
  - E2E tests for full workflows (immediate + short-term)
  - Rollback procedures tested
  - Pattern expiry checker tested

---

### 2. FUNCTIONAL SPECIFICATIONS (Level 2)

Create directory: `specs/functional/`

#### A. `specs/functional/_index.md`
Manifest of all functional specs with:
- Spec ID, title, status, dependencies
- User journey map (which specs cover which journeys)
- Requirement traceability matrix

#### B. `specs/functional/daa-initialization.md`
**Domain**: Decentralized Autonomous Agent initialization

**Extract from**: neural-enhancement-immediate.md Phase 1

**Must Include**:
- User Stories:
  - US-DAA-01: As a system operator, I want to initialize DAA service so agents can learn
  - US-DAA-02: As a system operator, I want to initialize swarm topology for agent coordination
  - US-DAA-03: As a system operator, I want to verify DAA features are active
- Requirements:
  - REQ-DAA-01: DAA must initialize with autonomousLearning: true
  - REQ-DAA-02: Swarm must support hierarchical topology for research workflows
  - REQ-DAA-03: Maximum 20 agents per swarm (configurable)
  - REQ-DAA-04: Cognitive patterns must include all 6 types (convergent, divergent, lateral, systems, critical, adaptive)
  - REQ-DAA-05: Error recovery checkpoint must be created before initialization
- Edge Cases:
  - EC-DAA-01: DAA init fails → retry once, then abort with error log
  - EC-DAA-02: Swarm init fails → rollback to checkpoint
  - EC-DAA-03: Features missing cognitive_diversity → reinitialize with correct config
- Acceptance Criteria (Given/When/Then for each user story)

#### C. `specs/functional/agent-lifecycle.md`
**Domain**: Agent creation, management, and cleanup

**Extract from**: neural-enhancement-immediate.md Phase 2, Phase 3.5

**Must Include**:
- User Stories:
  - US-AGENT-01: As a research coordinator, I want to create agents in batches to prevent resource exhaustion
  - US-AGENT-02: As a research coordinator, I want to assign cognitive patterns to agents for optimal performance
  - US-AGENT-03: As a system operator, I want to cleanup agents after project completion to free resources
  - US-AGENT-04: As a system operator, I want to rollback failed agent creation to maintain system integrity
- Requirements:
  - REQ-AGENT-01: Agents must be created in batches of 5-10
  - REQ-AGENT-02: Agent IDs must include PROJECT_ID for isolation
  - REQ-AGENT-03: Batch failure rate >50% must trigger automatic rollback
  - REQ-AGENT-04: Each agent must have enableMemory: true
  - REQ-AGENT-05: Learning rates must be 0.08-0.15 based on agent type
  - REQ-AGENT-06: Agent metadata must include projectId, batch number, creation timestamp
  - REQ-AGENT-07: Cleanup must store deletion record before removing agents
  - REQ-AGENT-08: Swarm destruction when no active agents remain
  - REQ-AGENT-09: 35 total agents across 3 categories (PhD: 17, Business Research: 9, Business Strategy: 9)
- Edge Cases:
  - EC-AGENT-01: Agent creation fails mid-batch → log failure, continue with remaining
  - EC-AGENT-02: Agent already exists → skip creation, log warning
  - EC-AGENT-03: Invalid cognitive pattern → reject with clear error message
  - EC-AGENT-04: Cleanup fails for one agent → continue cleanup, log failure
- Non-Functional Requirements:
  - NFR-AGENT-01: Agent creation must complete <5s per agent
  - NFR-AGENT-02: Batch creation must have 5s delay between batches
  - NFR-AGENT-03: Agent isolation check must detect 100% of contamination

#### D. `specs/functional/knowledge-sharing.md`
**Domain**: Knowledge flow between agents

**Extract from**: neural-enhancement-short-term.md Phase 1

**Must Include**:
- User Stories:
  - US-KNOW-01: As a PhD research agent, I want to share findings with downstream agents for workflow continuity
  - US-KNOW-02: As a QA agent, I want to share quality concerns with peer reviewers in real-time
  - US-KNOW-03: As a system operator, I want knowledge sharing to retry on failure for reliability
- Requirements:
  - REQ-KNOW-01: Knowledge sharing must support 3 patterns (sequential, broadcast, mesh)
  - REQ-KNOW-02: All knowledge must be scoped to project_id namespace
  - REQ-KNOW-03: Knowledge sharing must retry up to 3 times with exponential backoff
  - REQ-KNOW-04: Success/failure logs must be stored for monitoring
  - REQ-KNOW-05: Knowledge content must include expiry dates
  - REQ-KNOW-06: 17+ knowledge sharing flows for PhD research workflow
  - REQ-KNOW-07: 5+ knowledge sharing flows for business research workflow
  - REQ-KNOW-08: 5+ knowledge sharing flows for business strategy workflow
- Edge Cases:
  - EC-KNOW-01: Source agent doesn't exist → fail with clear error
  - EC-KNOW-02: Target agent doesn't exist → log warning, continue to other targets
  - EC-KNOW-03: Network timeout on share → retry with backoff
  - EC-KNOW-04: Knowledge namespace collision → fail with namespace error
- Non-Functional Requirements:
  - NFR-KNOW-01: Knowledge sharing success rate must be >95%
  - NFR-KNOW-02: Share operation must complete <2s
  - NFR-KNOW-03: Retry backoff: 1s, 2s, 4s

#### E. `specs/functional/pattern-management.md`
**Domain**: Pattern storage, retrieval, and expiry

**Extract from**: neural-enhancement-short-term.md Phase 2

**Must Include**:
- User Stories:
  - US-PATTERN-01: As a meta-learning orchestrator, I want to store successful research patterns for future reuse
  - US-PATTERN-02: As a system operator, I want patterns to expire automatically to prevent stale knowledge
  - US-PATTERN-03: As a research agent, I want to retrieve relevant patterns before starting new research
- Requirements:
  - REQ-PATTERN-01: Pattern templates must include creation and expiry dates
  - REQ-PATTERN-02: Expiry rules: PhD=180d, Business Research=90d, Business Strategy=60d, Industry=120d
  - REQ-PATTERN-03: Expired patterns must be archived, not deleted
  - REQ-PATTERN-04: Pattern recording workflow must check for expired patterns before storing new ones
  - REQ-PATTERN-05: Pattern namespaces: patterns/{type}/successful, patterns/archived/{type}
  - REQ-PATTERN-06: Pattern expiry checker must run weekly via cron
  - REQ-PATTERN-07: Patterns must include: research_id, project_id, quality_score, agent_performance, lessons_learned
- Edge Cases:
  - EC-PATTERN-01: Pattern without creation date → log warning, skip expiry check
  - EC-PATTERN-02: Archive operation fails → retry, then log failure without deleting source
  - EC-PATTERN-03: Multiple patterns expire simultaneously → batch archive operation
- Non-Functional Requirements:
  - NFR-PATTERN-01: Pattern retrieval must complete <1s
  - NFR-PATTERN-02: Expiry checker must process 100+ patterns <30s
  - NFR-PATTERN-03: Archive storage must preserve all pattern metadata

#### F. `specs/functional/meta-learning.md`
**Domain**: Cross-domain knowledge transfer

**Extract from**: neural-enhancement-short-term.md Phase 3

**Must Include**:
- User Stories:
  - US-META-01: As a meta-learning orchestrator, I want to transfer PhD patterns to business research for efficiency
  - US-META-02: As a system operator, I want unsafe transfers blocked to prevent knowledge contamination
  - US-META-03: As a research agent, I want to adapt learning rate based on performance feedback
- Requirements:
  - REQ-META-01: Transfer compatibility matrix must define valid source→target mappings
  - REQ-META-02: Unsafe transfers must be blocked unless transferMode="gradual"
  - REQ-META-03: Transfer warnings must be logged for auditing
  - REQ-META-04: Learning rate adjustment rules: high performance (>0.9) → increase by 0.02, decline (>0.1 drop) → decrease by 0.02
  - REQ-META-05: Agent adaptation must accept performanceScore (0-1), feedback message, suggestions array
  - REQ-META-06: Meta-learning must support 3 transfer modes: adaptive, gradual, direct
- Edge Cases:
  - EC-META-01: Transfer healthcare patterns to fintech → blocked, logged as UNSAFE_TRANSFER
  - EC-META-02: No source patterns exist → fail with clear error
  - EC-META-03: Learning rate adjustment exceeds bounds (0.05-0.2) → clamp to valid range
- Non-Functional Requirements:
  - NFR-META-01: Transfer validation must complete <500ms
  - NFR-META-02: Learning rate convergence within 5 adaptation cycles

#### G. `specs/functional/monitoring.md`
**Domain**: Performance monitoring and degradation detection

**Extract from**: neural-enhancement-immediate.md Resource Monitoring, neural-enhancement-short-term.md Phase 6

**Must Include**:
- User Stories:
  - US-MONITOR-01: As a system operator, I want to capture baseline metrics before neural enhancement for comparison
  - US-MONITOR-02: As a system operator, I want weekly health checks to detect performance degradation
  - US-MONITOR-03: As a system operator, I want automatic alerts when thresholds are breached
- Requirements:
  - REQ-MONITOR-01: Baseline metrics must be captured before any agent creation
  - REQ-MONITOR-02: Warning thresholds: memory >80%, agent effectiveness <0.6, response time >5s, learning rate drift >0.05
  - REQ-MONITOR-03: Weekly health check must verify: agent effectiveness, pattern expiry, knowledge flow success rate, resource usage
  - REQ-MONITOR-04: Health check reports must be stored with timestamp and recommendations
  - REQ-MONITOR-05: Degradation detection for: agent_effectiveness_drop (0.15), knowledge_flow_failure_rate (0.25), pattern_reuse_success_rate (0.70)
- Edge Cases:
  - EC-MONITOR-01: Baseline capture fails → abort implementation, do not proceed
  - EC-MONITOR-02: Health check detects multiple critical issues → generate consolidated alert
  - EC-MONITOR-03: Resource usage >100% → emergency cleanup triggered
- Non-Functional Requirements:
  - NFR-MONITOR-01: Baseline capture must complete <30s
  - NFR-MONITOR-02: Health check must complete <5 minutes
  - NFR-MONITOR-03: Monitoring overhead must be <2% system resources

---

### 3. TECHNICAL SPECIFICATIONS (Level 3)

Create directory: `specs/technical/`

#### A. `specs/technical/_index.md`
Manifest of all technical specs

#### B. `specs/technical/architecture.md`
**Must Include**:
- System architecture diagram (Mermaid)
- Component diagram showing:
  - DAA Service (initialization, coordination)
  - Agent Manager (lifecycle, batching)
  - Knowledge Sharing Service (retry logic, namespace routing)
  - Pattern Storage (expiry, archival)
  - Meta-Learning Engine (transfer validation, adaptation)
  - Monitoring Service (metrics, health checks)
- Data flow diagrams for:
  - Agent creation workflow (with rollback)
  - Knowledge sharing workflow (with retry)
  - Pattern recording workflow (with expiry check)
- Technology decisions:
  - Why ruv-swarm: No-timeout MCP tools, pooled persistence
  - Why hierarchical topology: Natural research coordinator→specialist structure
  - Why SQLite memory: Fast, embedded, ACID-compliant
  - Why exponential backoff: Industry standard retry pattern

#### C. `specs/technical/data-models.md`
**Must Include**:
- Agent Model:
  ```typescript
  interface Agent {
    id: string; // Format: {name}-{PROJECT_ID}
    capabilities: string[];
    cognitivePattern: 'convergent' | 'divergent' | 'lateral' | 'systems' | 'critical' | 'adaptive';
    enableMemory: boolean;
    learningRate: number; // 0.08-0.15
    metadata: {
      projectId: string;
      batch: number;
      created: ISO8601;
    }
  }
  ```

- Knowledge Content Model:
  ```typescript
  interface KnowledgeContent {
    description: string;
    includes: string[];
    format: 'structured-json';
    retrieval_key: string; // Format: projects/{PROJECT_ID}/knowledge/{domain}
    project_id: string;
    created_at: ISO8601;
    expires_at: ISO8601;
  }
  ```

- Pattern Model:
  ```typescript
  interface Pattern {
    pattern_type: 'phd-research-success' | 'business-research-success' | 'business-strategy-success';
    version: string;
    research_id: string;
    project_id: string;
    created_at: ISO8601;
    expires_at: ISO8601;
    archived: boolean;
    quality_score: number; // 0-100
    agent_performance: Record<string, AgentPerformance>;
    lessons_learned: string[];
    reusable_components: Record<string, string>;
  }
  ```

- Project Metadata Model:
  ```typescript
  interface ProjectMetadata {
    project_id: string;
    created_at: ISO8601;
    status: 'initializing' | 'active' | 'completed' | 'failed-rolled-back' | 'cleaned-up';
    agent_count: number;
    phase: string;
  }
  ```

#### D. `specs/technical/api-contracts.md`
**Must Include**:
- MCP Tool Contracts (all ruv-swarm tools used):
  - `mcp__ruv-swarm__daa_init(config)`
  - `mcp__ruv-swarm__swarm_init(config)`
  - `mcp__ruv-swarm__daa_agent_create(agentConfig)`
  - `mcp__ruv-swarm__agent_list(filter)`
  - `mcp__ruv-swarm__daa_knowledge_share(shareConfig)`
  - `mcp__ruv-swarm__daa_learning_status(options)`
  - `mcp__ruv-swarm__daa_meta_learning(transferConfig)`
  - `mcp__ruv-swarm__daa_agent_adapt(adaptConfig)`
  - `mcp__ruv-swarm__daa_performance_metrics(options)`
  - `mcp__ruv-swarm__memory_usage(options)`
  - `mcp__ruv-swarm__benchmark_run(options)`
  - `mcp__ruv-swarm__swarm_destroy(options)`

- Memory Storage API (claude-flow):
  - `npx claude-flow memory store {key} {json} --namespace {ns}`
  - `npx claude-flow memory retrieve --key {ns}/{key}`
  - `npx claude-flow memory delete --key {ns}/{key}`

- Function Signatures:
  ```typescript
  async function shareKnowledgeWithRetry(
    config: KnowledgeShareConfig,
    maxRetries: number = 3
  ): Promise<ShareResult>

  async function cleanupProject(projectId: string): Promise<CleanupResult>

  async function validateMetaLearningTransfer(
    config: MetaLearningConfig
  ): Promise<boolean>

  async function weeklyNeuralHealthCheck(
    projectId: string
  ): Promise<HealthReport>
  ```

#### E. `specs/technical/error-recovery.md`
**Must Include**:
- Rollback Procedure:
  1. Stop all operations
  2. List created agents
  3. Store failure state to `projects/{PROJECT_ID}/rollback`
  4. Execute cleanupProject(PROJECT_ID)
  5. Mark project status as "failed-rolled-back"
- Retry Strategies:
  - Knowledge sharing: 3 attempts, exponential backoff (1s, 2s, 4s)
  - Agent creation: Single batch failure allowed, >50% triggers rollback
  - Pattern archival: 2 attempts, log failure if both fail
- Error Logging:
  - All errors logged to `projects/{PROJECT_ID}/errors/`
  - Include: timestamp, phase, error message, action taken
- Recovery Checkpoints:
  - Pre-implementation: Before DAA init
  - Post-DAA-init: After successful DAA initialization
  - Per-batch: After each successful batch creation

#### F. `specs/technical/performance-requirements.md`
**Must Include**:
- Performance Budgets:
  - Agent creation: <5s per agent, 5s delay between batches
  - Knowledge sharing: <2s per share, <5% failure rate
  - Pattern retrieval: <1s
  - Baseline metrics capture: <30s
  - Weekly health check: <5 minutes
  - Pattern expiry checker: <30s for 100+ patterns
- Resource Limits:
  - Memory usage: <70% sustained, <80% peak
  - Agent count: Max 20 per swarm (configurable to 100)
  - Batch size: 5-10 agents
  - Knowledge domains: 10-15 per project
  - Pattern storage: Unlimited with automatic archival
- Scalability Targets:
  - Support 10+ concurrent projects
  - 1000+ patterns in active storage
  - 100+ agents across all projects
  - 50+ knowledge shares per minute

---

### 4. TASK SPECIFICATIONS (Level 4)

Create directory: `specs/tasks/`

Generate atomic task specs for each phase:

#### A. `specs/tasks/_index.md`
Manifest of all tasks with dependencies

#### B. `specs/tasks/TASK-001-baseline-capture.md`
**Title**: Capture Baseline Performance Metrics
**Prerequisites**: None
**Inputs**: None
**Outputs**: Baseline metrics stored in `projects/{PROJECT_ID}/baselines/baseline-metrics`
**Steps**: (Extract from Phase 0.2)
**Success Criteria**: Metrics captured and stored successfully
**Rollback**: N/A (no state changes)

#### C. `specs/tasks/TASK-002-daa-init.md`
**Title**: Initialize DAA Service
**Prerequisites**: TASK-001
**Dependencies**: REQ-DAA-01, REQ-DAA-04
**Steps**: (Extract from Phase 1.1)
**Rollback**: Clear DAA state if init fails

#### D. `specs/tasks/TASK-003-swarm-init.md`
**Title**: Initialize Swarm with Hierarchical Topology
**Prerequisites**: TASK-002
**Dependencies**: REQ-DAA-02, REQ-DAA-03
**Steps**: (Extract from Phase 1.2)

(Continue for all 30+ tasks across both implementation guides)

---

### 5. CONTEXT FILES (Level 5)

Create directory: `specs/context/`

#### A. `specs/context/activeContext.md`
Template for tracking current session state:
- Current phase
- Last completed task
- Active agents
- Known issues
- Next steps

#### B. `specs/context/decisionLog.md`
Template for architectural decisions:
- Decision ID
- Date
- Context
- Options considered
- Decision made
- Rationale
- Consequences

#### C. `specs/context/progress.md`
Template for roadmap tracking:
- Immediate implementation: % complete
- Short-term implementation: % complete
- Tasks completed
- Tasks remaining
- Blockers

---

## SPECIFICATION QUALITY CHECKLIST

Before finalizing, verify each spec has:

- ✅ Unique requirement IDs (REQ-DOMAIN-##)
- ✅ Traceability to source documents
- ✅ Given/When/Then acceptance criteria
- ✅ Edge cases identified
- ✅ Non-functional requirements (NFRs)
- ✅ Error states defined
- ✅ Rollback procedures
- ✅ Performance metrics
- ✅ Machine-parseable structure (XML or structured Markdown)
- ✅ Self-contained (no external context needed)
- ✅ Testable acceptance criteria
- ✅ Clear success criteria

---

## OUTPUT FORMAT

For each specification file, use this structure:

```xml
<specification id="SPEC-XXX" version="1.0">

<metadata>
  <title>Specification Title</title>
  <status>draft|approved</status>
  <owner>Neural Enhancement System Team</owner>
  <last_updated>YYYY-MM-DD</last_updated>
  <related_specs>
    <spec_ref>SPEC-YYY</spec_ref>
  </related_specs>
</metadata>

<overview>
Concise description of what this spec covers and why it exists.
</overview>

<user_stories>
  <story id="US-XXX-##" priority="must-have|should-have|could-have">
    <narrative>As a [user], I want to [action] so that [benefit]</narrative>
    <acceptance_criteria>
      <criterion id="AC-##">
        <given>Context</given>
        <when>Action</when>
        <then>Expected outcome</then>
      </criterion>
    </acceptance_criteria>
  </story>
</user_stories>

<requirements>
  <requirement id="REQ-XXX-##" story_ref="US-XXX-##" priority="must|should|could">
    <description>Clear, testable requirement</description>
    <rationale>Why this requirement exists</rationale>
    <source>Reference to source document section</source>
  </requirement>
</requirements>

<edge_cases>
  <edge_case id="EC-XXX-##" req_ref="REQ-XXX-##">
    <scenario>Description of edge case</scenario>
    <expected_behavior>How system should behave</expected_behavior>
  </edge_case>
</edge_cases>

<non_functional_requirements>
  <nfr id="NFR-XXX-##" category="performance|security|reliability|usability">
    <requirement>Measurable NFR</requirement>
    <metric>How to measure</metric>
    <target>Target value</target>
  </nfr>
</non_functional_requirements>

</specification>
```

---

## CRITICAL INSTRUCTIONS FOR AI AGENT

1. **Read all input documents completely** before starting
2. **Extract every requirement** from neural enhancement docs
3. **Create unique IDs** for all requirements (REQ-XXX-##)
4. **Map requirements to user stories** (who benefits)
5. **Identify all edge cases** mentioned or implied
6. **Generate complete file contents** for each spec file
7. **Use XML structure** for machine parseability
8. **Maintain traceability** from code → requirement → source document
9. **Create all directories** as specified
10. **Follow exact naming conventions** from prdtospec.md

---

## SUCCESS CRITERIA FOR COMPLETION

Your task is complete when:

- ✅ All directories created: `specs/`, `specs/functional/`, `specs/technical/`, `specs/tasks/`, `specs/context/`
- ✅ Constitution file created with all required sections
- ✅ 7 functional specs created (one per domain)
- ✅ 6 technical specs created
- ✅ 30+ task specs created (covering all phases)
- ✅ 3 context template files created
- ✅ All _index.md manifests created
- ✅ Every requirement has unique ID
- ✅ Every requirement traces to source document
- ✅ All edge cases documented
- ✅ All NFRs identified and measurable
- ✅ All specs follow XML structure from prdtospec.md
- ✅ No placeholders or TODOs remaining

---

## EXAMPLE OUTPUT (PARTIAL)

Here's what the first file should look like:

**File**: `specs/constitution.md`

```xml
<constitution version="1.0" last_updated="2025-11-27">

<metadata>
  <project_name>Neural Enhancement System for AI Agent Swarms</project_name>
  <spec_version>1.0.0</spec_version>
  <authors>Claude Flow Blueprint Team</authors>
</metadata>

<tech_stack>
  <runtime version="18.x">Node.js</runtime>
  <mcp_tools>
    <tool version="1.0.20">ruv-swarm</tool>
    <tool version="2.7.31">claude-flow@alpha</tool>
    <tool version="latest">flow-nexus (optional)</tool>
  </mcp_tools>
  <memory>
    <system>AgentDB/ReasoningBank</system>
    <persistence>SQLite with WAL mode</persistence>
  </memory>
  <language version="ES2022">JavaScript/TypeScript</language>
</tech_stack>

<directory_structure>
docs2/neuralenhancement/
├── specs/
│   ├── constitution.md
│   ├── functional/
│   │   ├── _index.md
│   │   ├── daa-initialization.md
│   │   ├── agent-lifecycle.md
│   │   ├── knowledge-sharing.md
│   │   ├── pattern-management.md
│   │   ├── meta-learning.md
│   │   └── monitoring.md
│   ├── technical/
│   │   ├── _index.md
│   │   ├── architecture.md
│   │   ├── data-models.md
│   │   ├── api-contracts.md
│   │   ├── error-recovery.md
│   │   └── performance-requirements.md
│   ├── tasks/
│   │   ├── _index.md
│   │   ├── TASK-001-baseline-capture.md
│   │   └── ...
│   └── context/
│       ├── activeContext.md
│       ├── decisionLog.md
│       └── progress.md
├── neural-enhancement-immediate.md
├── neural-enhancement-short-term.md
├── NEURAL-ENHANCEMENT-FIXES-SUMMARY.md
└── neural-pattern-expiry-checker.js
</directory_structure>

<coding_standards>
  <naming_conventions>
    <agents>Agent ID format: {agent-name}-{PROJECT_ID}</agents>
    <namespaces>projects/{PROJECT_ID}/{domain}/{key}</namespaces>
    <memory_keys>{namespace}/{key}</memory_keys>
    <project_ids>neural-impl-YYYYMMDD-HHMMSS</project_ids>
  </naming_conventions>

  <file_organization>
    <rule>All specs in specs/ directory with appropriate subdirectory</rule>
    <rule>Implementation guides in root of neuralenhancement/</rule>
    <rule>Utility scripts in root of neuralenhancement/</rule>
  </file_organization>

  <error_handling>
    <rule>All async operations must use retry logic with exponential backoff</rule>
    <rule>Batch operations must validate >50% success rate before proceeding</rule>
    <rule>All errors must be logged to projects/{PROJECT_ID}/errors/</rule>
    <rule>Rollback procedures must be invoked on critical failures</rule>
  </error_handling>

  <batch_operations>
    <rule>Agent creation batches: 5-10 agents maximum</rule>
    <rule>5 second delay between batches to prevent resource saturation</rule>
    <rule>Batch results must be logged to projects/{PROJECT_ID}/agent-batches/</rule>
  </batch_operations>
</coding_standards>

<anti_patterns>
  <forbidden>
    <item reason="Resource Exhaustion">Do NOT create all 35 agents simultaneously; use batching</item>
    <item reason="Knowledge Contamination">Do NOT skip project ID isolation; every agent must include PROJECT_ID</item>
    <item reason="Unmeasurable Results">Do NOT skip baseline metric capture; required for comparison</item>
    <item reason="Namespace Collision">Do NOT use agent IDs without project scope; global uniqueness required</item>
    <item reason="Fragile Operations">Do NOT share knowledge without retry logic; network failures expected</item>
    <item reason="Stale Knowledge">Do NOT create patterns without expiry dates; contamination risk</item>
    <item reason="Unsafe Transfers">Do NOT allow cross-domain transfers without compatibility validation</item>
  </forbidden>
</anti_patterns>

<security_requirements>
  <rule id="SEC-01">Project isolation is mandatory; all agents must include unique PROJECT_ID</rule>
  <rule id="SEC-02">Memory namespaces must include project_id to prevent cross-project access</rule>
  <rule id="SEC-03">Agent IDs must be globally unique across all projects</rule>
  <rule id="SEC-04">Cross-domain transfers require safety validation via compatibility matrix</rule>
  <rule id="SEC-05">Pattern archives must preserve all metadata for audit trail</rule>
</security_requirements>

<performance_budgets>
  <metric name="agent_creation">Less than 5 seconds per agent</metric>
  <metric name="knowledge_sharing">Less than 2 seconds per share operation</metric>
  <metric name="pattern_retrieval">Less than 1 second</metric>
  <metric name="baseline_capture">Less than 30 seconds total</metric>
  <metric name="memory_operations">Less than 500ms</metric>
  <metric name="health_check">Less than 5 minutes for weekly check</metric>
</performance_budgets>

<testing_requirements>
  <coverage_minimum>80% line coverage for core functions</coverage_minimum>
  <required_tests>
    <test_type>Unit tests for shareKnowledgeWithRetry, cleanupProject, validateMetaLearningTransfer</test_type>
    <test_type>Integration tests for complete immediate implementation workflow</test_type>
    <test_type>Integration tests for complete short-term implementation workflow</test_type>
    <test_type>E2E test for agent creation with rollback</test_type>
    <test_type>E2E test for pattern expiry and archival</test_type>
    <test_type>Load test for 35 agent creation with batching</test_type>
  </required_tests>
</testing_requirements>

</constitution>
```

---

## BEGIN EXECUTION

Now execute this task completely. Create all specification files following the exact structure defined above.
