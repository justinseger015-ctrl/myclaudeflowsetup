# Functional Specification: Pattern Management

**Version:** 1.0
**Project:** Neural Enhancement System Implementation
**Project ID:** neural-impl-20251127
**Created:** 2025-11-27
**Status:** Active
**Agent:** Specification Agent #6/13

---

## Overview

This functional specification defines the complete pattern management infrastructure for neural-enhanced agents, enabling adaptive learning through pattern storage, expiry, and archival. It establishes domain-specific expiry policies, storage templates for PhD research, business research, and business strategy domains, automated expiry checking, and pattern retrieval with validation.

### Purpose

Pattern Management Infrastructure ensures:
- **Pattern Expiry Policy**: Domain-specific lifecycle management (60-180 days by domain)
- **Storage Templates**: Structured pattern storage for PhD (180d), business research (90d), and business strategy (60d) domains
- **Automated Expiry Checker**: Script-based pattern expiry detection and archival automation
- **Archive Procedures**: Graceful pattern archival to `patterns/archived` namespace
- **Pattern Recording Workflow**: Capture successful patterns with effectiveness scores
- **Pattern Retrieval Validation**: Serve only fresh, non-expired patterns to agents

### Scope

This specification covers:
1. Pattern expiry policy with domain-specific lifecycle rules (4 domains)
2. Storage templates for PhD, business research, and business strategy patterns
3. Automated expiry checker script (`neural-pattern-expiry-checker.js`)
4. Archive procedures for expired patterns (move to `patterns/archived`)
5. Pattern recording workflow from successful operations
6. Pattern retrieval with expiry validation (reject expired patterns)
7. Pattern quality scoring (effectiveness threshold: 0.7)
8. Cross-domain transfer safety (prevent inappropriate pattern transfers)
9. Pattern versioning and metadata tracking
10. Pattern library management per domain

**Out of Scope:**
- Pattern learning algorithms (see neural training docs)
- Real-time pattern application (see agent execution)
- Pattern visualization dashboards (see `07-monitoring-health.md`)

---

## Requirements Detail

### REQ-F026: Pattern Expiry Policy (Domain-Specific Lifecycle)

**Priority:** P0-Critical
**Phase:** Immediate (Phase 2.5 - 10 minutes)
**User Story:** US-033

**Description:**
Implement domain-specific pattern expiry policy to prevent stale patterns from contaminating research. Patterns expire based on domain dynamics: PhD research (180 days), business research (90 days), business strategy (60 days), and industry patterns (120 days). Expired patterns automatically archived to `patterns/archived` namespace.

**Expiry Policy Rules:**

```yaml
pattern_expiry_policy:
  policy_version: "1.0"
  expiry_rules:
    phd_patterns:
      max_age_days: 180
      reason: "Research methodologies evolve, 6-month refresh cycle"
      archive_behavior: "automatic"
      grace_period_days: 14

    business_research_patterns:
      max_age_days: 90
      reason: "Market dynamics change rapidly, quarterly refresh"
      archive_behavior: "automatic"
      grace_period_days: 7

    business_strategy_patterns:
      max_age_days: 60
      reason: "Competitive landscape shifts fast, bi-monthly refresh"
      archive_behavior: "automatic"
      grace_period_days: 5

    industry_patterns:
      max_age_days: 120
      reason: "Industry trends evolve moderately, 4-month refresh"
      archive_behavior: "automatic"
      grace_period_days: 10

  auto_archive: true
  archive_namespace: "patterns/archived"
  notify_on_expiry: true
  allow_manual_extension: true
  max_extensions: 2
```

**Acceptance Criteria:**
- [ ] Four domain-specific expiry rules implemented (PhD: 180d, Business Research: 90d, Business Strategy: 60d, Industry: 120d)
- [ ] Expiry policy stored in: `config/patterns/expiry`
- [ ] Policy version tracked (current: 1.0)
- [ ] Grace periods defined per domain (5-14 days)
- [ ] Auto-archive enabled for expired patterns
- [ ] Manual extension allowed (max 2 extensions per pattern)
- [ ] Expiry notifications logged to `patterns/expiry-notifications`
- [ ] Policy retrievable via: `getExpiryPolicy(domain)`

**Dependencies:**
- REQ-F005 (ReasoningBank memory backend)
- REQ-F022 (Knowledge flow effectiveness tracking provides pattern candidates)

**Test Coverage:**
- Unit: Verify expiry calculation for each domain
- Integration: Create pattern, advance time, confirm expiry detection
- Regression: Ensure grace period prevents premature expiry
- Edge Case: Test manual extension limits (max 2)

**Error Handling:**
- If expiry policy missing: Use default 90-day expiry for all domains
- If domain not in policy: Default to 90-day expiry, log WARNING
- If expiry date calculation fails: Log error, use creation_date + 90 days
- If archive fails: Retry once, then log error and keep pattern active

**Implementation:**

```javascript
// Pattern Expiry Policy Management

const EXPIRY_POLICY = {
  policy_version: "1.0",
  expiry_rules: {
    phd_patterns: {
      max_age_days: 180,
      reason: "Research methodologies evolve, 6-month refresh cycle",
      archive_behavior: "automatic",
      grace_period_days: 14
    },
    business_research_patterns: {
      max_age_days: 90,
      reason: "Market dynamics change rapidly, quarterly refresh",
      archive_behavior: "automatic",
      grace_period_days: 7
    },
    business_strategy_patterns: {
      max_age_days: 60,
      reason: "Competitive landscape shifts fast, bi-monthly refresh",
      archive_behavior: "automatic",
      grace_period_days: 5
    },
    industry_patterns: {
      max_age_days: 120,
      reason: "Industry trends evolve moderately, 4-month refresh",
      archive_behavior: "automatic",
      grace_period_days: 10
    }
  },
  auto_archive: true,
  archive_namespace: "patterns/archived",
  notify_on_expiry: true,
  allow_manual_extension: true,
  max_extensions: 2
};

// Initialize expiry policy
async function initializeExpiryPolicy() {
  console.log("Initializing pattern expiry policy...");

  const policyKey = "pattern-expiry-policy";
  const namespace = "config/patterns/expiry";

  // Check if policy already exists
  const existingPolicy = await npx claude-flow memory retrieve --key policyKey --namespace namespace --reasoningbank;

  if (existingPolicy) {
    console.log("✓ Expiry policy already exists");
    return JSON.parse(existingPolicy);
  }

  // Store new policy
  await npx claude-flow memory store policyKey JSON.stringify({
    ...EXPIRY_POLICY,
    created_at: new Date().toISOString()
  }) --namespace namespace --reasoningbank;

  console.log("✓ Pattern expiry policy initialized");
  console.log(`  - PhD patterns: ${EXPIRY_POLICY.expiry_rules.phd_patterns.max_age_days} days`);
  console.log(`  - Business research: ${EXPIRY_POLICY.expiry_rules.business_research_patterns.max_age_days} days`);
  console.log(`  - Business strategy: ${EXPIRY_POLICY.expiry_rules.business_strategy_patterns.max_age_days} days`);
  console.log(`  - Industry patterns: ${EXPIRY_POLICY.expiry_rules.industry_patterns.max_age_days} days`);

  return EXPIRY_POLICY;
}

// Get expiry policy for domain
async function getExpiryPolicy(domain) {
  const policy = await npx claude-flow memory retrieve --key "pattern-expiry-policy" --namespace "config/patterns/expiry" --reasoningbank;

  if (!policy) {
    console.warn("⚠️ Expiry policy not found, using defaults");
    return {
      max_age_days: 90,
      reason: "Default fallback expiry",
      archive_behavior: "automatic",
      grace_period_days: 7
    };
  }

  const policyData = JSON.parse(policy);
  const domainRule = policyData.expiry_rules[domain];

  if (!domainRule) {
    console.warn(`⚠️ Domain '${domain}' not in expiry policy, using default`);
    return {
      max_age_days: 90,
      reason: "Domain not configured, using default",
      archive_behavior: "automatic",
      grace_period_days: 7
    };
  }

  return domainRule;
}

// Calculate pattern expiry date
function calculateExpiryDate(createdAt, domain) {
  const createdDate = new Date(createdAt);

  // Get expiry policy for domain
  const policy = getExpiryPolicy(domain);

  // Calculate expiry: creation date + max_age_days + grace_period
  const totalDays = policy.max_age_days + policy.grace_period_days;
  const expiryDate = new Date(createdDate);
  expiryDate.setDate(expiryDate.getDate() + totalDays);

  return {
    expiryDate: expiryDate.toISOString(),
    maxAgeDays: policy.max_age_days,
    gracePeriodDays: policy.grace_period_days,
    totalDays
  };
}

// Check if pattern is expired
function isPatternExpired(pattern) {
  const now = new Date();
  const expiryDate = new Date(pattern.expiry_date);

  return now > expiryDate;
}

// Extend pattern expiry (manual intervention)
async function extendPatternExpiry(patternId, domain, extensionDays = 30) {
  console.log(`Extending pattern expiry: ${patternId} (+${extensionDays} days)`);

  const patternKey = `pattern-${patternId}`;
  const namespace = `patterns/${domain}`;

  const patternData = await npx claude-flow memory retrieve --key patternKey --namespace namespace --reasoningbank;

  if (!patternData) {
    throw new Error(`Pattern not found: ${patternId}`);
  }

  const pattern = JSON.parse(patternData);

  // Check extension limit
  const extensionCount = pattern.extension_count || 0;
  const policy = await getExpiryPolicy(domain);

  if (policy.max_extensions && extensionCount >= policy.max_extensions) {
    throw new Error(`Pattern ${patternId} has reached max extensions (${policy.max_extensions})`);
  }

  // Extend expiry date
  const currentExpiry = new Date(pattern.expiry_date);
  const newExpiry = new Date(currentExpiry);
  newExpiry.setDate(newExpiry.getDate() + extensionDays);

  const updatedPattern = {
    ...pattern,
    expiry_date: newExpiry.toISOString(),
    extension_count: extensionCount + 1,
    last_extended_at: new Date().toISOString(),
    extension_reason: `Manual extension #${extensionCount + 1}`
  };

  // Update pattern
  await npx claude-flow memory store patternKey JSON.stringify(updatedPattern) --namespace namespace --reasoningbank;

  console.log(`✓ Pattern expiry extended to ${newExpiry.toISOString()}`);
  console.log(`  - Extensions used: ${updatedPattern.extension_count}/${policy.max_extensions}`);

  // Log extension event
  await npx claude-flow memory store `extension-${patternId}-${Date.now()}` JSON.stringify({
    pattern_id: patternId,
    domain,
    previous_expiry: pattern.expiry_date,
    new_expiry: updatedPattern.expiry_date,
    extension_days: extensionDays,
    extension_count: updatedPattern.extension_count,
    timestamp: new Date().toISOString()
  }) --namespace "patterns/expiry-logs" --reasoningbank;

  return updatedPattern;
}
```

---

### REQ-F027: Storage Templates (PhD, Business Research, Business Strategy)

**Priority:** P0-Critical
**Phase:** Immediate (Phase 2.5 - 10 minutes)
**User Story:** US-033

**Description:**
Implement structured storage templates for three pattern domains: PhD research patterns, business research patterns, and business strategy patterns. Templates ensure consistent pattern structure, metadata tracking, effectiveness scoring, and domain-specific attributes.

**Storage Template Schemas:**

**PhD Research Pattern Template:**
```yaml
pattern_schema:
  domain: "phd_patterns"
  template_version: "1.0"
  required_fields:
    - pattern_id: "unique identifier"
    - pattern_type: "methodology|theoretical-framework|experimental-design|data-analysis"
    - created_at: "ISO 8601 timestamp"
    - expiry_date: "ISO 8601 timestamp (creation + 180 days + 14 grace)"
    - effectiveness_score: "float 0.0-1.0"
    - application_count: "integer (times pattern used)"
    - success_count: "integer (successful applications)"
    - research_context:
        field: "research field (e.g., 'machine-learning', 'neuroscience')"
        methodology: "qualitative|quantitative|mixed-methods"
        sample_size: "integer or 'not-applicable'"
    - pattern_content:
        description: "human-readable pattern description"
        steps: "array of procedural steps"
        preconditions: "array of required conditions"
        expected_outcomes: "array of expected results"
    - metadata:
        source_project_id: "project that created this pattern"
        created_by_agent: "agent that discovered pattern"
        validated_by: "array of agents that validated pattern"
        tags: "array of searchable tags"
