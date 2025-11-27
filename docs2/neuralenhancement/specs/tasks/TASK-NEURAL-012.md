# TASK-NEURAL-012: Performance Degradation Detector

## Metadata
- **Task ID**: TASK-NEURAL-012
- **Title**: Performance Degradation Detection and Monitoring
- **Implements Requirements**: REQ-NEURAL-38, REQ-NEURAL-39, REQ-NEURAL-40, REQ-NEURAL-41
- **Dependencies**: TASK-NEURAL-011 (Continuous Improvement Hooks)
- **Complexity**: MEDIUM
- **Estimated Time**: 25 minutes
- **Status**: PENDING

## Context

Performance degradation detection is critical for maintaining the effectiveness of neural enhancement over time. As patterns evolve and hooks execute continuously, there's a risk that performance may degrade due to stale patterns, hook failures, or ineffective learning strategies. Without automated monitoring, teams might not notice declining performance until productivity suffers significantly.

This task builds on TASK-011's continuous improvement hooks by monitoring the metrics they collect. It establishes performance baselines, tracks pattern strength trends from TASK-009's expiry system, and monitors hook execution success rates. The detector compares current performance against historical baselines to identify degradation early, enabling proactive intervention before problems compound.

By implementing automated alerting and response workflows, this task closes the feedback loop for neural enhancement. It prepares the foundation for TASK-013's multi-project monitoring by establishing per-project isolation patterns and degradation detection strategies that scale across concurrent workflows.

## Objectives

1. Create performance baseline capture system
2. Implement pattern strength degradation detection
3. Build hook execution monitoring
4. Create automated alerting system
5. Design degradation response workflows
6. Enable trend analysis and prediction

## Pseudo-code

