# TASK-NEURAL-009: Pattern Storage with Expiry Mechanism

## Metadata
- **Task ID**: TASK-NEURAL-009
- **Title**: Pattern Storage with Expiry Mechanism
- **Implements Requirements**: REQ-NEURAL-26, REQ-NEURAL-27, REQ-NEURAL-28, REQ-NEURAL-29
- **Dependencies**: TASK-NEURAL-008 (Knowledge Sharing)
- **Complexity**: MEDIUM
- **Estimated Time**: 25 minutes
- **Status**: PENDING

## Context

Implements a comprehensive pattern storage system with automatic expiry policies to prevent stale patterns from degrading meta-learning quality. Each domain (PhD research, business research, business strategy, industry analysis) has different expiry rules based on knowledge evolution rates. Expired patterns are automatically archived rather than deleted to preserve historical learning.

## Objectives

1. Create domain-specific pattern expiry policies
2. Implement pattern recording workflow with timestamp tracking
3. Build automated expiry checker and archival system
4. Define pattern templates for each domain type
5. Enable pattern lifecycle management

## Pseudo-code

```bash
# ========================================
# STEP 1: Create Pattern Expiry Policy
# ========================================

npx claude-flow memory store "pattern-expiry-policy" "{
  \"policy_version\": \"1.0\",
  \"project_id\": \"$PROJECT_ID\",
  \"created_at\": \"$(date -Iseconds)\",
  \"expiry_rules\": {
    \"phd_patterns\": {
      \"max_age_days\": 180,
      \"reason\": \"Academic research evolves significantly\",
      \"check_frequency_days\": 30
    },
    \"business_research_patterns\": {
      \"max_age_days\": 90,
      \"reason\": \"Market conditions change rapidly\",
      \"check_frequency_days\": 14
    },
    \"business_strategy_patterns\": {
      \"max_age_days\": 60,
      \"reason\": \"Strategic landscapes shift quickly\",
      \"check_frequency_days\": 7
    },
    \"industry_patterns\": {
      \"max_age_days\": 120,
      \"reason\": \"Industry trends evolve moderately\",
      \"check_frequency_days\": 21
    }
  },
  \"auto_archive\": true,
  \"archive_namespace\": \"patterns/archived\",
  \"notification_before_expiry_days\": 14
}" --namespace "config/patterns/expiry"

echo "✓ Pattern expiry policy created"

# ========================================
# STEP 2: Pattern Recording Workflow
# ========================================

mcp__ruv-swarm__daa_workflow_create({
  id: "pattern-recording-workflow",
  name: "Pattern Recording and Lifecycle Management",
  steps: [
    {
      id: "collect-metrics",
      agent: "meta-learning-orchestrator",
      action: "Collect performance metrics from recent transfers",
      timeout: 300
    },
    {
      id: "check-expiry",
      agent: "meta-learning-orchestrator",
      action: "Scan all patterns for expiry based on policy",
      depends_on: []
    },
    {
      id: "archive-expired",
      agent: "meta-learning-orchestrator",
      action: "Move expired patterns to archive namespace",
      depends_on: ["check-expiry"]
    },
    {
      id: "store-patterns",
      agent: "meta-learning-orchestrator",
      action: "Store new patterns with timestamps and expiry dates",
      depends_on: ["collect-metrics", "archive-expired"]
    },
    {
      id: "update-indexes",
      agent: "meta-learning-orchestrator",
      action: "Rebuild pattern search indexes",
      depends_on: ["store-patterns"]
    }
  ],
  strategy: "sequential"
})

echo "✓ Pattern recording workflow created"

# ========================================
# STEP 3: Pattern Expiry Checker Script
# ========================================

cat > docs2/neural-pattern-expiry-checker.js << 'EOF'
#!/usr/bin/env node
/**
 * Pattern Expiry Checker
 * Scans stored patterns and archives expired ones based on policy
 */

const { execSync } = require('child_process');

async function checkAndArchiveExpiredPatterns() {
  console.log('🔍 Starting pattern expiry check...');

  // Load expiry policy
  const policyJson = execSync(
    'npx claude-flow memory retrieve "pattern-expiry-policy" --namespace "config/patterns/expiry"',
    { encoding: 'utf-8' }
  );
  const policy = JSON.parse(policyJson);

  const domains = [
    'phd',
    'business-research',
    'business-strategy',
    'industry'
  ];

  let totalExpired = 0;
  let totalArchived = 0;

  for (const domain of domains) {
    console.log(`\n📂 Checking ${domain} patterns...`);

    // List all patterns in domain
    const patterns = execSync(
      `npx claude-flow memory list --namespace "patterns/${domain}/successful"`,
      { encoding: 'utf-8' }
    );

    const patternKeys = patterns.split('\n').filter(k => k.trim());

    for (const key of patternKeys) {
      try {
        // Retrieve pattern
        const patternData = execSync(
          `npx claude-flow memory retrieve "${key}" --namespace "patterns/${domain}/successful"`,
          { encoding: 'utf-8' }
        );
        const pattern = JSON.parse(patternData);

        // Check expiry
        const expiresAt = new Date(pattern.expires_at);
        const now = new Date();

        if (now > expiresAt) {
          console.log(`  ⏰ Expired: ${key} (expired ${Math.floor((now - expiresAt) / (1000 * 60 * 60 * 24))} days ago)`);
          totalExpired++;

          // Archive pattern
          if (policy.auto_archive) {
            execSync(
              `npx claude-flow memory store "${key}" '${JSON.stringify({
                ...pattern,
                archived_at: now.toISOString(),
                original_namespace: \`patterns/\${domain}/successful\`
              })}' --namespace "${policy.archive_namespace}/${domain}"`,
              { encoding: 'utf-8' }
            );

            // Delete from active patterns
            execSync(
              `npx claude-flow memory delete "${key}" --namespace "patterns/${domain}/successful"`,
              { encoding: 'utf-8' }
            );

            totalArchived++;
            console.log(`    ✓ Archived to ${policy.archive_namespace}/${domain}`);
          }
        }
      } catch (error) {
        console.error(`  ✗ Error processing ${key}:`, error.message);
      }
    }
  }

  console.log(`\n📊 Summary:`);
  console.log(`  - Total expired patterns: ${totalExpired}`);
  console.log(`  - Total archived: ${totalArchived}`);
  console.log(`  - Auto-archive enabled: ${policy.auto_archive}`);

  return { totalExpired, totalArchived };
}