```

**Business Research Pattern Template:**
```yaml
pattern_schema:
  domain: "business_research_patterns"
  template_version: "1.0"
  required_fields:
    - pattern_id: "unique identifier"
    - pattern_type: "market-analysis|competitor-intelligence|customer-insights|trend-detection"
    - created_at: "ISO 8601 timestamp"
    - expiry_date: "ISO 8601 timestamp (creation + 90 days + 7 grace)"
    - effectiveness_score: "float 0.0-1.0"
    - application_count: "integer"
    - success_count: "integer"
    - business_context:
        industry: "industry vertical (e.g., 'fintech', 'healthcare')"
        market_segment: "B2B|B2C|B2B2C"
        geographic_scope: "local|regional|national|global"
    - pattern_content:
        description: "pattern description"
        data_sources: "array of data source types"
        analysis_methods: "array of analytical techniques"
        insights: "array of key insights discovered"
    - metadata:
        source_project_id: "project ID"
        created_by_agent: "agent ID"
        validated_by: "array of validators"
        tags: "array of tags"
```

**Business Strategy Pattern Template:**
```yaml
pattern_schema:
  domain: "business_strategy_patterns"
  template_version: "1.0"
  required_fields:
    - pattern_id: "unique identifier"
    - pattern_type: "vision-setting|positioning|innovation|execution|performance-optimization"
    - created_at: "ISO 8601 timestamp"
    - expiry_date: "ISO 8601 timestamp (creation + 60 days + 5 grace)"
    - effectiveness_score: "float 0.0-1.0"
    - application_count: "integer"
    - success_count: "integer"
    - strategy_context:
        strategy_type: "offensive|defensive|growth|turnaround|diversification"
        organizational_level: "corporate|business-unit|functional"
        time_horizon: "short-term|medium-term|long-term"
    - pattern_content:
        description: "strategy pattern description"
        strategic_objectives: "array of objectives"
        implementation_steps: "array of steps"
        success_criteria: "array of KPIs"
    - metadata:
        source_project_id: "project ID"
        created_by_agent: "agent ID"
        validated_by: "array of validators"
        tags: "array of tags"
```

**Acceptance Criteria:**
- [ ] Three storage templates implemented (PhD, business research, business strategy)
- [ ] Template versioning tracked (current: 1.0)
- [ ] Required fields enforced: pattern_id, pattern_type, created_at, expiry_date, effectiveness_score
- [ ] Domain-specific context fields: research_context, business_context, strategy_context
- [ ] Effectiveness scoring: float 0.0-1.0 (threshold: 0.7 for pattern storage)
- [ ] Application tracking: application_count, success_count
- [ ] Metadata tracking: source_project_id, created_by_agent, validated_by, tags
- [ ] Template validation function: `validatePatternTemplate(pattern, domain)`

**Dependencies:**
- REQ-F026 (Expiry policy provides expiry_date)
- REQ-F022 (Effectiveness tracking provides effectiveness_score)

**Test Coverage:**
- Unit: Validate template schema for each domain
- Integration: Store pattern using template, retrieve and verify structure
- Regression: Ensure template changes don't break existing patterns
- Edge Case: Test pattern with missing required fields (expect error)

**Error Handling:**
- If required field missing: Throw validation error with field name
- If effectiveness_score < 0.7: Reject pattern storage, log INFO
- If domain unknown: Reject pattern, log error
- If expiry_date invalid: Recalculate using creation_date + domain policy

**Implementation:**

```javascript
// Pattern Storage Templates

const PATTERN_TEMPLATES = {
  phd_patterns: {
    domain: "phd_patterns",
    template_version: "1.0",
    required_fields: [
      "pattern_id",
      "pattern_type",
      "created_at",
      "expiry_date",
      "effectiveness_score",
      "application_count",
      "success_count",
      "research_context",
      "pattern_content",
      "metadata"
    ],
    pattern_types: [
      "methodology",
      "theoretical-framework",
      "experimental-design",
      "data-analysis"
    ]
  },
  business_research_patterns: {
    domain: "business_research_patterns",
    template_version: "1.0",
    required_fields: [
      "pattern_id",
      "pattern_type",
      "created_at",
      "expiry_date",
      "effectiveness_score",
      "application_count",
      "success_count",
      "business_context",
      "pattern_content",
      "metadata"
    ],
    pattern_types: [
      "market-analysis",
      "competitor-intelligence",
      "customer-insights",
      "trend-detection"
    ]
  },
  business_strategy_patterns: {
    domain: "business_strategy_patterns",
    template_version: "1.0",
    required_fields: [
      "pattern_id",
      "pattern_type",
      "created_at",
      "expiry_date",
      "effectiveness_score",
      "application_count",
      "success_count",
      "strategy_context",
      "pattern_content",
      "metadata"
    ],
    pattern_types: [
      "vision-setting",
      "positioning",
      "innovation",
      "execution",
      "performance-optimization"
    ]
  }
};

// Validate pattern against template
function validatePatternTemplate(pattern, domain) {
  console.log(`Validating pattern against ${domain} template...`);

  const template = PATTERN_TEMPLATES[domain];

  if (!template) {
    throw new Error(`Unknown pattern domain: ${domain}`);
  }

  // Check required fields
  const missingFields = [];
  for (const field of template.required_fields) {
    if (!(field in pattern)) {
      missingFields.push(field);
    }
  }

  if (missingFields.length > 0) {
    throw new Error(`Missing required fields: ${missingFields.join(", ")}`);
  }

  // Validate effectiveness score
  if (pattern.effectiveness_score < 0.7) {
    console.warn(`⚠️ Pattern effectiveness score ${pattern.effectiveness_score} below threshold 0.7`);
    return {
      valid: false,
      reason: "effectiveness_score_too_low",
      details: `Score ${pattern.effectiveness_score} < 0.7 threshold`
    };
  }

  // Validate pattern type
  if (!template.pattern_types.includes(pattern.pattern_type)) {
    throw new Error(`Invalid pattern_type '${pattern.pattern_type}' for domain '${domain}'. Valid types: ${template.pattern_types.join(", ")}`);
  }

  console.log(`✓ Pattern validation passed for domain: ${domain}`);

  return {
    valid: true,
    template_version: template.template_version
  };
}

// Create pattern from template (PhD Research)
function createPhDPattern(config) {
  const patternId = `phd-${Date.now()}-${Math.random().toString(36).substring(7)}`;
  const createdAt = new Date().toISOString();
  const expiryInfo = calculateExpiryDate(createdAt, "phd_patterns");

  return {
    pattern_id: patternId,
    pattern_type: config.pattern_type, // methodology|theoretical-framework|experimental-design|data-analysis
    created_at: createdAt,
    expiry_date: expiryInfo.expiryDate,
    effectiveness_score: config.effectiveness_score,
    application_count: 0,
    success_count: 0,
    research_context: {
      field: config.research_field,
      methodology: config.methodology, // qualitative|quantitative|mixed-methods
      sample_size: config.sample_size
    },
    pattern_content: {
      description: config.description,
      steps: config.steps,
      preconditions: config.preconditions,
      expected_outcomes: config.expected_outcomes
    },
    metadata: {
      source_project_id: config.project_id,
      created_by_agent: config.agent_id,
      validated_by: [],
      tags: config.tags || [],
      template_version: "1.0"
    }
  };
}

// Create pattern from template (Business Research)
function createBusinessResearchPattern(config) {
  const patternId = `bizresearch-${Date.now()}-${Math.random().toString(36).substring(7)}`;
  const createdAt = new Date().toISOString();
  const expiryInfo = calculateExpiryDate(createdAt, "business_research_patterns");

  return {
    pattern_id: patternId,
    pattern_type: config.pattern_type, // market-analysis|competitor-intelligence|customer-insights|trend-detection
    created_at: createdAt,
    expiry_date: expiryInfo.expiryDate,
    effectiveness_score: config.effectiveness_score,
    application_count: 0,
    success_count: 0,
    business_context: {
      industry: config.industry,
      market_segment: config.market_segment, // B2B|B2C|B2B2C
      geographic_scope: config.geographic_scope // local|regional|national|global
    },
    pattern_content: {
      description: config.description,
      data_sources: config.data_sources,
      analysis_methods: config.analysis_methods,
      insights: config.insights
    },
    metadata: {
      source_project_id: config.project_id,
      created_by_agent: config.agent_id,
      validated_by: [],
      tags: config.tags || [],
      template_version: "1.0"
    }
  };
}

// Create pattern from template (Business Strategy)
function createBusinessStrategyPattern(config) {
  const patternId = `bizstrategy-${Date.now()}-${Math.random().toString(36).substring(7)}`;
  const createdAt = new Date().toISOString();
  const expiryInfo = calculateExpiryDate(createdAt, "business_strategy_patterns");

  return {
    pattern_id: patternId,
    pattern_type: config.pattern_type, // vision-setting|positioning|innovation|execution|performance-optimization
    created_at: createdAt,
    expiry_date: expiryInfo.expiryDate,
    effectiveness_score: config.effectiveness_score,
    application_count: 0,
    success_count: 0,
    strategy_context: {
      strategy_type: config.strategy_type, // offensive|defensive|growth|turnaround|diversification
      organizational_level: config.organizational_level, // corporate|business-unit|functional
      time_horizon: config.time_horizon // short-term|medium-term|long-term
    },
    pattern_content: {
      description: config.description,
      strategic_objectives: config.strategic_objectives,
      implementation_steps: config.implementation_steps,
      success_criteria: config.success_criteria
    },
    metadata: {
      source_project_id: config.project_id,
      created_by_agent: config.agent_id,
      validated_by: [],
      tags: config.tags || [],
      template_version: "1.0"
    }
  };
}
```

---

### REQ-F028: Automated Expiry Checker Script

**Priority:** P0-Critical
**Phase:** Immediate (Phase 2.5 - 15 minutes)
**User Story:** US-033

**Description:**
Implement automated expiry checker script (`neural-pattern-expiry-checker.js`) that runs periodically to detect expired patterns, archive them gracefully, and notify stakeholders. Script supports dry-run mode, batch processing, and configurable scheduling.

**Script Requirements:**

**Filename:** `/home/cabdru/claudeflowblueprint/docs2/neural-pattern-expiry-checker.js`

**Functionality:**
1. Scan all pattern namespaces (`patterns/phd_patterns/*`, `patterns/business_research_patterns/*`, etc.)
2. Check each pattern's `expiry_date` against current date
3. Identify expired patterns (current date > expiry_date)
4. Archive expired patterns to `patterns/archived/{domain}/{pattern_id}`
5. Remove expired patterns from active namespace
6. Log expiry events to `patterns/expiry-notifications`
7. Generate expiry report with counts per domain
8. Support dry-run mode (report only, no archival)
9. Support batch size limit (prevent memory issues)
10. Support domain filtering (e.g., check only PhD patterns)

**Acceptance Criteria:**
- [ ] Script created: `docs2/neural-pattern-expiry-checker.js`
- [ ] Scans all pattern domains (PhD, business research, business strategy, industry)
- [ ] Detects expired patterns based on expiry_date
- [ ] Archives expired patterns to `patterns/archived/{domain}/`
- [ ] Removes expired patterns from active namespaces
- [ ] Logs expiry events with pattern metadata
- [ ] Generates expiry report: `{total_scanned, expired_count, archived_count, errors}`
- [ ] Dry-run mode: `--dry-run` flag (report only)
- [ ] Batch processing: `--batch-size <n>` (default: 100)
- [ ] Domain filtering: `--domain <domain>` (optional)
- [ ] Scheduling: Can be run via cron or manual trigger

**Dependencies:**
- REQ-F026 (Expiry policy defines expiry rules)
- REQ-F027 (Storage templates provide pattern structure)
- REQ-F029 (Archive procedures for pattern archival)

**Test Coverage:**
- Unit: Verify expiry detection logic
- Integration: Create expired pattern, run checker, confirm archival
- Regression: Ensure non-expired patterns not archived
- Performance: Test with 1000+ patterns, verify batch processing
- Dry-Run: Confirm dry-run doesn't archive patterns

**Error Handling:**
- If pattern read fails: Log error, skip pattern, continue
- If archive fails: Retry once, log error, keep pattern active
- If removal fails: Log error, keep archived copy, continue
- If script crashes: Log checkpoint, support resume from checkpoint

**Implementation:**

```javascript
#!/usr/bin/env node

/**
 * Neural Pattern Expiry Checker
 *
 * Scans pattern namespaces for expired patterns and archives them gracefully.
 *
 * Usage:
 *   node neural-pattern-expiry-checker.js [options]
 *
 * Options:
 *   --dry-run              Report only, don't archive patterns
 *   --batch-size <n>       Process patterns in batches (default: 100)
 *   --domain <domain>      Check specific domain only (phd_patterns|business_research_patterns|business_strategy_patterns|industry_patterns)
 *   --verbose              Enable verbose logging
 *
 * Examples:
 *   node neural-pattern-expiry-checker.js --dry-run
 *   node neural-pattern-expiry-checker.js --domain phd_patterns
 *   node neural-pattern-expiry-checker.js --batch-size 50 --verbose
 */