```bash
# ========================================
# STEP 1: Capture Performance Baseline
# ========================================

# Retrieve current metrics from TASK-011 hooks
HOOK_METRICS=$(npx claude-flow memory retrieve --key "hook-metrics" --namespace "projects/$PROJECT_ID/hooks")
PATTERN_STRENGTH=$(npx claude-flow memory retrieve --key "pattern-strength-baseline" --namespace "projects/$PROJECT_ID/patterns")

# Store baseline
npx claude-flow memory store "performance-baseline" "{
  \"project_id\": \"$PROJECT_ID\",
  \"captured_at\": \"$(date -Iseconds)\",
  \"metrics\": {
    \"hook_success_rate\": 0.88,
    \"pattern_strength_avg\": 0.82,
    \"task_completion_time_avg\": 180,
    \"pattern_reinforcement_rate\": 0.75
  },
  \"thresholds\": {
    \"hook_success_rate_min\": 0.70,
    \"pattern_strength_min\": 0.65,
    \"completion_time_max_increase\": 1.5,
    \"pattern_reinforcement_min\": 0.60
  },
  \"monitoring_frequency_minutes\": 15
}" --namespace "projects/$PROJECT_ID/performance"

echo "✓ Performance baseline captured"

# ========================================
# STEP 2: Create Degradation Detection System
# ========================================

cat > docs2/neural-degradation-detector.js << 'EOF'
#!/usr/bin/env node
/**
 * Performance Degradation Detector
 * Monitors hook metrics and pattern strength for degradation
 */

const { execSync } = require('child_process');

function retrieveMemory(key, namespace) {
  try {
    const result = execSync(
      `npx claude-flow memory retrieve --key "${key}" --namespace "${namespace}"`,
      { encoding: 'utf-8' }
    );
    return JSON.parse(result);
  } catch (error) {
    console.error(`Failed to retrieve ${key}: ${error.message}`);
    return null;
  }
}

function detectDegradation(baseline, current) {
  const degradations = [];

  // Check hook success rate
  if (current.hook_success_rate < baseline.thresholds.hook_success_rate_min) {
    degradations.push({
      type: 'hook_failure_rate',
      severity: 'HIGH',
      baseline: baseline.metrics.hook_success_rate,
      current: current.hook_success_rate,
      threshold: baseline.thresholds.hook_success_rate_min,
      recommendation: 'Check hook configuration and ReasoningBank connectivity'
    });
  }

  // Check pattern strength
  if (current.pattern_strength_avg < baseline.thresholds.pattern_strength_min) {
    degradations.push({
      type: 'pattern_strength_decline',
      severity: 'MEDIUM',
      baseline: baseline.metrics.pattern_strength_avg,
      current: current.pattern_strength_avg,
      threshold: baseline.thresholds.pattern_strength_min,
      recommendation: 'Review pattern expiry policy (TASK-009) and reinforcement workflow'
    });
  }

  // Check task completion time
  const timeIncrease = current.task_completion_time_avg / baseline.metrics.task_completion_time_avg;
  if (timeIncrease > baseline.thresholds.completion_time_max_increase) {
    degradations.push({
      type: 'performance_slowdown',
      severity: 'MEDIUM',
      baseline: baseline.metrics.task_completion_time_avg,
      current: current.task_completion_time_avg,
      increase_factor: timeIncrease,
      threshold: baseline.thresholds.completion_time_max_increase,
      recommendation: 'Run bottleneck analysis: npx claude-flow analysis bottleneck-detect'
    });
  }

  // Check pattern reinforcement rate
  if (current.pattern_reinforcement_rate < baseline.thresholds.pattern_reinforcement_min) {
    degradations.push({
      type: 'reinforcement_decline',
      severity: 'LOW',
      baseline: baseline.metrics.pattern_reinforcement_rate,
      current: current.pattern_reinforcement_rate,
      threshold: baseline.thresholds.pattern_reinforcement_min,
      recommendation: 'Verify post-task hook executing correctly'
    });
  }

  return degradations;
}

async function monitorPerformance(projectId) {
  console.log('🔍 Starting performance degradation monitoring...');

  // Load baseline
  const baseline = retrieveMemory('performance-baseline', `projects/${projectId}/performance`);
  if (!baseline) {
    console.error('❌ No baseline found. Run TASK-012 Step 1 first.');
    return;
  }

  // Get current metrics from hooks
  const currentMetrics = retrieveMemory('hook-metrics', `projects/${projectId}/hooks`);
  if (!currentMetrics) {
    console.warn('⚠️  No current metrics available yet');
    return;
  }

  // Detect degradation
  const degradations = detectDegradation(baseline, currentMetrics);

  if (degradations.length === 0) {
    console.log('✅ No performance degradation detected');
    return;
  }

  // Report degradations
  console.log(`\n⚠️  Detected ${degradations.length} performance issue(s):\n`);
  degradations.forEach((d, i) => {
    console.log(`${i + 1}. [${d.severity}] ${d.type}`);
    console.log(`   Baseline: ${d.baseline}`);
    console.log(`   Current: ${d.current}`);
    console.log(`   Threshold: ${d.threshold}`);
    console.log(`   Action: ${d.recommendation}\n`);
  });

  // Store degradation report
  execSync(`npx claude-flow memory store "degradation-report-${Date.now()}" '${JSON.stringify({
    project_id: projectId,
    detected_at: new Date().toISOString(),
    degradation_count: degradations.length,
    issues: degradations
  })}' --namespace "projects/${projectId}/performance/alerts"`);

  return degradations;
}

// Run if called directly
if (require.main === module) {
  const projectId = process.argv[2] || 'neural-impl-default';
  monitorPerformance(projectId)
    .then(() => process.exit(0))
    .catch(err => {
      console.error('Monitoring failed:', err);
      process.exit(1);
    });
}

module.exports = { monitorPerformance, detectDegradation };
EOF

chmod +x docs2/neural-degradation-detector.js
echo "✓ Degradation detector script created"

# ========================================
# STEP 3: Create Monitoring Workflow
# ========================================

npx claude-flow memory store "performance-monitoring-workflow" "{
  \"workflow_id\": \"performance-monitoring-workflow\",
  \"name\": \"Continuous Performance Monitoring\",
  \"project_id\": \"$PROJECT_ID\",
  \"steps\": [
    {
      \"id\": \"collect-current-metrics\",
      \"agent\": \"performance-monitor\",
      \"action\": \"Collect current hook metrics and pattern strength\",
      \"timeout\": 60
    },
    {
      \"id\": \"run-degradation-check\",
      \"agent\": \"performance-monitor\",
      \"action\": \"Execute degradation detector script\",
      \"depends_on\": [\"collect-current-metrics\"]
    },
    {
      \"id\": \"analyze-trends\",
      \"agent\": \"performance-monitor\",
      \"action\": \"Analyze performance trends over time\",
      \"depends_on\": [\"run-degradation-check\"]
    },
    {
      \"id\": \"alert-if-degraded\",
      \"agent\": \"performance-monitor\",
      \"action\": \"Send alerts if thresholds breached\",
      \"depends_on\": [\"analyze-trends\"]
    }
  ],
  \"strategy\": \"sequential\",
  \"schedule\": \"every_15_minutes\",
  \"enabled\": true
}" --namespace "projects/$PROJECT_ID/workflows"