// Run if called directly
if (require.main === module) {
  checkAndArchiveExpiredPatterns()
    .then(() => process.exit(0))
    .catch(err => {
      console.error('❌ Error:', err);
      process.exit(1);
    });
}

module.exports = { checkAndArchiveExpiredPatterns };
EOF

chmod +x docs2/neural-pattern-expiry-checker.js
echo "✓ Expiry checker script created"

# ========================================
# STEP 4: Store Sample Pattern with Expiry
# ========================================

# PhD Pattern Example
npx claude-flow memory store "pattern-phd-literature-review-01" "{
  \"pattern_id\": \"phd-literature-review-success\",
  \"domain\": \"phd\",
  \"pattern_type\": \"successful_transfer\",
  \"created_at\": \"$(date -Iseconds)\",
  \"expires_at\": \"$(date -d '+180 days' -Iseconds)\",
  \"source_domain\": \"systematic-review-methodology\",
  \"target_domain\": \"dissertation-chapter-2\",
  \"transfer_success_rate\": 0.92,
  \"pattern_data\": {
    \"strategy\": \"hierarchical-search-synthesis\",
    \"key_techniques\": [
      \"citation-network-analysis\",
      \"thematic-clustering\",
      \"gap-identification\"
    ],
    \"context_factors\": {
      \"field\": \"computer-science\",
      \"methodology\": \"mixed-methods\",
      \"timeline\": \"6-months\"
    }
  },
  \"usage_count\": 0,
  \"last_used_at\": null
}" --namespace "patterns/phd/successful"

# Business Research Pattern Example
npx claude-flow memory store "pattern-business-market-analysis-01" "{
  \"pattern_id\": \"business-market-analysis-success\",
  \"domain\": \"business-research\",
  \"pattern_type\": \"successful_transfer\",
  \"created_at\": \"$(date -Iseconds)\",
  \"expires_at\": \"$(date -d '+90 days' -Iseconds)\",
  \"source_domain\": \"competitor-analysis\",
  \"target_domain\": \"market-entry-strategy\",
  \"transfer_success_rate\": 0.88,
  \"pattern_data\": {
    \"strategy\": \"swot-to-strategy-mapping\",
    \"key_techniques\": [
      \"market-segmentation\",
      \"competitive-positioning\",
      \"trend-forecasting\"
    ],
    \"context_factors\": {
      \"industry\": \"saas\",
      \"market_maturity\": \"growth\",
      \"timeline\": \"quarter\"
    }
  },
  \"usage_count\": 0,
  \"last_used_at\": null
}" --namespace "patterns/business-research/successful"