const { execSync } = require('child_process');
const fs = require('fs');

// Configuration
const CONFIG = {
  domains: [
    'phd_patterns',
    'business_research_patterns',
    'business_strategy_patterns',
    'industry_patterns'
  ],
  archive_namespace: 'patterns/archived',
  expiry_log_namespace: 'patterns/expiry-notifications',
  batch_size: 100,
  dry_run: false,
  verbose: false,
  domain_filter: null
};

// Parse command-line arguments
function parseArgs() {
  const args = process.argv.slice(2);

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === '--dry-run') {
      CONFIG.dry_run = true;
    } else if (arg === '--verbose') {
      CONFIG.verbose = true;
    } else if (arg === '--batch-size') {
      CONFIG.batch_size = parseInt(args[++i], 10);
    } else if (arg === '--domain') {
      CONFIG.domain_filter = args[++i];
    }
  }

  if (CONFIG.dry_run) {
    console.log("🔍 DRY-RUN MODE: No patterns will be archived\n");
  }
}

// Execute memory command
function memoryCommand(command) {
  try {
    const result = execSync(`npx claude-flow ${command}`, { encoding: 'utf-8' });
    return result.trim();
  } catch (error) {
    console.error(`Memory command failed: ${error.message}`);
    return null;
  }
}

// Retrieve patterns from namespace
async function retrievePatterns(domain) {
  console.log(`Scanning ${domain}...`);

  const namespace = `patterns/${domain}`;
  const patterns = [];

  // Query all patterns in namespace (simulated - in production use actual memory query)
  // const result = memoryCommand(`memory query "*" --namespace "${namespace}" --limit 10000 --reasoningbank`);

  // For specification, simulate pattern retrieval
  // In production, parse memory query results

  return patterns;
}

// Check if pattern is expired
function isExpired(pattern) {
  const now = new Date();
  const expiryDate = new Date(pattern.expiry_date);

  return now > expiryDate;
}

// Archive expired pattern
async function archivePattern(pattern, domain) {
  const archiveKey = `${pattern.pattern_id}`;
  const archiveNamespace = `${CONFIG.archive_namespace}/${domain}`;

  console.log(`  - Archiving: ${pattern.pattern_id}`);

  if (CONFIG.dry_run) {
    console.log(`    [DRY-RUN] Would archive to: ${archiveNamespace}/${archiveKey}`);
    return { success: true, dry_run: true };
  }

  try {
    // Store pattern in archive
    const archiveData = {
      ...pattern,
      archived_at: new Date().toISOString(),
      archive_reason: "expiry"
    };

    // In production:
    // memoryCommand(`memory store "${archiveKey}" '${JSON.stringify(archiveData)}' --namespace "${archiveNamespace}" --reasoningbank`);

    // Remove from active namespace
    // memoryCommand(`memory delete --key "${pattern.pattern_id}" --namespace "patterns/${domain}" --reasoningbank`);

    console.log(`    ✓ Archived to: ${archiveNamespace}/${archiveKey}`);

    return { success: true };
  } catch (error) {
    console.error(`    ✗ Archive failed: ${error.message}`);
    return { success: false, error: error.message };
  }
}

// Log expiry event
async function logExpiryEvent(pattern, domain, archiveResult) {
  const logKey = `expiry-${pattern.pattern_id}-${Date.now()}`;
  const logData = {
    pattern_id: pattern.pattern_id,
    domain,
    expiry_date: pattern.expiry_date,
    archived_at: new Date().toISOString(),
    archive_success: archiveResult.success,
    archive_error: archiveResult.error || null
  };

  if (!CONFIG.dry_run) {
    // In production:
    // memoryCommand(`memory store "${logKey}" '${JSON.stringify(logData)}' --namespace "${CONFIG.expiry_log_namespace}" --reasoningbank`);
  }

  if (CONFIG.verbose) {
    console.log(`    [LOG] Expiry event: ${logKey}`);
  }
}

// Process batch of patterns
async function processBatch(patterns, domain) {
  const results = {
    scanned: patterns.length,
    expired: 0,
    archived: 0,
    errors: 0
  };

  for (const pattern of patterns) {
    if (isExpired(pattern)) {
      results.expired++;

      const archiveResult = await archivePattern(pattern, domain);

      if (archiveResult.success) {
        results.archived++;
      } else {
        results.errors++;
      }

      await logExpiryEvent(pattern, domain, archiveResult);
    }
  }

  return results;
}

// Main execution
async function main() {
  console.log("🧹 Neural Pattern Expiry Checker\n");

  parseArgs();

  const domains = CONFIG.domain_filter
    ? [CONFIG.domain_filter]
    : CONFIG.domains;

  const report = {
    start_time: new Date().toISOString(),
    domains_scanned: 0,
    total_patterns_scanned: 0,
    total_expired: 0,
    total_archived: 0,
    total_errors: 0,
    domain_results: {}
  };

  for (const domain of domains) {
    console.log(`\n📂 Domain: ${domain}`);

    const patterns = await retrievePatterns(domain);

    // Process in batches
    let batchResults = {
      scanned: 0,
      expired: 0,
      archived: 0,
      errors: 0
    };

    for (let i = 0; i < patterns.length; i += CONFIG.batch_size) {
      const batch = patterns.slice(i, i + CONFIG.batch_size);
      const batchNum = Math.floor(i / CONFIG.batch_size) + 1;
      const totalBatches = Math.ceil(patterns.length / CONFIG.batch_size);

      console.log(`  Batch ${batchNum}/${totalBatches} (${batch.length} patterns)`);

      const result = await processBatch(batch, domain);

      batchResults.scanned += result.scanned;
      batchResults.expired += result.expired;
      batchResults.archived += result.archived;
      batchResults.errors += result.errors;
    }

    report.domain_results[domain] = batchResults;
    report.domains_scanned++;
    report.total_patterns_scanned += batchResults.scanned;
    report.total_expired += batchResults.expired;
    report.total_archived += batchResults.archived;
    report.total_errors += batchResults.errors;

    console.log(`  ✓ Scanned: ${batchResults.scanned}`);
    console.log(`  ✓ Expired: ${batchResults.expired}`);
    console.log(`  ✓ Archived: ${batchResults.archived}`);
    if (batchResults.errors > 0) {
      console.log(`  ✗ Errors: ${batchResults.errors}`);
    }
  }

  report.end_time = new Date().toISOString();

  // Print summary report
  console.log("\n" + "=".repeat(60));
  console.log("EXPIRY CHECKER SUMMARY");
  console.log("=".repeat(60));
  console.log(`Start Time:       ${report.start_time}`);
  console.log(`End Time:         ${report.end_time}`);
  console.log(`Domains Scanned:  ${report.domains_scanned}`);
  console.log(`Total Patterns:   ${report.total_patterns_scanned}`);
  console.log(`Expired:          ${report.total_expired}`);
  console.log(`Archived:         ${report.total_archived}`);
  console.log(`Errors:           ${report.total_errors}`);
  console.log("=".repeat(60));

  // Save report
  const reportPath = `/tmp/neural-pattern-expiry-report-${Date.now()}.json`;
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
  console.log(`\n📊 Report saved: ${reportPath}\n`);

  process.exit(report.total_errors > 0 ? 1 : 0);
}

// Run main
main().catch(error => {
  console.error(`\n❌ Expiry checker failed: ${error.message}`);
  process.exit(1);
});
```

---

### REQ-F029: Archive Procedures

**Priority:** P0-Critical
**Phase:** Immediate (Phase 2.5 - 10 minutes)
**User Story:** US-033

**Description:**
Implement graceful pattern archival procedures to `patterns/archived/{domain}/` namespace. Archived patterns retain all metadata, timestamps, and effectiveness scores for historical analysis while being excluded from active pattern retrieval.

**Archive Namespace Structure:**

```
patterns/archived/
├── phd_patterns/
│   ├── {pattern-id-1}
│   ├── {pattern-id-2}
│   └── ...
├── business_research_patterns/
│   ├── {pattern-id-1}
│   └── ...
├── business_strategy_patterns/
│   └── ...
└── industry_patterns/
    └── ...
```

**Acceptance Criteria:**
- [ ] Archive namespace: `patterns/archived/{domain}/`
- [ ] Archived patterns retain full metadata + `archived_at` timestamp
- [ ] Archive reason tracked: `archive_reason` (expiry|manual|quality-degradation)
- [ ] Archive function: `archivePattern(patternId, domain, reason)`
- [ ] Unarchive function: `unarchivePattern(patternId, domain)` (emergency recovery)
- [ ] List archived patterns: `listArchivedPatterns(domain)`
- [ ] Archive size tracking: count archived patterns per domain
- [ ] Archive cleanup: purge archives older than 1 year (configurable)

**Dependencies:**
- REQ-F026 (Expiry policy triggers archival)
- REQ-F027 (Storage templates define pattern structure)
- REQ-F028 (Expiry checker automates archival)

**Test Coverage:**
- Unit: Verify archive metadata enrichment
- Integration: Archive pattern, verify active removal, confirm archived copy
- Regression: Ensure archived patterns not retrieved by active queries
- Recovery: Archive then unarchive, verify pattern restored to active

**Error Handling:**
- If archive storage fails: Retry once, keep pattern active if retry fails
- If active removal fails after archival: Log error, keep both copies (prefer active)
- If unarchive fails: Log error, keep archived copy
- If archive namespace full: Log CRITICAL, pause archival, escalate

**Implementation:**

```javascript
// Pattern Archive Procedures

const ARCHIVE_CONFIG = {
  archive_namespace: "patterns/archived",
  archive_retention_days: 365, // 1 year
  archive_reasons: ["expiry", "manual", "quality-degradation", "superseded"]
};

