# Progress Tracking Template

## Purpose & Usage

The Progress Tracking template monitors sprint progress, task completion, velocity metrics, and team performance. It provides quantitative insight into development pace and helps identify bottlenecks early.

**When to Use:**
- Sprint planning and execution
- Daily standups and status reports
- Identifying blockers and bottlenecks
- Measuring team velocity
- Reporting to stakeholders

## Template Structure

```markdown
# Progress Tracking: [Sprint/Project Name]

## Sprint Overview
- **Sprint Number**: [#]
- **Sprint Goal**: [Primary objective for this sprint]
- **Start Date**: [YYYY-MM-DD]
- **End Date**: [YYYY-MM-DD]
- **Duration**: [X weeks/days]
- **Team Size**: [# of agents/developers]

## Summary Metrics

### Current Status (as of [YYYY-MM-DD HH:MM])
- **Overall Progress**: [X%] complete
- **Tasks Completed**: [X / Y] ([Z%])
- **Story Points**: [X / Y] ([Z%])
- **Days Remaining**: [X]
- **Projected Completion**: [On track / At risk / Behind schedule]

### Velocity Metrics
- **Current Velocity**: [X] points/day
- **Planned Velocity**: [Y] points/day
- **Variance**: [+/-Z%]
- **Historical Average**: [X] points/day (last 3 sprints)

### Health Indicators
- 🟢 **On Track**: [count] tasks
- 🟡 **At Risk**: [count] tasks (delayed but recoverable)
- 🔴 **Blocked**: [count] tasks (cannot proceed)
- ⚪ **Not Started**: [count] tasks

## Task Breakdown

### Completed Tasks ✅
| ID | Task | Owner | Points | Completed | Duration |
|----|------|-------|--------|-----------|----------|
| T-001 | [Task description] | [Agent] | [pts] | [YYYY-MM-DD] | [Xh] |
| T-002 | [Task description] | [Agent] | [pts] | [YYYY-MM-DD] | [Xh] |

**Total**: [X tasks, Y points, Z hours]

### In Progress Tasks 🔄
| ID | Task | Owner | Points | Progress | Est. Completion | Status |
|----|------|-------|--------|----------|-----------------|--------|
| T-003 | [Task description] | [Agent] | [pts] | [X%] | [YYYY-MM-DD] | 🟢 On track |
| T-004 | [Task description] | [Agent] | [pts] | [X%] | [YYYY-MM-DD] | 🟡 At risk |

**Total**: [X tasks, Y points]

### Blocked Tasks 🚫
| ID | Task | Owner | Points | Blocker | Blocked Since | Impact |
|----|------|-------|--------|---------|---------------|--------|
| T-005 | [Task description] | [Agent] | [pts] | [Blocker description] | [YYYY-MM-DD] | High/Med/Low |

**Total**: [X tasks, Y points]
**Action Required**: [Summary of unblock actions needed]

### Backlog Tasks 📋
| ID | Task | Owner | Points | Priority | Planned Start |
|----|------|-------|--------|----------|---------------|
| T-006 | [Task description] | [Agent] | [pts] | High/Med/Low | [YYYY-MM-DD] |

**Total**: [X tasks, Y points]

## Progress by Category

### Feature Development
- **Total**: [X tasks] ([Y%] complete)
- **Completed**: [A tasks]
- **In Progress**: [B tasks]
- **Blocked**: [C tasks]
- **Remaining**: [D tasks]

### Bug Fixes
- **Total**: [X tasks] ([Y%] complete)
- **Critical**: [A/B] complete
- **High Priority**: [C/D] complete
- **Medium Priority**: [E/F] complete

### Technical Debt
- **Total**: [X tasks] ([Y%] complete)
- **Refactoring**: [A/B] complete
- **Performance**: [C/D] complete
- **Documentation**: [E/F] complete

### Testing
- **Unit Tests**: [X%] coverage ([target: Y%])
- **Integration Tests**: [A/B] complete
- **E2E Tests**: [C/D] complete
- **Performance Tests**: [E/F] complete

## Daily Progress Log

### [YYYY-MM-DD] - Day [X] of Sprint
**Completed**:
- ✅ [Task ID] - [Brief description] ([Agent])
- ✅ [Task ID] - [Brief description] ([Agent])

**Started**:
- 🔄 [Task ID] - [Brief description] ([Agent])

**Blocked**:
- 🚫 [Task ID] - [Blocker] ([Agent])

**Key Events**:
- [Significant event or decision]
- [Blocker resolved]
- [Scope change]

**Metrics**:
- Tasks completed: [X]
- Points earned: [Y]
- Velocity: [Z] pts/day

---

### [YYYY-MM-DD] - Day [X-1] of Sprint
**Completed**:
- ✅ [Task ID] - [Brief description] ([Agent])

[Continue daily logs...]

## Burndown Chart (Text-Based)

```
Story Points Remaining
100 |█
 90 |██
 80 |███
 70 |████
 60 |█████         ← Actual
 50 |██████       /
 40 |███████     /
 30 |████████   /
 20 |█████████ /
 10 |██████████ ← Ideal
  0 |___________
    D1 D2 D3 D4 D5 D6 D7 D8 D9 D10
