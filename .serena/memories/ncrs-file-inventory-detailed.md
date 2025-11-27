# NCRS File Inventory - Detailed Breakdown

## Backend Root Module (ncrs/) - 202 Python Files

### Root Level Files (24 files, 8,105 LOC total)
- facade_core.py: 492 LOC
- facade_workflow.py: 631 LOC
- utils.py: 830 LOC
- synapse_builder.py: 816 LOC
- state_manager.py: 771 LOC
- runtime_mode_controller.py: 623 LOC
- controller.py: 354 LOC
- hop_utils.py: 457 LOC
- unified_cortex.py: 439 LOC
- config.py: 237 LOC
- exceptions.py: 312 LOC
- concept_extraction.py: 231 LOC
- neuron_factory.py: 244 LOC
- node_mapping_cache.py: 268 LOC
- csv_data_cache.py: 307 LOC
- model_constants.py: 181 LOC
- facade.py: 159 LOC
- facade_validation.py: 138 LOC
- firing_rate.py: 139 LOC
- hop_runner.py: 87 LOC
- model_state.py: 144 LOC
- facade_metrics.py: 103 LOC
- multi_path_controller.py: 41 LOC
- __init__.py: 101 LOC

### Subdirectories (28 total)
- multi_path_controller/ (7 subdirs: parallel/, parallel_snn/, multihop/, examples/)
- classification/ (config_loader/, prompts/)
- seed_extraction/ (prompts/)
- seed_selection/
- hop_runner/
- hybrid/ (path_history/)
- network_builder/
- orchestrator/
- monitoring/
- integration/
- llm/
- utils/
- database/
- evaluation/
- analysis/
- decoders/
- embeddings/
- extraction/
- fixes/
- goal_region/
- snn/
- optimization/
- rpc/
- config/

## Workflow Stages (src/api/routes/classify/)

### Four Active Workflow Stages (1,272 LOC total)
- workflow_stage_seeds.py: 350 LOC
- workflow_stage_multihop_loop.py: 477 LOC
- workflow_stage_hyde.py: 238 LOC
- workflow_stage_multihop_init.py: 207 LOC

### Supporting Files (classify/)
- endpoint.py: Main endpoint handling
- models.py: API models
- utils.py: Endpoint utilities
- __init__.py
- __pycache__/

## Frontend (src/web/src/) - 157 TypeScript/React Files

### Main Files (root level)
- App.tsx
- App.css
- main.tsx
- index.css
- vite-env.d.ts

### Directories (8 major)
- components/ (15 subdirs)
  - pipeline/, workflow/, visualizations/, forms/, etc.
- pages/ (route pages)
- stores/ (Zustand state)
- hooks/ (custom React hooks)
- lib/ (utilities)
- services/ (API services)
- types/ (TypeScript types)
- config/
- styles/
- utils/
- assets/
- api/

## Tests (tests/) - 53 Python Files

### Test Categories
- unit/ (multiple test files for hyde, multihop)
- integration/ (hyde_e2e, multihop, sse_events)
- regression/ (regression test suite)
- network_builder/ (network tests)
- load/ (load testing)
- standalone/ (standalone scripts)
- verification/ (verification tests)

## Documentation - 33 Markdown Files

### docs/ (12 files)
- brian2_initialization_analysis.md
- fork-context-implementation.md
- fork-fix-verification-report.md
- hop_00_performance_analysis.md
- network_pool_implementation_guide.md
- per_simulation_optimization_report.md
- streaming-collection-design.md (59 KB)
- streaming-collection-implementation.md
- streaming-validation-report.md
- testing-streaming-collection.md
- worker-fix-complete-summary.md
- worker-queue-analysis.md

### docs2/ (21 files)
- ADR.md, API_GUIDE.md, WORKFLOW.md, USACF.md
- claudeflow.md, coreidea.md, claudecodeskills.md
- Brian2Report.md, MetaPromptGenerator.md, QWEN_SERVER_GUIDE.md
- SAPPO.md, goodcodeguide.md, goodtestsguide.md
- learntheory.md, gametasknosec.md, subagent.md
- systemspecs.md, truthprompt.md
- Plus copies and variations

### Root (3 files)
- README.md
- CLAUDE.md
- BRIAN2_FIX_SUMMARY.md

### docs3/
- christheory/ directory (theory documentation)

## Configuration Files

### Python
- pyproject.toml: 6.1 KB

### Node/JavaScript
- src/web/package.json
- src/web/tsconfig.json
- src/web/vite.config.ts

### Project Config
- .env (environment variables)
- .mcp.json (MCP server configuration)
- .gitignore (git ignore rules)
- .pre-commit-config.yaml
- .pylintrc
- Makefile

### Claude Code
- .claude/ (agent definitions, skills, hooks, commands)

## Data & Cache Files

### data/ Directory
- query_tracking.db (SQLite)
- csv_cache/ (cached CSV data)
- .cache/ (concept index cache)
- .claude-flow/metrics/ (Claude Flow metrics)

### models/ Directory
- Qwen2.5-7B-Instruct/ (model storage + cache)

### logs/ Directory
- worker_errors/ (error logs)

## Summary Statistics
- Total Python Files: 202 (backend) + 53 (tests) = 255
- Total TypeScript Files: 157
- Total Documentation: 33 markdown files
- Total Config Files: 10+
- Root Backend LOC: 8,105
- Workflow Stage LOC: 1,272
- Parallel SNN Runner LOC: 2,290