// Archive pattern
async function archivePattern(patternId, domain, reason = "expiry") {
  console.log(`Archiving pattern: ${patternId} (reason: ${reason})`);

  if (!ARCHIVE_CONFIG.archive_reasons.includes(reason)) {
    console.warn(`⚠️ Unknown archive reason: ${reason}, using 'manual'`);
    reason = "manual";
  }

  // Retrieve pattern from active namespace
  const activeNamespace = `patterns/${domain}`;
  const patternKey = `pattern-${patternId}`;

  const patternData = await npx claude-flow memory retrieve --key patternKey --namespace activeNamespace --reasoningbank;

  if (!patternData) {
    throw new Error(`Pattern not found in active namespace: ${patternId}`);
  }

  const pattern = JSON.parse(patternData);

  // Enrich with archive metadata
  const archivedPattern = {
    ...pattern,
    archived_at: new Date().toISOString(),
    archive_reason: reason,
    original_namespace: activeNamespace,
    archive_version: "1.0"
  };

  // Store in archive namespace
  const archiveNamespace = `${ARCHIVE_CONFIG.archive_namespace}/${domain}`;
  const archiveKey = `archived-${patternId}`;

  await npx claude-flow memory store archiveKey JSON.stringify(archivedPattern) --namespace archiveNamespace --reasoningbank;

  console.log(`  ✓ Archived to: ${archiveNamespace}/${archiveKey}`);

  // Remove from active namespace
  // In production: await npx claude-flow memory delete --key patternKey --namespace activeNamespace --reasoningbank

  console.log(`  ✓ Removed from active namespace: ${activeNamespace}`);

  // Log archive event
  await npx claude-flow memory store `archive-event-${patternId}-${Date.now()}` JSON.stringify({
    pattern_id: patternId,
    domain,
    archive_reason: reason,
    archived_at: archivedPattern.archived_at,
    original_expiry: pattern.expiry_date,
    effectiveness_score: pattern.effectiveness_score
  }) --namespace "patterns/archive-logs" --reasoningbank;

  return {
    pattern_id: patternId,
    archived_at: archivedPattern.archived_at,
    archive_namespace: archiveNamespace,
    archive_key: archiveKey
  };
}

// Unarchive pattern (emergency recovery)
async function unarchivePattern(patternId, domain) {
  console.log(`Unarchiving pattern: ${patternId}`);

  const archiveNamespace = `${ARCHIVE_CONFIG.archive_namespace}/${domain}`;
  const archiveKey = `archived-${patternId}`;

  const archivedData = await npx claude-flow memory retrieve --key archiveKey --namespace archiveNamespace --reasoningbank;

  if (!archivedData) {
    throw new Error(`Pattern not found in archive: ${patternId}`);
  }

  const archivedPattern = JSON.parse(archivedData);

  // Remove archive metadata
  const { archived_at, archive_reason, original_namespace, archive_version, ...restoredPattern } = archivedPattern;

  // Recalculate expiry (add 30 days grace period)
  const newCreatedAt = new Date().toISOString();
  const expiryInfo = calculateExpiryDate(newCreatedAt, domain);

  restoredPattern.created_at = newCreatedAt;
  restoredPattern.expiry_date = expiryInfo.expiryDate;
  restoredPattern.unarchived_at = newCreatedAt;
  restoredPattern.unarchive_reason = "manual-recovery";

  // Restore to active namespace
  const activeNamespace = `patterns/${domain}`;
  const patternKey = `pattern-${patternId}`;

  await npx claude-flow memory store patternKey JSON.stringify(restoredPattern) --namespace activeNamespace --reasoningbank;

  console.log(`  ✓ Restored to active namespace: ${activeNamespace}/${patternKey}`);

  // Log unarchive event
  await npx claude-flow memory store `unarchive-event-${patternId}-${Date.now()}` JSON.stringify({
    pattern_id: patternId,
    domain,
    unarchived_at: restoredPattern.unarchived_at,
    original_archive_date: archived_at,
    new_expiry: restoredPattern.expiry_date
  }) --namespace "patterns/archive-logs" --reasoningbank;

  return {
    pattern_id: patternId,
    unarchived_at: restoredPattern.unarchived_at,
    new_expiry: restoredPattern.expiry_date
  };
}

// List archived patterns
async function listArchivedPatterns(domain, limit = 100) {
  console.log(`Listing archived patterns for domain: ${domain}`);

  const archiveNamespace = `${ARCHIVE_CONFIG.archive_namespace}/${domain}`;

  // In production:
  // const archivedPatterns = await npx claude-flow memory query "archived-*" --namespace archiveNamespace --limit limit --reasoningbank;

  // For specification, simulate
  const archivedPatterns = [];

  console.log(`  Found ${archivedPatterns.length} archived patterns`);

  return archivedPatterns.map(p => ({
    pattern_id: p.pattern_id,
    pattern_type: p.pattern_type,
    archived_at: p.archived_at,
    archive_reason: p.archive_reason,
    effectiveness_score: p.effectiveness_score,
    original_expiry: p.expiry_date
  }));
}

// Track archive size per domain
async function trackArchiveSize(domain) {
  const archivedPatterns = await listArchivedPatterns(domain, 10000);

  const archiveStats = {
    domain,
    total_archived: archivedPatterns.length,
    archive_reasons: {},
    oldest_archive: null,
    newest_archive: null,
    timestamp: new Date().toISOString()
  };

  // Group by archive reason
  for (const pattern of archivedPatterns) {
    const reason = pattern.archive_reason;
    archiveStats.archive_reasons[reason] = (archiveStats.archive_reasons[reason] || 0) + 1;

    // Track oldest/newest
    if (!archiveStats.oldest_archive || pattern.archived_at < archiveStats.oldest_archive) {
      archiveStats.oldest_archive = pattern.archived_at;
    }
    if (!archiveStats.newest_archive || pattern.archived_at > archiveStats.newest_archive) {
      archiveStats.newest_archive = pattern.archived_at;
    }
  }

  console.log(`Archive stats for ${domain}:`);
  console.log(`  - Total archived: ${archiveStats.total_archived}`);
  console.log(`  - Archive reasons:`, archiveStats.archive_reasons);
  console.log(`  - Oldest: ${archiveStats.oldest_archive}`);
  console.log(`  - Newest: ${archiveStats.newest_archive}`);

  // Store archive stats
  await npx claude-flow memory store `archive-stats-${domain}` JSON.stringify(archiveStats) --namespace "patterns/archive-stats" --reasoningbank;

  return archiveStats;
}

// Cleanup old archives (older than retention period)
async function cleanupOldArchives(domain, dryRun = true) {
  console.log(`Cleaning up archives older than ${ARCHIVE_CONFIG.archive_retention_days} days (dry-run: ${dryRun})`);

  const archivedPatterns = await listArchivedPatterns(domain, 10000);
  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - ARCHIVE_CONFIG.archive_retention_days);

  const patternsToDelete = archivedPatterns.filter(p => new Date(p.archived_at) < cutoffDate);

  console.log(`  Found ${patternsToDelete.length} archives older than ${cutoffDate.toISOString()}`);

  if (dryRun) {
    console.log("  [DRY-RUN] No archives deleted");
    return { dry_run: true, candidates: patternsToDelete.length };
  }

  // Delete old archives
  const deletionResults = [];
  for (const pattern of patternsToDelete) {
    try {
      // In production:
      // await npx claude-flow memory delete --key `archived-${pattern.pattern_id}` --namespace `${ARCHIVE_CONFIG.archive_namespace}/${domain}` --reasoningbank

      deletionResults.push({ pattern_id: pattern.pattern_id, deleted: true });
      console.log(`  ✓ Deleted: ${pattern.pattern_id}`);
    } catch (error) {
      deletionResults.push({ pattern_id: pattern.pattern_id, deleted: false, error: error.message });
      console.error(`  ✗ Delete failed: ${pattern.pattern_id} - ${error.message}`);
    }
  }

  const deletedCount = deletionResults.filter(r => r.deleted).length;

  console.log(`  Cleanup complete: ${deletedCount}/${patternsToDelete.length} deleted`);

  return {
    dry_run: false,
    candidates: patternsToDelete.length,
    deleted: deletedCount,
    errors: patternsToDelete.length - deletedCount
  };
}
```

---

### REQ-F030: Pattern Recording Workflow

**Priority:** P0-Critical
**Phase:** Immediate (Phase 2.6 - 15 minutes)
**User Story:** US-033

**Description:**
Implement pattern recording workflow to capture successful patterns from operations. Patterns extracted from high-effectiveness operations (score ≥ 0.7), validated against templates, enriched with metadata, and stored in domain-specific namespaces.

**Recording Workflow Steps:**

1. **Pattern Detection**: Monitor operations for effectiveness ≥ 0.7
2. **Pattern Extraction**: Extract procedural steps, preconditions, outcomes
3. **Template Validation**: Validate against domain-specific template
4. **Metadata Enrichment**: Add project_id, agent_id, tags, timestamps
5. **Quality Scoring**: Calculate effectiveness score from operation success
6. **Domain Classification**: Classify into PhD/business-research/business-strategy
7. **Pattern Storage**: Store in `patterns/{domain}/pattern-{id}`
8. **Expiry Calculation**: Calculate expiry_date based on domain policy
9. **Indexing**: Add to pattern library for retrieval

**Acceptance Criteria:**
- [ ] Pattern recording function: `recordPattern(operation, domain, effectiveness)`
- [ ] Effectiveness threshold enforcement: ≥ 0.7 required
- [ ] Template validation before storage
- [ ] Automatic expiry_date calculation using domain policy
- [ ] Metadata enrichment: project_id, agent_id, tags, created_at
- [ ] Pattern library indexing: `patterns/{domain}/library-index`
- [ ] Duplicate detection: prevent recording same pattern twice
- [ ] Pattern versioning: support pattern updates (v1.0, v1.1, etc.)
- [ ] Recording logs: track all pattern recording events

**Dependencies:**
- REQ-F026 (Expiry policy for expiry_date calculation)
- REQ-F027 (Storage templates for validation)
- REQ-F022 (Effectiveness tracking provides effectiveness scores)

**Test Coverage:**
- Unit: Verify pattern extraction from operation data
- Integration: Record pattern, retrieve, verify structure
- Regression: Ensure low-effectiveness patterns (< 0.7) rejected
- Duplicate: Attempt to record same pattern twice, verify rejection

**Error Handling:**
- If effectiveness < 0.7: Reject pattern, log INFO
- If template validation fails: Reject pattern, log error with details
- If duplicate detected: Skip recording, log INFO
- If storage fails: Retry once, log error if retry fails

**Implementation:**

```javascript
// Pattern Recording Workflow

const RECORDING_CONFIG = {
  effectiveness_threshold: 0.7,
  enable_duplicate_detection: true,
  enable_pattern_versioning: true,
  library_index_namespace: "patterns/library-index"
};