```

**Interpretation**:
- **Above ideal line**: Behind schedule
- **On ideal line**: On track
- **Below ideal line**: Ahead of schedule

**Current Status**: [Behind/On track/Ahead] by [X] points

## Risk Assessment

### High Risk Items
| Risk | Impact | Probability | Mitigation | Owner |
|------|--------|-------------|------------|-------|
| [Risk description] | High/Med/Low | High/Med/Low | [Mitigation strategy] | [Agent] |

### Scope Changes
| Change | Impact | Approved | Points Impact |
|--------|--------|----------|---------------|
| [Change description] | [Impact description] | Yes/No | +/- [X] pts |

### Dependency Tracking
| Task | Depends On | Status | Risk |
|------|------------|--------|------|
| [Task ID] | [Dependency] | Completed/Pending | 🟢/🟡/🔴 |

## Team Performance

### Agent Performance
| Agent | Completed | In Progress | Points Earned | Avg Task Time | Efficiency |
|-------|-----------|-------------|---------------|---------------|------------|
| [Agent name] | [X tasks] | [Y tasks] | [Z pts] | [Ah] | [B%] |

**Top Performers**: [Agent names and achievements]
**Support Needed**: [Agents needing help]

### Bottleneck Analysis
**Current Bottlenecks**:
1. [Bottleneck description] - Impact: [High/Med/Low]
   - **Cause**: [Root cause]
   - **Resolution**: [Action plan]

2. [Bottleneck description] - Impact: [High/Med/Low]
   - **Cause**: [Root cause]
   - **Resolution**: [Action plan]

### Quality Metrics
- **Defect Rate**: [X] bugs per [Y] tasks
- **Rework Rate**: [X%] of tasks required rework
- **Test Coverage**: [X%] (target: [Y%])
- **Code Review Pass Rate**: [X%]

## Sprint Retrospective (End of Sprint)

### What Went Well ✅
- [Success 1]
- [Success 2]
- [Success 3]

### What Didn't Go Well ❌
- [Challenge 1]
- [Challenge 2]
- [Challenge 3]

### Action Items for Next Sprint
- [ ] [Action item 1] - Owner: [Agent]
- [ ] [Action item 2] - Owner: [Agent]
- [ ] [Action item 3] - Owner: [Agent]

### Velocity Analysis
- **Planned**: [X] points
- **Completed**: [Y] points
- **Efficiency**: [Z%]
- **Trend**: [Improving/Stable/Declining]

## Memory Integration

```bash
# Store sprint progress
npx claude-flow memory store "sprint/[number]/progress" '{
  "sprint_number": [X],
  "progress_percentage": [Y],
  "tasks_completed": [A],
  "tasks_total": [B],
  "velocity": [C],
  "status": "on-track|at-risk|behind",
  "blockers_count": [D],
  "updated_at": "[ISO-timestamp]"
}' --namespace "project/progress"