echo "✓ Monitoring workflow created"

# ========================================
# STEP 4: Create Alerting System
# ========================================

npx claude-flow memory store "alerting-config" "{
  \"project_id\": \"$PROJECT_ID\",
  \"enabled\": true,
  \"channels\": [
    {
      \"type\": \"memory\",
      \"namespace\": \"projects/$PROJECT_ID/performance/alerts\",
      \"enabled\": true
    },
    {
      \"type\": \"console\",
      \"enabled\": true,
      \"severity_threshold\": \"MEDIUM\"
    }
  ],
  \"alert_rules\": [
    {
      \"metric\": \"hook_success_rate\",
      \"condition\": \"below_threshold\",
      \"threshold\": 0.70,
      \"severity\": \"HIGH\",
      \"message\": \"Hook success rate below 70% - check ReasoningBank connectivity\"
    },
    {
      \"metric\": \"pattern_strength_avg\",
      \"condition\": \"below_threshold\",
      \"threshold\": 0.65,
      \"severity\": \"MEDIUM\",
      \"message\": \"Pattern strength declining - review reinforcement workflow\"
    },
    {
      \"metric\": \"task_completion_time\",
      \"condition\": \"increased_by\",
      \"factor\": 1.5,
      \"severity\": \"MEDIUM\",
      \"message\": \"Task completion time increased 50% - run bottleneck analysis\"
    }
  ],
  \"alert_frequency_minutes\": 30
}" --namespace "projects/$PROJECT_ID/performance"

echo "✓ Alerting system configured"

# ========================================
# STEP 5: Test Degradation Detection
# ========================================

# Run degradation detector with current PROJECT_ID
node docs2/neural-degradation-detector.js "$PROJECT_ID"

# Verify alerts stored
npx claude-flow memory list --namespace "projects/$PROJECT_ID/performance/alerts"

echo "✓ Degradation detection tested"

# ========================================
# STEP 6: Create Response Workflows
# ========================================

npx claude-flow memory store "degradation-response-workflows" "{
  \"project_id\": \"$PROJECT_ID\",
  \"workflows\": {
    \"hook_failure\": {
      \"steps\": [
        \"Check ReasoningBank status: npx claude-flow agent memory status\",
        \"Verify hook configuration: retrieve hook-config\",
        \"Re-run hook setup from TASK-011\",
        \"Test hooks individually\",
        \"Monitor for 30 minutes\"
      ],
      \"automation_level\": \"semi-automatic\"
    },
    \"pattern_strength_decline\": {
      \"steps\": [
        \"Review pattern expiry policy from TASK-009\",
        \"Check if too many patterns expired recently\",
        \"Verify pattern reinforcement workflow running\",
        \"Increase reinforcement frequency if needed\",
        \"Re-baseline pattern strength\"
      ],
      \"automation_level\": \"manual\"
    },
    \"performance_slowdown\": {
      \"steps\": [
        \"Run bottleneck analysis: npx claude-flow analysis bottleneck-detect\",
        \"Check token usage: npx claude-flow analysis token-usage --breakdown\",
        \"Review agent coordination topology\",
        \"Consider topology optimization\",
        \"Monitor after changes\"
      ],
      \"automation_level\": \"semi-automatic\"
    }
  }
}" --namespace "projects/$PROJECT_ID/performance"

echo "✓ Response workflows defined"

# ========================================
# STEP 7: Store Task Completion
# ========================================

npx claude-flow memory store "task-012-complete" "{
  \"task_id\": \"TASK-NEURAL-012\",
  \"status\": \"completed\",
  \"completed_at\": \"$(date -Iseconds)\",
  \"monitoring_enabled\": true,
  \"next_task\": \"TASK-NEURAL-013\",
  \"for_next_agent\": {
    \"task_013_needs\": \"Per-project monitoring patterns, isolation strategies\",
    \"memory_keys\": [
      \"projects/$PROJECT_ID/performance/baseline\",
      \"projects/$PROJECT_ID/performance/alerts\",
      \"degradation-detector-script: docs2/neural-degradation-detector.js\"
    ],
    \"monitoring_patterns\": \"Use this task's detector script with PROJECT_ID isolation\"
  }
}" --namespace "projects/$PROJECT_ID/implementation"