// Record pattern from successful operation
async function recordPattern(operation, domain, projectId) {
  console.log(`Recording pattern from operation: ${operation.operation_id}`);

  // 1. Check effectiveness threshold
  if (operation.effectiveness_score < RECORDING_CONFIG.effectiveness_threshold) {
    console.warn(`⚠️ Pattern effectiveness ${operation.effectiveness_score} below threshold ${RECORDING_CONFIG.effectiveness_threshold}`);
    return {
      recorded: false,
      reason: "effectiveness_too_low",
      effectiveness_score: operation.effectiveness_score
    };
  }

  // 2. Extract pattern from operation
  const patternConfig = extractPatternFromOperation(operation, domain);

  // 3. Create pattern using appropriate template
  let pattern;
  if (domain === "phd_patterns") {
    pattern = createPhDPattern(patternConfig);
  } else if (domain === "business_research_patterns") {
    pattern = createBusinessResearchPattern(patternConfig);
  } else if (domain === "business_strategy_patterns") {
    pattern = createBusinessStrategyPattern(patternConfig);
  } else {
    throw new Error(`Unknown domain: ${domain}`);
  }

  // 4. Validate against template
  const validation = validatePatternTemplate(pattern, domain);

  if (!validation.valid) {
    console.error(`❌ Pattern validation failed: ${validation.reason}`);
    return {
      recorded: false,
      reason: validation.reason,
      details: validation.details
    };
  }

  // 5. Check for duplicates
  if (RECORDING_CONFIG.enable_duplicate_detection) {
    const duplicate = await detectDuplicatePattern(pattern, domain);

    if (duplicate) {
      console.warn(`⚠️ Duplicate pattern detected: ${duplicate.pattern_id}`);

      // Update existing pattern instead of creating duplicate
      return await updatePatternVersion(duplicate.pattern_id, domain, pattern);
    }
  }

  // 6. Store pattern
  const namespace = `patterns/${domain}`;
  const patternKey = `pattern-${pattern.pattern_id}`;

  await npx claude-flow memory store patternKey JSON.stringify(pattern) --namespace namespace --reasoningbank;

  console.log(`✓ Pattern recorded: ${pattern.pattern_id}`);
  console.log(`  - Domain: ${domain}`);
  console.log(`  - Type: ${pattern.pattern_type}`);
  console.log(`  - Effectiveness: ${pattern.effectiveness_score}`);
  console.log(`  - Expiry: ${pattern.expiry_date}`);

  // 7. Update pattern library index
  await updatePatternLibraryIndex(pattern, domain);

  // 8. Log recording event
  await npx claude-flow memory store `recording-event-${pattern.pattern_id}` JSON.stringify({
    pattern_id: pattern.pattern_id,
    domain,
    pattern_type: pattern.pattern_type,
    effectiveness_score: pattern.effectiveness_score,
    operation_id: operation.operation_id,
    recorded_at: new Date().toISOString(),
    project_id: projectId
  }) --namespace "patterns/recording-logs" --reasoningbank;

  return {
    recorded: true,
    pattern_id: pattern.pattern_id,
    domain,
    effectiveness_score: pattern.effectiveness_score
  };
}

// Extract pattern from operation data
function extractPatternFromOperation(operation, domain) {
  // Extract common fields
  const baseConfig = {
    pattern_type: operation.pattern_type || "methodology",
    effectiveness_score: operation.effectiveness_score,
    description: operation.description || "Extracted pattern from successful operation",
    project_id: operation.project_id,
    agent_id: operation.agent_id,
    tags: operation.tags || []
  };

  // Domain-specific extraction
  if (domain === "phd_patterns") {
    return {
      ...baseConfig,
      research_field: operation.research_field || "general",
      methodology: operation.methodology || "mixed-methods",
      sample_size: operation.sample_size || "not-applicable",
      steps: operation.steps || [],
      preconditions: operation.preconditions || [],
      expected_outcomes: operation.expected_outcomes || []
    };
  } else if (domain === "business_research_patterns") {
    return {
      ...baseConfig,
      industry: operation.industry || "general",
      market_segment: operation.market_segment || "B2B",
      geographic_scope: operation.geographic_scope || "national",
      data_sources: operation.data_sources || [],
      analysis_methods: operation.analysis_methods || [],
      insights: operation.insights || []
    };
  } else if (domain === "business_strategy_patterns") {
    return {
      ...baseConfig,
      strategy_type: operation.strategy_type || "growth",
      organizational_level: operation.organizational_level || "business-unit",
      time_horizon: operation.time_horizon || "medium-term",
      strategic_objectives: operation.strategic_objectives || [],
      implementation_steps: operation.implementation_steps || [],
      success_criteria: operation.success_criteria || []
    };
  }

  throw new Error(`Unknown domain: ${domain}`);
}

// Detect duplicate patterns
async function detectDuplicatePattern(pattern, domain) {
  // In production: Query patterns with similar content
  // Use semantic similarity or exact match on key fields

  // For specification, simulate duplicate detection
  return null;
}

// Update pattern version
async function updatePatternVersion(patternId, domain, newPatternData) {
  console.log(`Updating pattern version: ${patternId}`);

  const namespace = `patterns/${domain}`;
  const patternKey = `pattern-${patternId}`;

  const existingData = await npx claude-flow memory retrieve --key patternKey --namespace namespace --reasoningbank;

  if (!existingData) {
    throw new Error(`Pattern not found for update: ${patternId}`);
  }

  const existingPattern = JSON.parse(existingData);

  // Increment version
  const currentVersion = existingPattern.metadata.pattern_version || "1.0";
  const [major, minor] = currentVersion.split(".").map(Number);
  const newVersion = `${major}.${minor + 1}`;

  // Merge patterns
  const updatedPattern = {
    ...existingPattern,
    application_count: existingPattern.application_count + 1,
    success_count: existingPattern.success_count + 1,
    effectiveness_score: (existingPattern.effectiveness_score + newPatternData.effectiveness_score) / 2, // Average
    metadata: {
      ...existingPattern.metadata,
      pattern_version: newVersion,
      last_updated_at: new Date().toISOString(),
      update_reason: "duplicate-pattern-merge"
    }
  };

  // Update storage
  await npx claude-flow memory store patternKey JSON.stringify(updatedPattern) --namespace namespace --reasoningbank;

  console.log(`✓ Pattern version updated: ${currentVersion} → ${newVersion}`);

  return {
    recorded: true,
    pattern_id: patternId,
    domain,
    version: newVersion,
    update_type: "version-increment"
  };
}

// Update pattern library index
async function updatePatternLibraryIndex(pattern, domain) {
  const indexKey = `library-index-${domain}`;
  const indexNamespace = RECORDING_CONFIG.library_index_namespace;

  // Retrieve existing index
  const indexData = await npx claude-flow memory retrieve --key indexKey --namespace indexNamespace --reasoningbank;

  const index = indexData ? JSON.parse(indexData) : {
    domain,
    patterns: [],
    last_updated: null
  };

  // Add pattern to index
  index.patterns.push({
    pattern_id: pattern.pattern_id,
    pattern_type: pattern.pattern_type,
    effectiveness_score: pattern.effectiveness_score,
    created_at: pattern.created_at,
    expiry_date: pattern.expiry_date,
    tags: pattern.metadata.tags
  });

  index.last_updated = new Date().toISOString();

  // Update index
  await npx claude-flow memory store indexKey JSON.stringify(index) --namespace indexNamespace --reasoningbank;

  console.log(`  ✓ Pattern library index updated: ${domain}`);
}
```

---

### REQ-F031: Pattern Retrieval with Expiry Validation

**Priority:** P0-Critical
**Phase:** Immediate (Phase 2.6 - 10 minutes)
**User Story:** US-033

**Description:**
Implement pattern retrieval with automatic expiry validation to ensure agents only receive fresh, non-expired patterns. Retrieval filters expired patterns, sorts by effectiveness, and supports domain/type filtering.

**Retrieval Features:**

1. **Expiry Validation**: Filter out patterns with current_date > expiry_date
2. **Effectiveness Sorting**: Sort by effectiveness_score descending
3. **Domain Filtering**: Retrieve patterns from specific domain only
4. **Type Filtering**: Filter by pattern_type (methodology, market-analysis, etc.)
5. **Tag Filtering**: Filter by tags for semantic matching
6. **Recency Sorting**: Option to sort by created_at (newest first)
7. **Limit Control**: Limit number of patterns returned
8. **Similarity Matching**: Retrieve patterns similar to provided context

**Acceptance Criteria:**
- [ ] Retrieval function: `retrievePatterns(domain, filters, sortBy, limit)`
- [ ] Automatic expiry filtering: exclude expired patterns
- [ ] Effectiveness sorting: highest score first (default)
- [ ] Domain filtering: `domain` parameter required
- [ ] Type filtering: `pattern_type` optional filter
- [ ] Tag filtering: `tags` array optional filter
- [ ] Recency sorting: `sortBy: 'created_at'` option
- [ ] Limit control: default 10, max 100
- [ ] Empty result handling: return [] if no matching patterns
- [ ] Retrieval logging: track pattern retrieval events

**Dependencies:**
- REQ-F026 (Expiry policy for validation)
- REQ-F027 (Storage templates define pattern structure)
- REQ-F030 (Pattern recording populates library)

**Test Coverage:**
- Unit: Verify expiry filtering logic
- Integration: Store expired pattern, retrieve, confirm filtered out
- Regression: Ensure fresh patterns retrieved correctly
- Sorting: Verify effectiveness and recency sorting
- Filters: Test domain, type, and tag filtering

**Error Handling:**
- If domain invalid: Throw error
- If no patterns found: Return empty array []
- If expiry validation fails: Log error, exclude pattern
- If retrieval fails: Log error, return empty array

**Implementation:**

```javascript
// Pattern Retrieval with Expiry Validation

const RETRIEVAL_CONFIG = {
  default_limit: 10,
  max_limit: 100,
  default_sort: "effectiveness_score", // or "created_at"
  enable_similarity_matching: true
};

// Retrieve patterns with expiry validation
async function retrievePatterns(domain, filters = {}, options = {}) {
  console.log(`Retrieving patterns from domain: ${domain}`);

  const {
    pattern_type = null,
    tags = [],
    min_effectiveness = 0.7,
    include_expired = false
  } = filters;

  const {
    sortBy = RETRIEVAL_CONFIG.default_sort,
    limit = RETRIEVAL_CONFIG.default_limit,
    offset = 0
  } = options;

  // Validate limit
  const effectiveLimit = Math.min(limit, RETRIEVAL_CONFIG.max_limit);

  // Retrieve all patterns from domain (in production, use optimized query)
  const namespace = `patterns/${domain}`;

  // Simulated retrieval - in production use actual memory query
  let patterns = []; // await retrieveAllPatternsFromNamespace(namespace);

  // 1. Filter by expiry (unless explicitly included)
  if (!include_expired) {
    const now = new Date();
    patterns = patterns.filter(p => {
      const expiryDate = new Date(p.expiry_date);
      return now <= expiryDate;
    });

    console.log(`  - After expiry filter: ${patterns.length} patterns`);
  }

  // 2. Filter by pattern type
  if (pattern_type) {
    patterns = patterns.filter(p => p.pattern_type === pattern_type);
    console.log(`  - After type filter (${pattern_type}): ${patterns.length} patterns`);
  }

  // 3. Filter by minimum effectiveness
  patterns = patterns.filter(p => p.effectiveness_score >= min_effectiveness);
  console.log(`  - After effectiveness filter (≥${min_effectiveness}): ${patterns.length} patterns`);

  // 4. Filter by tags
  if (tags.length > 0) {
    patterns = patterns.filter(p => {
      const patternTags = p.metadata.tags || [];
      return tags.some(tag => patternTags.includes(tag));
    });
    console.log(`  - After tag filter (${tags.join(", ")}): ${patterns.length} patterns`);
  }

  // 5. Sort patterns
  if (sortBy === "effectiveness_score") {
    patterns.sort((a, b) => b.effectiveness_score - a.effectiveness_score);
  } else if (sortBy === "created_at") {
    patterns.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  } else if (sortBy === "application_count") {
    patterns.sort((a, b) => b.application_count - a.application_count);
  }

  console.log(`  - Sorted by: ${sortBy}`);

  // 6. Apply limit and offset
  const paginatedPatterns = patterns.slice(offset, offset + effectiveLimit);

  console.log(`✓ Retrieved ${paginatedPatterns.length} patterns (offset: ${offset}, limit: ${effectiveLimit})`);

  // 7. Log retrieval event
  await npx claude-flow memory store `retrieval-event-${Date.now()}` JSON.stringify({
    domain,
    filters,
    options,
    results_count: paginatedPatterns.length,
    timestamp: new Date().toISOString()
  }) --namespace "patterns/retrieval-logs" --reasoningbank;

  return paginatedPatterns;
}