# Retrieve sprint metrics
npx claude-flow memory retrieve \
  --key "sprint/[number]/progress" \
  --namespace "project/progress"

# Store daily metrics
npx claude-flow memory store "sprint/[number]/day/[date]" '{
  "date": "[YYYY-MM-DD]",
  "tasks_completed": [X],
  "points_earned": [Y],
  "blockers_new": [Z],
  "blockers_resolved": [A]
}' --namespace "project/progress"

# Calculate velocity trend
npx claude-flow memory search \
  --pattern "sprint/.*/progress" \
  --namespace "project/progress" \
  | jq '.[] | .velocity'
```

## Neural Enhancement Integration

```bash
# Train velocity prediction model
npx claude-flow neural train \
  --pattern-type "prediction" \
  --training-data "project/progress" \
  --epochs 50

# Predict sprint completion
npx claude-flow neural predict \
  --model-id "velocity-predictor" \
  --input '{
    "current_velocity": [X],
    "remaining_points": [Y],
    "days_remaining": [Z],
    "blockers_count": [A]
  }'

# Analyze bottlenecks
npx claude-flow bottleneck analyze \
  --component "sprint-execution" \
  --metrics ["velocity", "blocker-count", "completion-rate"]
```
```

## Example Usage

### Full Sprint Tracking