echo "========================================="
echo "TASK-NEURAL-012 COMPLETED"
echo "Performance monitoring active"
echo "Degradation detector: docs2/neural-degradation-detector.js"
echo "Next: TASK-NEURAL-013 (Concurrent Project Isolation)"
echo "========================================="
```

## Validation Criteria

1. ✅ Performance baseline captured with all key metrics
2. ✅ Degradation detector script created and executable
3. ✅ Monitoring workflow configured with 15-minute frequency
4. ✅ Alerting system configured with severity thresholds
5. ✅ Test run detects degradation correctly
6. ✅ Response workflows defined for all degradation types
7. ✅ Task completion record stored with forward-looking context

## Test Commands

```bash
# Test baseline retrieval
npx claude-flow memory retrieve --key "performance-baseline" --namespace "projects/$PROJECT_ID/performance"

# Run degradation detector manually
node docs2/neural-degradation-detector.js "$PROJECT_ID"

# Check for alerts
npx claude-flow memory list --namespace "projects/$PROJECT_ID/performance/alerts"

# Verify alerting config
npx claude-flow memory retrieve --key "alerting-config" --namespace "projects/$PROJECT_ID/performance"

# Check response workflows
npx claude-flow memory retrieve --key "degradation-response-workflows" --namespace "projects/$PROJECT_ID/performance"

# Verify task completion
npx claude-flow memory retrieve --key "task-012-complete" --namespace "projects/$PROJECT_ID/implementation"
```

## Forward-Looking Context

### For TASK-NEURAL-013 (Concurrent Project Isolation)

**Memory Locations to Retrieve**:
- `projects/$PROJECT_ID/performance/baseline` - Baseline metrics per project
- `projects/$PROJECT_ID/performance/alerts` - Alert history per project
- `degradation-detector.js` - Script that uses PROJECT_ID for isolation

**What TASK-013 Needs**:
1. Per-project monitoring patterns established here
2. Degradation detector that accepts PROJECT_ID parameter
3. Isolated performance namespaces
4. Alert routing per project

**How TASK-013 Uses This**:
```bash
# Each project gets isolated monitoring
node docs2/neural-degradation-detector.js "project-A"
node docs2/neural-degradation-detector.js "project-B"

# Alerts stored per project
projects/project-A/performance/alerts
projects/project-B/performance/alerts
```

**Critical for TASK-013**:
- All memory namespaces use PROJECT_ID
- Degradation detector script is project-aware
- Baselines captured per project
- No cross-project metric contamination

## Troubleshooting

**Issue**: No baseline found when running detector
**Solution**: Run Step 1 first to capture baseline: `npx claude-flow memory retrieve --key "performance-baseline"...`

**Issue**: Degradation detector script fails to execute
**Solution**: Verify Node.js installed, script has execute permissions: `chmod +x docs2/neural-degradation-detector.js`

**Issue**: Memory retrieval fails in detector script
**Solution**: Check ReasoningBank status: `npx claude-flow agent memory status`. Verify PROJECT_ID correct.

**Issue**: No current metrics available
**Solution**: Ensure TASK-011 hooks are running and collecting metrics. Wait 15 minutes for first collection cycle.

**Issue**: All metrics show degradation immediately
**Solution**: Re-capture baseline - may have been captured during anomaly: `projects/$PROJECT_ID/performance/baseline`

**Issue**: Alerts not appearing in memory
**Solution**: Verify alerting-config enabled: true. Check namespace spelling matches detector script.

**Issue**: False positives in degradation detection
**Solution**: Adjust thresholds in performance-baseline. Consider increasing monitoring frequency for better sampling.

**Issue**: Script cannot parse JSON from memory
**Solution**: Verify memory stores using correct syntax (positional args). Check for JSON formatting errors.

## Success Indicators

When complete, you should see:
1. ✅ Performance baseline stored with 4 key metrics
2. ✅ Degradation detector script created (docs2/neural-degradation-detector.js)
3. ✅ Script executes without errors
4. ✅ Monitoring workflow scheduled every 15 minutes
5. ✅ Alerting system configured with severity levels
6. ✅ Test detection identifies issues correctly
7. ✅ Response workflows defined for 3 degradation types
8. ✅ Task completion record with TASK-013 handoff
9. ✅ All memory stored in correct PROJECT_ID namespaces
10. ✅ Ready for multi-project isolation in TASK-013

## Dependencies for Next Tasks

- **TASK-013**: Needs per-project monitoring patterns, degradation detector with PROJECT_ID isolation, alert routing strategies