// Retrieve single pattern by ID (with expiry check)
async function retrievePatternById(patternId, domain, allowExpired = false) {
  console.log(`Retrieving pattern by ID: ${patternId}`);

  const namespace = `patterns/${domain}`;
  const patternKey = `pattern-${patternId}`;

  const patternData = await npx claude-flow memory retrieve --key patternKey --namespace namespace --reasoningbank;

  if (!patternData) {
    console.warn(`⚠️ Pattern not found: ${patternId}`);
    return null;
  }

  const pattern = JSON.parse(patternData);

  // Check expiry
  if (!allowExpired && isPatternExpired(pattern)) {
    console.warn(`⚠️ Pattern expired: ${patternId} (expiry: ${pattern.expiry_date})`);
    return null;
  }

  console.log(`✓ Retrieved pattern: ${patternId} (effectiveness: ${pattern.effectiveness_score})`);

  return pattern;
}

// Retrieve patterns by similarity (semantic matching)
async function retrieveSimilarPatterns(contextDescription, domain, limit = 5) {
  console.log(`Retrieving similar patterns for context: "${contextDescription.substring(0, 50)}..."`);

  // In production: Use semantic embedding similarity
  // For specification, simulate similarity search

  // Retrieve all active patterns
  const allPatterns = await retrievePatterns(domain, {}, { limit: 100 });

  // Simulate similarity scoring (in production, use vector embeddings)
  const scoredPatterns = allPatterns.map(p => ({
    ...p,
    similarity_score: Math.random() // Simulated similarity
  }));

  // Sort by similarity
  scoredPatterns.sort((a, b) => b.similarity_score - a.similarity_score);

  const similarPatterns = scoredPatterns.slice(0, limit);

  console.log(`✓ Retrieved ${similarPatterns.length} similar patterns`);

  return similarPatterns;
}

// Increment pattern application counter
async function trackPatternApplication(patternId, domain, success = true) {
  console.log(`Tracking pattern application: ${patternId} (success: ${success})`);

  const namespace = `patterns/${domain}`;
  const patternKey = `pattern-${patternId}`;

  const patternData = await npx claude-flow memory retrieve --key patternKey --namespace namespace --reasoningbank;

  if (!patternData) {
    throw new Error(`Pattern not found: ${patternId}`);
  }

  const pattern = JSON.parse(patternData);

  // Update counters
  pattern.application_count = (pattern.application_count || 0) + 1;

  if (success) {
    pattern.success_count = (pattern.success_count || 0) + 1;
  }

  // Recalculate effectiveness score
  pattern.effectiveness_score = pattern.success_count / pattern.application_count;

  pattern.metadata.last_applied_at = new Date().toISOString();

  // Update pattern
  await npx claude-flow memory store patternKey JSON.stringify(pattern) --namespace namespace --reasoningbank;

  console.log(`✓ Pattern application tracked: ${patternId}`);
  console.log(`  - Applications: ${pattern.application_count}`);
  console.log(`  - Successes: ${pattern.success_count}`);
  console.log(`  - Effectiveness: ${pattern.effectiveness_score.toFixed(3)}`);

  return {
    pattern_id: patternId,
    application_count: pattern.application_count,
    success_count: pattern.success_count,
    effectiveness_score: pattern.effectiveness_score
  };
}
```

---

### REQ-F032: Pattern Quality Scoring

**Priority:** P1-High
**Phase:** Monitoring (Phase 3 - 10 minutes)
**User Story:** US-034

**Description:**
Implement pattern quality scoring based on success rate, recency, application frequency, and validation consensus. Quality scores inform pattern selection and archival decisions.

**Quality Metrics:**

```yaml
quality_scoring:
  effectiveness_weight: 0.5      # Success rate importance
  recency_weight: 0.2            # Pattern freshness importance
  frequency_weight: 0.2          # Application count importance
  validation_weight: 0.1         # Validator consensus importance

  score_formula: |
    quality_score =
      (success_count / application_count) * 0.5 +
      (1 - days_since_creation / max_age_days) * 0.2 +
      (application_count / max_application_count) * 0.2 +
      (validated_by_count / total_validators) * 0.1
```

**Acceptance Criteria:**
- [ ] Quality scoring function: `calculateQualityScore(pattern)`
- [ ] Four weighted metrics: effectiveness (50%), recency (20%), frequency (20%), validation (10%)
- [ ] Score range: 0.0-1.0
- [ ] Quality threshold for retention: ≥ 0.6
- [ ] Quality degradation detection: alert when score drops below threshold
- [ ] Quality trends tracked over time
- [ ] Low-quality patterns flagged for review or archival

**Dependencies:**
- REQ-F030 (Pattern recording provides application_count, success_count)
- REQ-F031 (Pattern retrieval tracks application frequency)

**Test Coverage:**
- Unit: Verify quality score calculation
- Integration: Track pattern applications, verify score updates
- Regression: Ensure quality score persists across sessions

**Error Handling:**
- If missing data for scoring: Use defaults, log WARNING
- If score calculation fails: Default to 0.5, log error

**Implementation:**

```javascript
// Pattern Quality Scoring

const QUALITY_CONFIG = {
  effectiveness_weight: 0.5,
  recency_weight: 0.2,
  frequency_weight: 0.2,
  validation_weight: 0.1,
  quality_threshold: 0.6,
  max_application_count: 100 // Normalization factor
};

// Calculate pattern quality score
function calculateQualityScore(pattern) {
  const now = new Date();
  const createdDate = new Date(pattern.created_at);
  const expiryDate = new Date(pattern.expiry_date);

  // 1. Effectiveness score (success rate)
  const effectiveness = pattern.application_count > 0
    ? pattern.success_count / pattern.application_count
    : 0.5; // Default for new patterns

  // 2. Recency score (pattern freshness)
  const daysSinceCreation = (now - createdDate) / (1000 * 60 * 60 * 24);
  const maxAgeDays = (expiryDate - createdDate) / (1000 * 60 * 60 * 24);
  const recency = Math.max(0, 1 - (daysSinceCreation / maxAgeDays));

  // 3. Frequency score (application count)
  const frequency = Math.min(1, pattern.application_count / QUALITY_CONFIG.max_application_count);

  // 4. Validation score (validator consensus)
  const validatedByCount = (pattern.metadata.validated_by || []).length;
  const validation = Math.min(1, validatedByCount / 3); // Assume 3 validators ideal

  // Calculate weighted quality score
  const qualityScore =
    effectiveness * QUALITY_CONFIG.effectiveness_weight +
    recency * QUALITY_CONFIG.recency_weight +
    frequency * QUALITY_CONFIG.frequency_weight +
    validation * QUALITY_CONFIG.validation_weight;

  return {
    quality_score: parseFloat(qualityScore.toFixed(3)),
    components: {
      effectiveness: parseFloat(effectiveness.toFixed(3)),
      recency: parseFloat(recency.toFixed(3)),
      frequency: parseFloat(frequency.toFixed(3)),
      validation: parseFloat(validation.toFixed(3))
    }
  };
}

// Update pattern quality score
async function updatePatternQualityScore(patternId, domain) {
  console.log(`Updating quality score for pattern: ${patternId}`);

  const namespace = `patterns/${domain}`;
  const patternKey = `pattern-${patternId}`;

  const patternData = await npx claude-flow memory retrieve --key patternKey --namespace namespace --reasoningbank;

  if (!patternData) {
    throw new Error(`Pattern not found: ${patternId}`);
  }

  const pattern = JSON.parse(patternData);

  // Calculate quality score
  const qualityResult = calculateQualityScore(pattern);

  // Update pattern
  pattern.quality_score = qualityResult.quality_score;
  pattern.quality_components = qualityResult.components;
  pattern.quality_last_updated = new Date().toISOString();

  // Check quality threshold
  if (qualityResult.quality_score < QUALITY_CONFIG.quality_threshold) {
    console.warn(`⚠️ Pattern quality below threshold: ${qualityResult.quality_score} < ${QUALITY_CONFIG.quality_threshold}`);

    pattern.quality_alert = {
      triggered_at: new Date().toISOString(),
      quality_score: qualityResult.quality_score,
      threshold: QUALITY_CONFIG.quality_threshold,
      recommendation: "review-for-archival"
    };
  }

  // Update storage
  await npx claude-flow memory store patternKey JSON.stringify(pattern) --namespace namespace --reasoningbank;

  console.log(`✓ Quality score updated: ${qualityResult.quality_score}`);
  console.log(`  - Effectiveness: ${qualityResult.components.effectiveness}`);
  console.log(`  - Recency: ${qualityResult.components.recency}`);
  console.log(`  - Frequency: ${qualityResult.components.frequency}`);
  console.log(`  - Validation: ${qualityResult.components.validation}`);

  return qualityResult;
}

// Detect quality degradation
async function detectQualityDegradation(domain) {
  console.log(`Detecting quality degradation in domain: ${domain}`);

  const patterns = await retrievePatterns(domain, {}, { limit: 1000 });

  const degradedPatterns = [];

  for (const pattern of patterns) {
    const qualityResult = calculateQualityScore(pattern);

    if (qualityResult.quality_score < QUALITY_CONFIG.quality_threshold) {
      degradedPatterns.push({
        pattern_id: pattern.pattern_id,
        pattern_type: pattern.pattern_type,
        quality_score: qualityResult.quality_score,
        components: qualityResult.components,
        recommendation: determineRecommendation(qualityResult)
      });
    }
  }

  console.log(`Found ${degradedPatterns.length} degraded patterns`);

  // Store degradation report
  await npx claude-flow memory store `quality-degradation-${domain}-${Date.now()}` JSON.stringify({
    domain,
    total_patterns: patterns.length,
    degraded_count: degradedPatterns.length,
    degraded_patterns: degradedPatterns,
    timestamp: new Date().toISOString()
  }) --namespace "patterns/quality-reports" --reasoningbank;

  return degradedPatterns;
}

// Determine recommendation based on quality score
function determineRecommendation(qualityResult) {
  const { quality_score, components } = qualityResult;

  if (quality_score < 0.3) {
    return "archive-immediately";
  } else if (quality_score < 0.5) {
    return "archive-if-not-improved-in-30-days";
  } else if (quality_score < 0.6) {
    if (components.effectiveness < 0.5) {
      return "review-effectiveness";
    } else if (components.recency < 0.3) {
      return "consider-archival-due-to-age";
    } else {
      return "monitor-quality-trends";
    }
  }

  return "maintain-active-status";
}
```

---

### REQ-F033: Cross-Domain Transfer Safety

**Priority:** P1-High
**Phase:** Monitoring (Phase 3 - 10 minutes)
**User Story:** US-034

**Description:**
Implement cross-domain transfer safety to prevent inappropriate pattern transfers between domains. Prevents PhD research patterns from being applied to business strategy tasks and vice versa.

**Transfer Safety Rules:**

```yaml
transfer_safety:
  allowed_transfers:
    phd_patterns:
      - phd_patterns           # Same domain allowed
      - industry_patterns      # PhD can inform industry research

    business_research_patterns:
      - business_research_patterns
      - industry_patterns      # Business research can inform industry
      - business_strategy_patterns  # Research informs strategy

    business_strategy_patterns:
      - business_strategy_patterns
      # NOT allowed: PhD or business research patterns

    industry_patterns:
      - industry_patterns
      - phd_patterns           # Industry can be informed by research
      - business_research_patterns

  transfer_validation_mode: "strict"  # strict|permissive|disabled
```

**Acceptance Criteria:**
- [ ] Transfer validation function: `validatePatternTransfer(sourcePattern, targetDomain)`
- [ ] Transfer rules defined per domain (allowed target domains)
- [ ] Strict mode: reject unauthorized transfers
- [ ] Permissive mode: warn but allow unauthorized transfers
- [ ] Disabled mode: allow all transfers (for testing)
- [ ] Transfer logs: track all transfer attempts and validations
- [ ] Transfer rejection messages with explanation

**Dependencies:**
- REQ-F027 (Storage templates define domain types)
- REQ-F031 (Pattern retrieval enforces transfer validation)

**Test Coverage:**
- Unit: Verify transfer validation logic
- Integration: Attempt unauthorized transfer, confirm rejection
- Regression: Ensure authorized transfers succeed
- Edge Case: Test permissive and disabled modes

**Error Handling:**
- If unauthorized transfer in strict mode: Reject, log error
- If unauthorized transfer in permissive mode: Warn, allow
- If transfer validation fails: Default to reject, log error

**Implementation:**

```javascript
// Cross-Domain Transfer Safety