```markdown
# Progress Tracking: Sprint 12 - Neural Enhancement Implementation

## Sprint Overview
- **Sprint Number**: 12
- **Sprint Goal**: Implement core neural enhancement features with 90% test coverage
- **Start Date**: 2025-11-20
- **End Date**: 2025-12-04
- **Duration**: 2 weeks
- **Team Size**: 6 agents (3 coders, 1 tester, 1 reviewer, 1 architect)

## Summary Metrics

### Current Status (as of 2025-11-27 16:00)
- **Overall Progress**: 68% complete
- **Tasks Completed**: 17 / 25 (68%)
- **Story Points**: 82 / 120 (68.3%)
- **Days Remaining**: 5 working days
- **Projected Completion**: 🟢 On track (with buffer)

### Velocity Metrics
- **Current Velocity**: 11.7 points/day
- **Planned Velocity**: 12 points/day
- **Variance**: -2.5%
- **Historical Average**: 10.8 points/day (last 3 sprints)

### Health Indicators
- 🟢 **On Track**: 18 tasks (72%)
- 🟡 **At Risk**: 2 tasks (8%)
- 🔴 **Blocked**: 1 task (4%)
- ⚪ **Not Started**: 4 tasks (16%)

## Task Breakdown

### Completed Tasks ✅
| ID | Task | Owner | Points | Completed | Duration |
|----|------|-------|--------|-----------|----------|
| T-001 | Implement neural pattern recognition service | ml-developer | 8 | 2025-11-21 | 12h |
| T-002 | Create pgvector database schema | code-analyzer | 5 | 2025-11-21 | 6h |
| T-003 | Build vector embedding API endpoints | coder | 5 | 2025-11-22 | 7h |
| T-004 | Implement training data ingestion pipeline | backend-dev | 8 | 2025-11-23 | 10h |
| T-005 | Create model checkpoint storage system | backend-dev | 5 | 2025-11-23 | 5h |
| T-006 | Write unit tests for pattern recognition | tester | 3 | 2025-11-24 | 4h |
| T-007 | Implement similarity search API | coder | 5 | 2025-11-24 | 6h |
| T-008 | Create neural config management | system-architect | 3 | 2025-11-25 | 3h |
| T-009 | Write integration tests for embedding API | tester | 5 | 2025-11-25 | 7h |
| T-010 | Implement model versioning system | backend-dev | 5 | 2025-11-26 | 5h |
| T-011 | Create monitoring dashboards | perf-analyzer | 3 | 2025-11-26 | 4h |
| T-012 | Write E2E tests for training pipeline | tester | 8 | 2025-11-27 | 9h |
| T-013 | Implement batch inference API | coder | 5 | 2025-11-27 | 6h |
| T-014 | Create model performance benchmarks | performance-benchmarker | 3 | 2025-11-27 | 3h |
| T-015 | Document neural API endpoints | api-docs | 3 | 2025-11-27 | 3h |
| T-016 | Code review: pattern recognition | reviewer | 2 | 2025-11-27 | 2h |
| T-017 | Code review: embedding API | reviewer | 2 | 2025-11-27 | 2h |

**Total**: 17 tasks, 82 points, 94 hours

### In Progress Tasks 🔄
| ID | Task | Owner | Points | Progress | Est. Completion | Status |
|----|------|-------|--------|----------|-----------------|--------|
| T-018 | Implement model auto-tuning | ml-developer | 8 | 60% | 2025-11-28 | 🟢 On track |
| T-019 | Create performance optimization suite | perf-analyzer | 5 | 40% | 2025-11-29 | 🟡 At risk (complexity) |
| T-020 | Write security audit for neural endpoints | security-auditor | 3 | 30% | 2025-11-28 | 🟢 On track |

**Total**: 3 tasks, 16 points

### Blocked Tasks 🚫
| ID | Task | Owner | Points | Blocker | Blocked Since | Impact |
|----|------|-------|--------|---------|---------------|--------|
| T-021 | Deploy neural services to staging | cicd-engineer | 5 | Waiting on infrastructure approval | 2025-11-26 | Medium |

**Total**: 1 task, 5 points
**Action Required**: Follow up with DevOps for infrastructure approval (expected today)

### Backlog Tasks 📋
| ID | Task | Owner | Points | Priority | Planned Start |
|----|------|-------|--------|----------|---------------|
| T-022 | Implement neural cache invalidation | backend-dev | 3 | Medium | 2025-11-28 |
| T-023 | Create model rollback mechanism | system-architect | 5 | High | 2025-11-29 |
| T-024 | Write load tests for inference API | tester | 5 | High | 2025-11-30 |
| T-025 | Final integration testing | tester | 4 | Critical | 2025-12-01 |

**Total**: 4 tasks, 17 points

## Progress by Category

### Feature Development
- **Total**: 15 tasks (73% complete)
- **Completed**: 11 tasks
- **In Progress**: 2 tasks
- **Blocked**: 1 task
- **Remaining**: 1 task

### Bug Fixes
- **Total**: 0 tasks (N/A - greenfield development)

### Technical Debt
- **Total**: 2 tasks (50% complete)
- **Refactoring**: 1/1 complete (config management)
- **Performance**: 0/1 complete (optimization suite in progress)

### Testing
- **Unit Tests**: 92% coverage (target: 90%) ✅
- **Integration Tests**: 3/4 complete
- **E2E Tests**: 1/2 complete
- **Performance Tests**: 1/1 complete (benchmarks)

## Daily Progress Log

### 2025-11-27 - Day 6 of Sprint
**Completed**:
- ✅ T-012 - E2E tests for training pipeline (tester) - 8 pts
- ✅ T-013 - Batch inference API (coder) - 5 pts
- ✅ T-014 - Model performance benchmarks (performance-benchmarker) - 3 pts
- ✅ T-015 - API documentation (api-docs) - 3 pts
- ✅ T-016 - Code review: pattern recognition (reviewer) - 2 pts
- ✅ T-017 - Code review: embedding API (reviewer) - 2 pts

**Started**:
- 🔄 T-018 - Model auto-tuning (ml-developer) - 8 pts (60% complete)
- 🔄 T-019 - Performance optimization suite (perf-analyzer) - 5 pts (40% complete)
- 🔄 T-020 - Security audit (security-auditor) - 3 pts (30% complete)

**Blocked**:
- 🚫 T-021 - Staging deployment still waiting on infrastructure

**Key Events**:
- Performance benchmarks exceeded targets (50ms vs 100ms target for similarity search)
- API documentation complete and reviewed
- Security auditor identified minor issue in token validation (fixing today)

**Metrics**:
- Tasks completed: 6
- Points earned: 23
- Velocity: 13.8 pts/day (above plan!)

---

### 2025-11-26 - Day 5 of Sprint
**Completed**:
- ✅ T-010 - Model versioning system (backend-dev) - 5 pts
- ✅ T-011 - Monitoring dashboards (perf-analyzer) - 3 pts

**Started**:
- 🔄 T-012 - E2E tests for training pipeline (tester)

**Blocked**:
- 🚫 T-021 - Staging deployment blocked on infrastructure approval

**Key Events**:
- Versioning system supports backward compatibility
- Monitoring dashboards integrated with Grafana

**Metrics**:
- Tasks completed: 2
- Points earned: 8
- Velocity: 11.4 pts/day

## Burndown Chart (Text-Based)

```
Story Points Remaining
120|█
110|██
100|███
 90|████
 80|█████
 70|██████
 60|███████
 50|████████      Actual ↓
 40|█████████       38 pts
 30|██████████     /
 20|███████████   /
 10|████████████ /  Ideal ↓
  0|____________/_____ 24 pts
    D1 D2 D3 D4 D5 D6 D7 D8 D9 D10