# Business Strategy Pattern Example
npx claude-flow memory store "pattern-business-strategy-pivot-01" "{
  \"pattern_id\": \"business-strategy-pivot-success\",
  \"domain\": \"business-strategy\",
  \"pattern_type\": \"successful_transfer\",
  \"created_at\": \"$(date -Iseconds)\",
  \"expires_at\": \"$(date -d '+60 days' -Iseconds)\",
  \"source_domain\": \"product-market-fit-analysis\",
  \"target_domain\": \"strategic-pivot-execution\",
  \"transfer_success_rate\": 0.85,
  \"pattern_data\": {
    \"strategy\": \"lean-startup-adaptation\",
    \"key_techniques\": [
      \"customer-discovery\",
      \"hypothesis-testing\",
      \"iterative-refinement\"
    ],
    \"context_factors\": {
      \"company_stage\": \"early-stage\",
      \"pivot_type\": \"customer-segment\",
      \"urgency\": \"high\"
    }
  },
  \"usage_count\": 0,
  \"last_used_at\": null
}" --namespace "patterns/business-strategy/successful"

# Industry Pattern Example
npx claude-flow memory store "pattern-industry-ai-adoption-01" "{
  \"pattern_id\": \"industry-ai-adoption-success\",
  \"domain\": \"industry\",
  \"pattern_type\": \"successful_transfer\",
  \"created_at\": \"$(date -Iseconds)\",
  \"expires_at\": \"$(date -d '+120 days' -Iseconds)\",
  \"source_domain\": \"ai-implementation-healthcare\",
  \"target_domain\": \"ai-implementation-finance\",
  \"transfer_success_rate\": 0.78,
  \"pattern_data\": {
    \"strategy\": \"cross-industry-best-practices\",
    \"key_techniques\": [
      \"regulatory-mapping\",
      \"risk-assessment-framework\",
      \"phased-rollout\"
    ],
    \"context_factors\": {
      \"regulation_level\": \"high\",
      \"data_sensitivity\": \"high\",
      \"timeline\": \"12-months\"
    }
  },
  \"usage_count\": 0,
  \"last_used_at\": null
}" --namespace "patterns/industry/successful"

echo "✓ Sample patterns stored with expiry timestamps"

# ========================================
# STEP 5: Create Pattern Templates
# ========================================

npx claude-flow memory store "pattern-templates" "{
  \"template_version\": \"1.0\",
  \"templates\": {
    \"phd\": {
      \"required_fields\": [
        \"pattern_id\",
        \"domain\",
        \"created_at\",
        \"expires_at\",
        \"source_domain\",
        \"target_domain\",
        \"transfer_success_rate\"
      ],
      \"optional_fields\": [
        \"usage_count\",
        \"last_used_at\",
        \"researcher_notes\"
      ],
      \"pattern_data_schema\": {
        \"strategy\": \"string\",
        \"key_techniques\": \"array\",
        \"context_factors\": {
          \"field\": \"string\",
          \"methodology\": \"string\",
          \"timeline\": \"string\"
        }
      }
    },
    \"business_research\": {
      \"required_fields\": [
        \"pattern_id\",
        \"domain\",
        \"created_at\",
        \"expires_at\",
        \"source_domain\",
        \"target_domain\",
        \"transfer_success_rate\"
      ],
      \"pattern_data_schema\": {
        \"strategy\": \"string\",
        \"key_techniques\": \"array\",
        \"context_factors\": {
          \"industry\": \"string\",
          \"market_maturity\": \"string\",
          \"timeline\": \"string\"
        }
      }
    },
    \"business_strategy\": {
      \"required_fields\": [
        \"pattern_id\",
        \"domain\",
        \"created_at\",
        \"expires_at\",
        \"source_domain\",
        \"target_domain\",
        \"transfer_success_rate\"
      ],
      \"pattern_data_schema\": {
        \"strategy\": \"string\",
        \"key_techniques\": \"array\",
        \"context_factors\": {
          \"company_stage\": \"string\",
          \"pivot_type\": \"string\",
          \"urgency\": \"string\"
        }
      }
    },
    \"industry\": {
      \"required_fields\": [
        \"pattern_id\",
        \"domain\",
        \"created_at\",
        \"expires_at\",
        \"source_domain\",
        \"target_domain\",
        \"transfer_success_rate\"
      ],
      \"pattern_data_schema\": {
        \"strategy\": \"string\",
        \"key_techniques\": \"array\",
        \"context_factors\": {
          \"regulation_level\": \"string\",
          \"data_sensitivity\": \"string\",
          \"timeline\": \"string\"
        }
      }
    }
  }
}" --namespace "config/patterns/templates"

echo "✓ Pattern templates created for all domains"

# ========================================
# STEP 6: Validation
# ========================================