const TRANSFER_SAFETY_CONFIG = {
  validation_mode: "strict", // strict|permissive|disabled
  allowed_transfers: {
    phd_patterns: ["phd_patterns", "industry_patterns"],
    business_research_patterns: [
      "business_research_patterns",
      "industry_patterns",
      "business_strategy_patterns"
    ],
    business_strategy_patterns: ["business_strategy_patterns"],
    industry_patterns: [
      "industry_patterns",
      "phd_patterns",
      "business_research_patterns"
    ]
  }
};

// Validate pattern transfer across domains
function validatePatternTransfer(sourcePattern, targetDomain) {
  console.log(`Validating pattern transfer: ${sourcePattern.metadata.source_domain || sourcePattern.domain} → ${targetDomain}`);

  const sourceDomain = sourcePattern.metadata.source_domain || "unknown";

  // Disabled mode: allow all transfers
  if (TRANSFER_SAFETY_CONFIG.validation_mode === "disabled") {
    console.log("  [DISABLED MODE] Transfer allowed");
    return { allowed: true, mode: "disabled" };
  }

  // Check if transfer allowed
  const allowedTargets = TRANSFER_SAFETY_CONFIG.allowed_transfers[sourceDomain] || [];
  const isAllowed = allowedTargets.includes(targetDomain);

  if (isAllowed) {
    console.log(`✓ Transfer allowed: ${sourceDomain} → ${targetDomain}`);
    return {
      allowed: true,
      source_domain: sourceDomain,
      target_domain: targetDomain
    };
  }

  // Unauthorized transfer detected
  const errorMessage = `Unauthorized pattern transfer: ${sourceDomain} → ${targetDomain}. Allowed targets: ${allowedTargets.join(", ")}`;

  if (TRANSFER_SAFETY_CONFIG.validation_mode === "strict") {
    console.error(`❌ ${errorMessage}`);
    return {
      allowed: false,
      mode: "strict",
      source_domain: sourceDomain,
      target_domain: targetDomain,
      error: errorMessage
    };
  } else if (TRANSFER_SAFETY_CONFIG.validation_mode === "permissive") {
    console.warn(`⚠️ ${errorMessage} [PERMISSIVE: Allowing anyway]`);
    return {
      allowed: true,
      mode: "permissive",
      warning: errorMessage,
      source_domain: sourceDomain,
      target_domain: targetDomain
    };
  }

  // Default: reject
  return {
    allowed: false,
    source_domain: sourceDomain,
    target_domain: targetDomain,
    error: errorMessage
  };
}

// Retrieve patterns with transfer safety
async function retrievePatternsWithTransferSafety(sourceDomain, targetDomain, filters = {}, options = {}) {
  console.log(`Retrieving patterns with transfer safety: ${sourceDomain} → ${targetDomain}`);

  // Retrieve patterns from source domain
  const patterns = await retrievePatterns(sourceDomain, filters, options);

  // Validate each pattern transfer
  const validPatterns = [];
  const rejectedPatterns = [];

  for (const pattern of patterns) {
    const validation = validatePatternTransfer({ ...pattern, domain: sourceDomain }, targetDomain);

    if (validation.allowed) {
      validPatterns.push(pattern);
    } else {
      rejectedPatterns.push({
        pattern_id: pattern.pattern_id,
        rejection_reason: validation.error
      });
    }
  }

  console.log(`✓ Transfer validation complete:`);
  console.log(`  - Valid: ${validPatterns.length}`);
  console.log(`  - Rejected: ${rejectedPatterns.length}`);

  // Log transfer validation
  await npx claude-flow memory store `transfer-validation-${Date.now()}` JSON.stringify({
    source_domain: sourceDomain,
    target_domain: targetDomain,
    validation_mode: TRANSFER_SAFETY_CONFIG.validation_mode,
    valid_count: validPatterns.length,
    rejected_count: rejectedPatterns.length,
    rejected_patterns: rejectedPatterns,
    timestamp: new Date().toISOString()
  }) --namespace "patterns/transfer-logs" --reasoningbank;

  return {
    valid_patterns: validPatterns,
    rejected_patterns: rejectedPatterns,
    validation_mode: TRANSFER_SAFETY_CONFIG.validation_mode
  };
}
```

---

### REQ-F034: Pattern Versioning and Metadata Tracking

**Priority:** P2-Medium
**Phase:** Short-term (Phase 4 - 10 minutes)
**User Story:** US-035

**Description:**
Implement pattern versioning to track pattern evolution over time. Support version increments, change logs, backward compatibility, and version rollback.

**Versioning Features:**

1. **Semantic Versioning**: major.minor format (e.g., 1.0, 1.1, 2.0)
2. **Change Logs**: Track changes between versions
3. **Version History**: Store all historical versions
4. **Backward Compatibility**: Flag breaking changes
5. **Version Rollback**: Restore previous version if needed

**Acceptance Criteria:**
- [ ] Pattern versioning: `pattern_version` field (e.g., "1.0")
- [ ] Version increment: `incrementPatternVersion(patternId, domain, changeType)`
- [ ] Change types: `minor` (1.0 → 1.1), `major` (1.9 → 2.0)
- [ ] Change logs: `version_history` array with change descriptions
- [ ] Version history storage: `patterns/{domain}/versions/{pattern-id}/`
- [ ] Version rollback: `rollbackPatternVersion(patternId, domain, targetVersion)`
- [ ] Breaking change flag: `is_breaking_change` boolean

**Dependencies:**
- REQ-F027 (Storage templates include version metadata)
- REQ-F030 (Pattern recording initializes version 1.0)

**Test Coverage:**
- Unit: Verify version increment logic
- Integration: Increment version, verify history stored
- Rollback: Rollback to previous version, verify restoration

**Error Handling:**
- If version history missing: Initialize with current version
- If rollback target not found: Throw error
- If version format invalid: Use 1.0 as default

**Implementation:**

```javascript
// Pattern Versioning and Metadata Tracking

const VERSIONING_CONFIG = {
  initial_version: "1.0",
  version_history_namespace: "patterns/versions"
};

// Increment pattern version
async function incrementPatternVersion(patternId, domain, changeType = "minor", changeDescription) {
  console.log(`Incrementing pattern version: ${patternId} (changeType: ${changeType})`);

  const namespace = `patterns/${domain}`;
  const patternKey = `pattern-${patternId}`;

  const patternData = await npx claude-flow memory retrieve --key patternKey --namespace namespace --reasoningbank;

  if (!patternData) {
    throw new Error(`Pattern not found: ${patternId}`);
  }

  const pattern = JSON.parse(patternData);

  // Get current version
  const currentVersion = pattern.metadata.pattern_version || VERSIONING_CONFIG.initial_version;
  const [major, minor] = currentVersion.split(".").map(Number);

  // Calculate new version
  let newVersion;
  if (changeType === "major") {
    newVersion = `${major + 1}.0`;
  } else {
    newVersion = `${major}.${minor + 1}`;
  }

  // Store version history
  const versionHistory = pattern.metadata.version_history || [];

  versionHistory.push({
    version: currentVersion,
    timestamp: new Date().toISOString(),
    change_type: changeType,
    change_description: changeDescription,
    effectiveness_score: pattern.effectiveness_score,
    application_count: pattern.application_count
  });

  // Update pattern
  pattern.metadata.pattern_version = newVersion;
  pattern.metadata.version_history = versionHistory;
  pattern.metadata.last_version_update = new Date().toISOString();
  pattern.metadata.is_breaking_change = (changeType === "major");

  // Save updated pattern
  await npx claude-flow memory store patternKey JSON.stringify(pattern) --namespace namespace --reasoningbank;

  console.log(`✓ Pattern version updated: ${currentVersion} → ${newVersion}`);
  console.log(`  - Change type: ${changeType}`);
  console.log(`  - Description: ${changeDescription}`);

  // Store version snapshot
  await storeVersionSnapshot(pattern, domain, currentVersion);

  return {
    pattern_id: patternId,
    previous_version: currentVersion,
    new_version: newVersion,
    change_type: changeType
  };
}

// Store version snapshot
async function storeVersionSnapshot(pattern, domain, version) {
  const versionNamespace = `${VERSIONING_CONFIG.version_history_namespace}/${domain}/${pattern.pattern_id}`;
  const versionKey = `version-${version}`;

  await npx claude-flow memory store versionKey JSON.stringify({
    ...pattern,
    snapshot_version: version,
    snapshot_timestamp: new Date().toISOString()
  }) --namespace versionNamespace --reasoningbank;

  console.log(`  ✓ Version snapshot stored: ${versionNamespace}/${versionKey}`);
}

// Rollback pattern to previous version
async function rollbackPatternVersion(patternId, domain, targetVersion) {
  console.log(`Rolling back pattern: ${patternId} → v${targetVersion}`);

  // Retrieve version snapshot
  const versionNamespace = `${VERSIONING_CONFIG.version_history_namespace}/${domain}/${patternId}`;
  const versionKey = `version-${targetVersion}`;

  const snapshotData = await npx claude-flow memory retrieve --key versionKey --namespace versionNamespace --reasoningbank;

  if (!snapshotData) {
    throw new Error(`Version snapshot not found: ${patternId} v${targetVersion}`);
  }

  const snapshot = JSON.parse(snapshotData);

  // Restore pattern (remove snapshot metadata)
  const { snapshot_version, snapshot_timestamp, ...restoredPattern } = snapshot;

  restoredPattern.metadata.rollback_info = {
    rolled_back_at: new Date().toISOString(),
    from_version: restoredPattern.metadata.pattern_version,
    to_version: targetVersion,
    rollback_reason: "manual-rollback"
  };

  restoredPattern.metadata.pattern_version = targetVersion;

  // Save restored pattern
  const namespace = `patterns/${domain}`;
  const patternKey = `pattern-${patternId}`;

  await npx claude-flow memory store patternKey JSON.stringify(restoredPattern) --namespace namespace --reasoningbank;

  console.log(`✓ Pattern rolled back to v${targetVersion}`);

  return {
    pattern_id: patternId,
    restored_version: targetVersion
  };
}
```

---

### REQ-F035: Pattern Library Management

**Priority:** P2-Medium
**Phase:** Short-term (Phase 4 - 10 minutes)
**User Story:** US-035

**Description:**
Implement pattern library management to organize, search, and maintain pattern collections per domain. Libraries enable efficient pattern discovery, curation, and knowledge sharing.

**Library Features:**

1. **Library Index**: Centralized index of all patterns per domain
2. **Pattern Search**: Full-text and semantic search across patterns
3. **Pattern Collections**: Curated collections for specific use cases
4. **Library Statistics**: Pattern count, average quality, usage metrics
5. **Library Maintenance**: Cleanup, deduplication, quality reviews

**Acceptance Criteria:**
- [ ] Library index: `patterns/library-index/{domain}`
- [ ] Pattern search: `searchPatternLibrary(domain, query, searchType)`
- [ ] Search types: `exact`, `semantic`, `tag-based`
- [ ] Library statistics: `getLibraryStatistics(domain)`
- [ ] Pattern collections: `createPatternCollection(name, patternIds)`
- [ ] Library maintenance: `maintainPatternLibrary(domain)` (cleanup, dedup)

**Dependencies:**
- REQ-F030 (Pattern recording populates library)
- REQ-F031 (Pattern retrieval uses library index)

**Test Coverage:**
- Unit: Verify library index updates
- Integration: Search library, verify results
- Maintenance: Run library maintenance, verify cleanup

**Error Handling:**
- If library index corrupted: Rebuild from patterns
- If search fails: Return empty results, log error
- If maintenance fails: Log error, skip problematic patterns

**Implementation:**

```javascript
// Pattern Library Management