```

**Interpretation**:
- **Status**: Ahead of schedule by 14 points
- **Trend**: Velocity increasing (avg 11.7 vs planned 12)
- **Projection**: Sprint completion 1 day early with current velocity

**Current Status**: 🟢 Ahead by 14 points (buffer for unexpected issues)

## Risk Assessment

### High Risk Items
| Risk | Impact | Probability | Mitigation | Owner |
|------|--------|-------------|------------|-------|
| Infrastructure approval delay | Medium | Medium | Daily follow-up with DevOps; prepare local testing alternative | cicd-engineer |
| Performance optimization complexity | Low | High | Allocate ml-developer as backup if needed | perf-analyzer |

### Scope Changes
| Change | Impact | Approved | Points Impact |
|--------|--------|----------|---------------|
| Add model rollback mechanism | Enhanced reliability for production | Yes | +5 pts (added to backlog) |

### Dependency Tracking
| Task | Depends On | Status | Risk |
|------|------------|--------|------|
| T-021 (Staging deploy) | Infrastructure approval | Pending | 🟡 Medium |
| T-024 (Load tests) | T-021 (Staging env) | Pending | 🟢 Low (can test locally) |
| T-025 (Integration test) | All features complete | On track | 🟢 Low |

## Team Performance

### Agent Performance
| Agent | Completed | In Progress | Points Earned | Avg Task Time | Efficiency |
|-------|-----------|-------------|---------------|---------------|------------|
| backend-dev | 3 tasks | 0 tasks | 18 pts | 6.7h | 105% |
| coder | 2 tasks | 0 tasks | 10 pts | 6.5h | 98% |
| ml-developer | 1 task | 1 task | 8 pts | 12h | 90% |
| tester | 3 tasks | 0 tasks | 16 pts | 6.7h | 102% |
| reviewer | 2 tasks | 0 tasks | 4 pts | 2h | 110% |
| perf-analyzer | 1 task | 1 task | 3 pts | 4h | 95% |

**Top Performers**: reviewer (110% efficiency), backend-dev (105% efficiency)
**Support Needed**: ml-developer on T-018 (complexity higher than estimated)

### Bottleneck Analysis
**Current Bottlenecks**:
1. Infrastructure approval process - Impact: Medium
   - **Cause**: External dependency on DevOps team availability
   - **Resolution**: Daily standup with DevOps; alternative local testing prepared

2. Performance optimization complexity - Impact: Low
   - **Cause**: More edge cases than initially estimated
   - **Resolution**: ml-developer allocated as backup for Day 7 if needed

### Quality Metrics
- **Defect Rate**: 0.2 bugs per task (excellent)
- **Rework Rate**: 5% (1 task needed minor revision)
- **Test Coverage**: 92% (exceeds target of 90%)
- **Code Review Pass Rate**: 94% (very good)

## Memory Integration

```bash
# Store sprint progress
npx claude-flow memory store "sprint/12/progress" '{
  "sprint_number": 12,
  "progress_percentage": 68,
  "tasks_completed": 17,
  "tasks_total": 25,
  "velocity": 11.7,
  "status": "ahead",
  "blockers_count": 1,
  "updated_at": "2025-11-27T16:00:00Z"
}' --namespace "project/progress"

