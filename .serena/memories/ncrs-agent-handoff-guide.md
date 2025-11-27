# NCRS Agent Handoff Guide - From Agent #1 to Subsequent Agents

## Workflow Context
- Agent #1: Current State Mapping (COMPLETE)
- Agent #2: Memory Cleanup (next)
- Agent #3: Documentation Synthesis
- Agent #4: Verification
- Agents #5-7: (downstream)

## How to Retrieve Baseline Data

### Reading Agent #1 Findings

#### Option 1: Read Memory Files (Recommended)
```bash
# Get comprehensive overview
npx serena read-memory ncrs-current-state-baseline

# Get detailed file inventory
npx serena read-memory ncrs-file-inventory-detailed

# Get agent handoff guidance
npx serena read-memory ncrs-agent-handoff-guide
```

#### Option 2: Read Documentation File
```bash
cat /home/cabdru/newdemo/docs/current-state-inventory.md
```

## Key File Locations

### For Memory Cleanup Agent (#2)
**Purpose**: Clean up old data and cache files

Files to clean:
- Cache: /home/cabdru/newdemo/data/.cache/
- Model cache: /home/cabdru/newdemo/models/Qwen*/.cache/
- Temp queries: /home/cabdru/newdemo/temp_queries/ (11 directories)
- Build artifacts: /home/cabdru/newdemo/.mypy_cache/, .pytest_cache/
- Old logs: /home/cabdru/newdemo/logs/worker_errors/

Files to keep (with analysis):
- All .py files in ncrs/ (202 files)
- All test files (53 files)
- Frontend files (157 .ts/.tsx files)
- docs/ and docs2/ (33 markdown files)
- Database files (query_tracking.db, memory.db)

Inventory location: /home/cabdru/newdemo/docs/current-state-inventory.md (Backend Structure → Baseline Metrics)

### For Documentation Agent (#3)
**Purpose**: Synthesize architecture documentation

Key sources:
- docs2/WORKFLOW.md (55 KB) - Workflow documentation
- docs2/API_GUIDE.md (35 KB) - API endpoints
- docs2/coreidea.md (15.8 KB) - Core architecture
- README.md (12.2 KB) - Project overview
- BRIAN2_FIX_SUMMARY.md - Brian2 optimizations

Workflow stage details:
- Location: /home/cabdru/newdemo/src/api/routes/classify/
- Files: workflow_stage_*.py (4 files, 1,272 LOC total)

Architecture overview in inventory: /home/cabdru/newdemo/docs/current-state-inventory.md (Technology Stack section)

### For Verification Agent (#4)
**Purpose**: Verify all components work correctly

Test suite location: /home/cabdru/newdemo/tests/
- 53 Python test files
- Categories: unit/, integration/, regression/, network_builder/, load/, standalone/, verification/

Workflow stages to verify:
1. workflow_stage_seeds.py (350 LOC)
2. workflow_stage_hyde.py (238 LOC)
3. workflow_stage_multihop_init.py (207 LOC)
4. workflow_stage_multihop_loop.py (477 LOC)

Critical modules to test:
- ncrs/facade_core.py (492 LOC) - Main entry point
- ncrs/multi_path_controller/parallel/parallel_snn_runner.py (2,290 LOC) - Parallel execution
- ncrs/facade_workflow.py (631 LOC) - Workflow orchestration

Database to verify: /home/cabdru/newdemo/data/query_tracking.db

### For Downstream Agents (#5-7)
**Purpose**: Use baseline for feature implementation

Git baseline:
- Branch: snnupgrade
- Latest commit: c501348 (streaming collection)
- 10+ recent commits available

Modified files (not staged):
- .gitignore
- docs2/claudeflow.md
- ncrs/facade_core.py
- ncrs/multi_path_controller/parallel/parallel_snn_runner.py

Key metrics for planning:
- Backend: 202 files, 8,105 LOC
- Frontend: 157 files
- Tests: 53 files
- Pipeline stages: 6 (classification, seeds, SNN hops, synthesis)
- Multi-path K: 3 concurrent paths

## Critical Paths for Future Work

### Path 1: Backend Enhancements
```
modify: ncrs/facade_core.py (492 LOC)
modify: ncrs/facade_workflow.py (631 LOC)
modify: ncrs/multi_path_controller/parallel/parallel_snn_runner.py (2,290 LOC)
test: tests/integration/multihop/ (integration tests)
```

### Path 2: API Endpoint Improvements
```
modify: src/api/routes/classify/workflow_stage_*.py (1,272 LOC)
modify: src/api/routes/classify/endpoint.py
test: tests/integration/hyde_e2e/ (end-to-end tests)
```

### Path 3: Frontend Enhancements
```
modify: src/web/src/components/ (15 subdirs, 157 files total)
modify: src/web/src/stores/ (state management)
modify: src/web/src/pages/ (page components)
test: src/web/ (frontend tests)
```

### Path 4: Documentation
```
create/modify: docs/ and docs2/ (33 files)
reference: /home/cabdru/newdemo/docs/current-state-inventory.md
sync: docs2/claudeflow.md with latest Claude Flow
```

## Database & Configuration

### Active Databases
- /home/cabdru/newdemo/data/query_tracking.db (SQLite query tracking)
- /home/cabdru/newdemo/.swarm/memory.db (Swarm memory)

### Configuration Files
- pyproject.toml: Python 3.11+, Brian2 2.9.0
- src/web/package.json: React 19.2.0, Three.js, Vite
- .env: Environment variables
- .claude/: Claude Code agent definitions

### Build & Test Commands
```bash
npm run build          # Build frontend
npm run test           # Run tests
npm run lint          # Lint code
pytest                # Run Python tests
mypy                  # Type checking
```

## Success Metrics for Next Agents

### Agent #2 (Memory Cleanup)
- Files cleaned: temp_queries/, .cache/, logs/
- Preservation verified: 202+53+157 code files intact
- Size reduction reported

### Agent #3 (Documentation)
- Docs synthesized: 33 files → coherent guide
- Architecture documented: 6-step pipeline clear
- API documented: 4 workflow stages detailed

### Agent #4 (Verification)
- Tests passing: all 53 test files
- Workflow stages working: 4/4 endpoints functional
- Database integrity: query_tracking.db valid

### Agents #5-7 (Implementation)
- Code organized: modules < 500 LOC
- Tests updated: new tests for changes
- Docs updated: corresponding documentation
- Git tracked: clean commits with messages

## Emergency References

If lost, retrieve baseline from:
1. Memory files (Serena): ncrs-current-state-baseline
2. Documentation: /home/cabdru/newdemo/docs/current-state-inventory.md
3. Git: git log --oneline -10 (shows commit history)
4. Git: git status (shows modified files)

---

## CRITICAL: Absolute File Paths

All paths in this guide are absolute. Never use relative paths in agent-to-agent communication.

Example: 
- CORRECT: /home/cabdru/newdemo/ncrs/facade_core.py
- WRONG: ncrs/facade_core.py

---

Agent #1 Complete. Ready for handoff to Agent #2 (Memory Cleanup).