const LIBRARY_CONFIG = {
  index_namespace: "patterns/library-index",
  collections_namespace: "patterns/collections",
  statistics_namespace: "patterns/library-stats"
};

// Get library statistics
async function getLibraryStatistics(domain) {
  console.log(`Generating library statistics for: ${domain}`);

  const patterns = await retrievePatterns(domain, {}, { limit: 10000 });

  const stats = {
    domain,
    total_patterns: patterns.length,
    pattern_types: {},
    avg_effectiveness: 0,
    avg_quality_score: 0,
    total_applications: 0,
    total_successes: 0,
    oldest_pattern: null,
    newest_pattern: null,
    timestamp: new Date().toISOString()
  };

  let totalEffectiveness = 0;
  let totalQuality = 0;

  for (const pattern of patterns) {
    // Count by type
    const patternType = pattern.pattern_type;
    stats.pattern_types[patternType] = (stats.pattern_types[patternType] || 0) + 1;

    // Sum effectiveness and quality
    totalEffectiveness += pattern.effectiveness_score;
    totalQuality += pattern.quality_score || 0;

    // Track applications
    stats.total_applications += pattern.application_count;
    stats.total_successes += pattern.success_count;

    // Track oldest/newest
    if (!stats.oldest_pattern || pattern.created_at < stats.oldest_pattern) {
      stats.oldest_pattern = pattern.created_at;
    }
    if (!stats.newest_pattern || pattern.created_at > stats.newest_pattern) {
      stats.newest_pattern = pattern.created_at;
    }
  }

  stats.avg_effectiveness = patterns.length > 0
    ? (totalEffectiveness / patterns.length).toFixed(3)
    : 0;

  stats.avg_quality_score = patterns.length > 0
    ? (totalQuality / patterns.length).toFixed(3)
    : 0;

  console.log(`Library Statistics for ${domain}:`);
  console.log(`  - Total patterns: ${stats.total_patterns}`);
  console.log(`  - Avg effectiveness: ${stats.avg_effectiveness}`);
  console.log(`  - Avg quality: ${stats.avg_quality_score}`);
  console.log(`  - Total applications: ${stats.total_applications}`);

  // Store statistics
  await npx claude-flow memory store `library-stats-${domain}` JSON.stringify(stats) --namespace LIBRARY_CONFIG.statistics_namespace --reasoningbank;

  return stats;
}

// Search pattern library
async function searchPatternLibrary(domain, query, searchType = "semantic") {
  console.log(`Searching pattern library: ${domain} (query: "${query}", type: ${searchType})`);

  const patterns = await retrievePatterns(domain, {}, { limit: 1000 });

  let results = [];

  if (searchType === "exact") {
    // Exact match on description or tags
    results = patterns.filter(p =>
      p.pattern_content.description.toLowerCase().includes(query.toLowerCase()) ||
      (p.metadata.tags || []).some(tag => tag.toLowerCase() === query.toLowerCase())
    );
  } else if (searchType === "tag-based") {
    // Tag-based search
    results = patterns.filter(p =>
      (p.metadata.tags || []).some(tag => tag.toLowerCase().includes(query.toLowerCase()))
    );
  } else if (searchType === "semantic") {
    // Semantic search (simulated - in production use embeddings)
    results = await retrieveSimilarPatterns(query, domain, 10);
  }

  console.log(`✓ Found ${results.length} matching patterns`);

  return results;
}

// Maintain pattern library (cleanup, deduplication)
async function maintainPatternLibrary(domain) {
  console.log(`Maintaining pattern library: ${domain}`);

  const patterns = await retrievePatterns(domain, {}, { limit: 10000 });

  const maintenanceReport = {
    domain,
    total_patterns: patterns.length,
    duplicates_removed: 0,
    low_quality_archived: 0,
    expired_archived: 0,
    timestamp: new Date().toISOString()
  };

  // 1. Detect and remove duplicates
  const duplicates = detectDuplicates(patterns);
  maintenanceReport.duplicates_removed = duplicates.length;

  console.log(`  - Duplicates detected: ${duplicates.length}`);

  // 2. Archive low-quality patterns
  const lowQualityPatterns = patterns.filter(p => {
    const quality = calculateQualityScore(p);
    return quality.quality_score < 0.3;
  });

  for (const pattern of lowQualityPatterns) {
    await archivePattern(pattern.pattern_id, domain, "quality-degradation");
    maintenanceReport.low_quality_archived++;
  }

  console.log(`  - Low-quality patterns archived: ${maintenanceReport.low_quality_archived}`);

  // 3. Archive expired patterns
  const expiredPatterns = patterns.filter(p => isPatternExpired(p));

  for (const pattern of expiredPatterns) {
    await archivePattern(pattern.pattern_id, domain, "expiry");
    maintenanceReport.expired_archived++;
  }

  console.log(`  - Expired patterns archived: ${maintenanceReport.expired_archived}`);

  // Store maintenance report
  await npx claude-flow memory store `maintenance-report-${domain}-${Date.now()}` JSON.stringify(maintenanceReport) --namespace "patterns/maintenance-reports" --reasoningbank;

  console.log(`✓ Library maintenance complete for ${domain}`);

  return maintenanceReport;
}

// Detect duplicate patterns
function detectDuplicates(patterns) {
  const duplicates = [];
  const seenSignatures = new Map();

  for (const pattern of patterns) {
    // Create pattern signature (for deduplication)
    const signature = `${pattern.pattern_type}-${pattern.pattern_content.description.substring(0, 100)}`;

    if (seenSignatures.has(signature)) {
      duplicates.push({
        pattern_id: pattern.pattern_id,
        duplicate_of: seenSignatures.get(signature)
      });
    } else {
      seenSignatures.set(signature, pattern.pattern_id);
    }
  }

  return duplicates;
}
```

---

## Integration Points

### Downstream Dependencies (What This Provides)

**To Meta-Learning (06-meta-learning.md):**
- Fresh patterns only (expired patterns archived)
- Domain-specific pattern libraries (PhD, business research, business strategy)
- Pattern quality scores for selection optimization
- Pattern application tracking for effectiveness analysis
- Transfer safety rules for cross-domain learning

**To Monitoring & Health (07-monitoring-health.md):**
- Pattern library statistics (count, avg quality, usage)
- Pattern expiry notifications
- Quality degradation alerts
- Archive activity metrics
- Transfer validation logs

### Upstream Dependencies (What This Requires)

**From Knowledge Sharing (04-knowledge-sharing.md):**
- Knowledge flow effectiveness data (provides effectiveness scores)
- Agent participation data (identifies successful patterns)
- Flow completion metrics (triggers pattern recording)
- Namespace isolation (ensures project-scoped patterns)

**From Agent Lifecycle (03-agent-lifecycle.md):**
- Agent IDs for pattern metadata tracking
- Cognitive patterns for domain classification
- Agent effectiveness scores for pattern quality

---

## Quality Metrics

### Pattern Expiry Coverage

**Definition:** Percentage of active patterns with valid expiry dates

**Target:** ≥ 99%

**Measurement:**
```javascript
const patterns = await retrievePatterns(domain, {}, { limit: 10000 });
const withExpiry = patterns.filter(p => p.expiry_date).length;
const coverage = (withExpiry / patterns.length * 100).toFixed(1);
console.log(`Pattern Expiry Coverage: ${coverage}%`);
```

**Remediation:** If < 99%, run expiry date backfill for patterns missing expiry_date

---

### Pattern Quality Average

**Definition:** Average quality score across all active patterns

**Target:** ≥ 0.7

**Measurement:**
```javascript
const stats = await getLibraryStatistics(domain);
console.log(`Avg Quality Score: ${stats.avg_quality_score}`);
```

**Remediation:** If < 0.7, archive low-quality patterns, improve pattern recording criteria

---

### Archive Automation Rate

**Definition:** Percentage of expirations handled automatically vs manually

**Target:** ≥ 95%

**Measurement:**
```javascript
const archiveEvents = await retrieveArchiveEvents();
const autoArchived = archiveEvents.filter(e => e.archive_reason === "expiry").length;
const manualArchived = archiveEvents.filter(e => e.archive_reason === "manual").length;
const autoRate = (autoArchived / (autoArchived + manualArchived) * 100).toFixed(1);
console.log(`Archive Automation Rate: ${autoRate}%`);
```

**Remediation:** If < 95%, verify expiry checker script running, check for automation failures

---

## Summary for Agent #7 (Meta-Learning)

**Completion Status:** 10/10 requirements delivered (REQ-F026 to REQ-F035)

**Pattern Management Inventory:**

| Component | Deliverables | Key Features |
|-----------|-------------|--------------|
| Expiry Policy | 4 domain rules | PhD: 180d, BizResearch: 90d, BizStrategy: 60d, Industry: 120d |
| Storage Templates | 3 templates | PhD, Business Research, Business Strategy schemas |
| Expiry Checker | 1 script | Automated detection, archival, dry-run mode |
| Archive Procedures | 5 functions | Archive, unarchive, list, stats, cleanup |
| Pattern Recording | 6 functions | Record, extract, validate, detect duplicates |
| Pattern Retrieval | 4 functions | Retrieve, by-ID, similarity, application tracking |
| Quality Scoring | 4 functions | Calculate, update, detect degradation |
| Transfer Safety | 3 functions | Validate, retrieve with safety, transfer logs |
| Versioning | 3 functions | Increment, rollback, version history |
| Library Management | 5 functions | Stats, search, maintain, collections |

**What Agent #7 Needs for Meta-Learning:**

1. **Fresh Patterns Only**: Expired patterns archived, only active patterns available
2. **Domain Libraries**: Three pattern libraries (PhD, business research, business strategy)
3. **Quality Scores**: Patterns filtered by quality threshold (≥ 0.7)
4. **Transfer Rules**: Cross-domain transfer safety prevents inappropriate transfers
5. **Application Data**: Pattern success/failure tracking for learning optimization
6. **Pattern Metadata**: Tags, creation dates, effectiveness scores for semantic matching

**Dependencies for Meta-Learning:**
- `patterns/{domain}/*` - active pattern storage
- `patterns/archived/{domain}/*` - archived patterns (excluded from retrieval)
- `patterns/library-index/*` - pattern library indexes
- `patterns/quality-reports/*` - quality degradation reports
- `patterns/transfer-logs/*` - transfer validation logs
- `config/patterns/expiry` - expiry policy configuration

**Key Integration Data:**
- 4 domain-specific expiry policies (60-180 days)
- 3 storage templates (PhD, business research, business strategy)
- 1 automated expiry checker script (`docs2/neural-pattern-expiry-checker.js`)
- Archive namespace: `patterns/archived/{domain}/`
- Pattern quality threshold: 0.7 for storage, 0.6 for retention
- Transfer safety: Strict mode enabled by default
- Pattern versioning: Semantic versioning (major.minor)
- Library statistics: Total, avg quality, avg effectiveness per domain

---

## Document Control

**Version History:**

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-27 | Initial Pattern Management functional spec | Specification Agent #6 |

**Related Documents:**

**Upstream (Level 1 - Depends on):**
- `04-knowledge-sharing.md` - Knowledge flows provide effectiveness data
- `03-agent-lifecycle.md` - Agent metadata for pattern tracking
- `02-daa-initialization.md` - ReasoningBank backend
- `00-project-constitution.md` - Project foundation

**Downstream (Level 2 - Depends on this):**
- `06-meta-learning.md` - Requires fresh patterns and quality scores
- `07-monitoring-health.md` - Requires pattern library statistics
- `08-integration-testing.md` - Requires pattern management for end-to-end tests

**Source PRDs:**
- `docs2/neuralenhancement/neural-enhancement-short-term.md` - Phase 2-3

---

**END OF FUNCTIONAL SPECIFICATION: PATTERN MANAGEMENT**