# Store daily metrics
npx claude-flow memory store "sprint/12/day/2025-11-27" '{
  "date": "2025-11-27",
  "tasks_completed": 6,
  "points_earned": 23,
  "blockers_new": 0,
  "blockers_resolved": 0,
  "velocity": 13.8
}' --namespace "project/progress"
```

## Neural Enhancement Integration

```bash
# Predict sprint completion
npx claude-flow neural predict \
  --model-id "velocity-predictor" \
  --input '{
    "current_velocity": 11.7,
    "remaining_points": 38,
    "days_remaining": 5,
    "blockers_count": 1
  }'

# Output: Predicted completion in 3.2 days (1.8 days early)
```
```

## Integration Points

### 1. Memory System Integration
```bash
# Auto-update progress every hour
npx claude-flow hooks post-task \
  --task-id "T-XXX" \
  --update-progress true

# Retrieve velocity trends
npx claude-flow memory search \
  --pattern "sprint/.*/day/.*" \
  --namespace "project/progress"

# Compare sprint performance
npx claude-flow memory retrieve \
  --key "sprint/*/progress" \
  --namespace "project/progress"
```

### 2. Active Context Integration
- Current sprint status shown in active context
- Blockers from progress tracking appear in active context
- Velocity informs task estimates in active context

### 3. Decision Log Integration
- Scope changes documented as decisions
- Risk mitigations may trigger decision entries
- Retrospective findings inform future decisions

### 4. Session Restoration Integration
- Sprint state restored on session start
- Daily progress provides context for resumed work
- Blockers highlighted for immediate attention

## Best Practices

### ✅ DO
- **Update daily** (minimum once per day, ideally after standup)
- **Track actual vs estimated** time for learning
- **Document blockers immediately** (don't wait for standup)
- **Celebrate wins** (acknowledge completed milestones)
- **Use consistent metrics** (points, hours, completion %)
- **Analyze trends** (velocity, quality, bottlenecks)
- **Store in memory** for historical analysis
- **Update burndown** daily for visual tracking
- **Record retrospective findings** at sprint end
- **Link to tasks** in other documents (specs, decisions)

### ❌ DON'T
- **Don't update only at sprint end** (stale data is useless)
- **Don't hide problems** (surface blockers early)
- **Don't ignore velocity trends** (declining velocity = problem)
- **Don't skip retrospectives** (learning opportunity lost)
- **Don't change metrics mid-sprint** (consistency matters)
- **Don't blame individuals** (focus on process improvement)
- **Don't forget to archive** (keep only current sprint active)
- **Don't set unrealistic velocity** (use historical average)

### Velocity Calculation

```
Velocity = Total Story Points Completed / Days Elapsed

Example:
82 points completed / 7 days = 11.7 points/day

Projected Completion = Remaining Points / Current Velocity
38 points / 11.7 pts/day = 3.2 days
```

### Burndown Chart Interpretation

- **Steep drop**: High productivity day
- **Flat line**: No progress (investigate blockers)
- **Above ideal line**: Behind schedule (need acceleration)
- **Below ideal line**: Ahead of schedule (good buffer)
- **Irregular pattern**: Inconsistent velocity (smooth it out)

### Status Indicators

- 🟢 **On Track**: <= 10% variance from plan, no blockers
- 🟡 **At Risk**: 10-25% variance or minor blockers, recoverable
- 🔴 **Blocked**: > 25% variance or critical blockers, needs escalation
- ⚪ **Not Started**: In backlog, planned for future

## Performance Optimization

- **Archive completed sprints** to separate files
- **Keep only last 7 days** of detailed daily logs
- **Summarize older data** (monthly/quarterly rollups)
- **Index by sprint number** for O(1) lookup
- **Cache current sprint** in memory for fast access
- **Automate metric calculation** via hooks

---

**Template Version**: 1.0.0
**Last Updated**: 2025-11-27
**Maintained By**: Claude Flow Blueprint Project