echo ""
echo "🔍 Validating Pattern Storage System..."

# Check policy
echo "1. Verifying expiry policy..."
npx claude-flow memory retrieve "pattern-expiry-policy" --namespace "config/patterns/expiry" > /dev/null 2>&1 && \
  echo "   ✓ Policy stored" || echo "   ✗ Policy missing"

# Check workflow
echo "2. Verifying recording workflow..."
mcp__ruv-swarm__daa_workflow_create({ id: "test" }) 2>&1 | grep -q "already exists\|created" && \
  echo "   ✓ Workflow functional" || echo "   ✗ Workflow error"

# Check script
echo "3. Verifying expiry checker..."
[ -x docs2/neural-pattern-expiry-checker.js ] && \
  echo "   ✓ Checker script executable" || echo "   ✗ Script not executable"

# Check patterns
echo "4. Verifying sample patterns..."
for ns in "patterns/phd/successful" "patterns/business-research/successful" \
          "patterns/business-strategy/successful" "patterns/industry/successful"; do
  npx claude-flow memory list --namespace "$ns" 2>&1 | grep -q "pattern-" && \
    echo "   ✓ Patterns in $ns" || echo "   ✗ No patterns in $ns"
done

echo ""
echo "✅ TASK-NEURAL-009 Complete"
echo "📦 Deliverables:"
echo "   1. Pattern expiry policy (4 domain types)"
echo "   2. Pattern recording workflow"
echo "   3. Expiry checker script (docs2/neural-pattern-expiry-checker.js)"
echo "   4. Archive automation enabled"
echo "   5. Pattern templates for PhD, Business Research, Business Strategy, Industry"
```

## Deliverables

1. **Pattern Expiry Policy** (config/patterns/expiry namespace)
   - 4 domain-specific expiry rules
   - Auto-archive configuration
   - Check frequency settings

2. **Pattern Recording Workflow** (DAA workflow)
   - Metrics collection step
   - Expiry checking step
   - Archive automation step
   - Pattern storage step
   - Index update step

3. **Expiry Checker Script** (docs2/neural-pattern-expiry-checker.js)
   - Automated expiry scanning
   - Archive migration logic
   - Summary reporting
   - Executable Node.js script

4. **Archive Automation**
   - Automatic pattern archival
   - Original namespace tracking
   - Archive timestamp recording

5. **Pattern Templates** (4 domain types)
   - PhD patterns (180-day expiry)
   - Business Research patterns (90-day expiry)
   - Business Strategy patterns (60-day expiry)
   - Industry patterns (120-day expiry)

## Validation Criteria

- [ ] Pattern expiry policy stored in config/patterns/expiry namespace
- [ ] All 4 domain types have expiry rules defined
- [ ] Pattern recording workflow created with 5 steps
- [ ] Expiry checker script (docs2/neural-pattern-expiry-checker.js) is executable
- [ ] Archive automation enabled (auto_archive: true)
- [ ] Sample patterns stored with created_at and expires_at timestamps
- [ ] Pattern templates define required fields and schema for each domain
- [ ] Archive namespace configured (patterns/archived)

## Success Metrics

- Pattern expiry policy covers all 4 domains
- Expiry checker can scan and archive expired patterns
- Sample patterns include proper timestamp fields
- Templates provide clear schema for each domain type

## Integration Points

### Upstream Dependencies
- **TASK-NEURAL-008**: Knowledge sharing provides patterns to store

### Downstream Dependencies
- **TASK-NEURAL-010**: Meta-learning validator uses stored patterns for transfer validation
- **TASK-NEURAL-011**: User feedback processor stores feedback patterns with expiry
- **TASK-NEURAL-012**: Pattern-based recommendation engine queries active patterns

## Notes

- Expiry dates are domain-specific based on knowledge evolution rates
- Archived patterns are preserved for historical analysis, not deleted
- Expiry checker should be run periodically (weekly or monthly)
- Pattern usage tracking (usage_count, last_used_at) helps identify valuable patterns
- Notification system can warn before pattern expiry for review

## Related Files

- `docs2/neural-pattern-expiry-checker.js` - Automated expiry checker script
- `docs2/neuralenhancement/specs/requirements/REQ-NEURAL-026.md` - Pattern storage requirements
- `docs2/neuralenhancement/specs/requirements/REQ-NEURAL-027.md` - Expiry policy requirements
- `docs2/neuralenhancement/specs/tasks/TASK-NEURAL-008.md` - Knowledge sharing (upstream)
- `docs2/neuralenhancement/specs/tasks/TASK-NEURAL-010.md` - Meta-learning validator (downstream)
