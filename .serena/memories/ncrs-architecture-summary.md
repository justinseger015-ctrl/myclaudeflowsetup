# NCRS Architecture Summary

**Last Updated**: 2025-11-23
**Document Version**: v4.0
**Git Reference**: snnupgrade/c501348
**Data Sources**: Agent #1 baseline, current-state-analysis-2025-11-23.md

## Purpose

Comprehensive architecture summary of NCRS project for future agent reference.

## File Inventory Overview

### Backend Python (ncrs/ module)
- **Total Files**: 202 Python files
- **Total LOC**: 8,105 lines of code
- **Location**: /home/cabdru/newdemo/ncrs/
- **Subdirectories**: 28 total
- **Pattern**: Modular facade architecture

### Frontend TypeScript/React
- **Total Files**: 157 files
- **Location**: /home/cabdru/newdemo/src/web/src/
- **Framework**: React 19.2.0 with TypeScript
- **Build Tool**: Vite
- **Key Features**: 3D visualization (Three.js), workflow tracking, pipeline visualization

### Test Suite
- **Total Files**: 53 Python test files
- **Location**: /home/cabdru/newdemo/tests/
- **Categories**: unit/, integration/, regression/, verification/, load/, standalone/

## Core Backend Modules (Top 15 by LOC)

| File | LOC | Purpose |
|------|-----|---------|
| parallel_snn_runner.py | 2,290 | Parallel SNN execution engine with 24 workers |
| synapse_builder.py | 816 | Brian2 synapse construction |
| utils.py | 830 | Utility functions |
| state_manager.py | 771 | State lifecycle management |
| facade_workflow.py | 631 | Workflow orchestration |
| runtime_mode_controller.py | 623 | Runtime mode selection |
| facade_core.py | 492 | System initialization + worker warmup |
| hop_utils.py | 457 | Hop execution utilities |
| unified_cortex.py | 439 | 9 cortical column definitions |
| controller.py | 354 | Main controller logic |
| exceptions.py | 312 | Custom exceptions |
| csv_data_cache.py | 307 | CSV data caching |
| node_mapping_cache.py | 268 | Node caching system |
| neuron_factory.py | 244 | Neuron creation factory |
| config.py | 237 | Configuration management |

**Total Top 15**: 8,071 LOC (~99.6% of root module LOC)

## Workflow API Stage Files

### Core Workflow Stages (4 files, 1,272 LOC)
1. **workflow_stage_multihop_loop.py** (477 LOC)
   - Main iterative hop execution
   - Streaming result collection
   - Path termination detection
   - SSE event emission

2. **workflow_stage_seeds.py** (350 LOC)
   - Seed concept extraction
   - ExtractionOrchestrator + DualSearchEngine
   - LLM + fuzzy + semantic search

3. **workflow_stage_hyde.py** (238 LOC)
   - HyDE goal generation
   - 5 async LLM calls (60% faster)
   - 384D goal embedding aggregation

4. **workflow_stage_multihop_init.py** (207 LOC)
   - Multi-path initialization
   - K=3 path setup
   - Network graph loading

### Supporting Files
- **endpoint.py** (325 LOC): Main FastAPI endpoint handler
- **utils.py** (127 LOC): API utilities
- **models.py** (109 LOC): API data models

**Total Workflow API**: 1,833 LOC (including endpoint + utils + models)

## Key Subdirectories (ncrs/ module - 28 total)

### Major Subdirectories
- **multi_path_controller/**: Multi-path reasoning control (7 subdirs: parallel/, parallel_snn/, multihop/, examples/)
- **classification/**: Query classification (config_loader/, prompts/)
- **seed_extraction/**: Seed extraction logic (prompts/)
- **seed_selection/**: Seed selection algorithms
- **hop_runner/**: Hop execution engine
- **hybrid/**: Hybrid reasoning (path_history/)
- **network_builder/**: Brian2 network construction
- **orchestrator/**: Workflow orchestration
- **monitoring/**: Performance monitoring
- **integration/**: External integrations
- **llm/**: LLM clients (Qwen RPC)
- **utils/**: Utility functions
- **database/**: Database operations
- **evaluation/**: Metrics and evaluation
- **analysis/**: Result analysis

### Additional Subdirectories
decoders/, embeddings/, extraction/, fixes/, goal_region/, snn/, optimization/, rpc/, config/

## Frontend Structure (src/web/src/)

### Main Directories (8 major)
- **components/** (15 subdirs): React components
  - pipeline/, workflow/, visualizations/, forms/, etc.
- **pages/**: Route pages
- **stores/**: Zustand state management
- **hooks/**: Custom React hooks
- **lib/**: Utilities
- **services/**: API services
- **types/**: TypeScript types
- **config/**: Configuration

### Key Features
- 3D visualization (Three.js Scene3DCanvas)
- Workflow progress tracking
- Pipeline visualization
- Stage details views
- Real-time SSE event handling

## Database Files

### SQLite Databases
1. **query_tracking.db**: /home/cabdru/newdemo/data/query_tracking.db
   - Main query state and results
   - 38 fields per query
   - 4 indexes (created_at, status, endpoint, hyde_generated)

2. **memory.db**: /home/cabdru/newdemo/.swarm/memory.db
   - Claude Flow coordination memory

3. **serena.db**: /home/cabdru/newdemo/serena/ncrs.db
   - Serena IDE memory storage

## Configuration Files

### Python
- **pyproject.toml**: 6.1 KB
  - Python 3.11+
  - Brian2 2.9.0
  - Dependencies

### Node/JavaScript
- **package.json**: React 19.2.0, TypeScript, Vite, Three.js
- **tsconfig.json**: TypeScript configuration
- **vite.config.ts**: Vite build configuration

### Project
- **.env**: Environment variables
- **.mcp.json**: MCP server configuration
- **.gitignore**: Git ignore rules
- **.pre-commit-config.yaml**: Pre-commit hooks
- **.pylintrc**: Linting rules
- **Makefile**: Build automation

### Claude Code
- **.claude/**: Agent definitions (54+ agents), Skills (25+)

## Documentation Structure (33 markdown files)

### docs/ (12 files)
Recent analysis and implementation guides:
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
Comprehensive system documentation:
- WORKFLOW.md (v4.0, updated 2025-11-23)
- API_GUIDE.md, ADR.md, USACF.md
- claudeflow.md, coreidea.md, claudecodeskills.md
- Brian2Report.md, MetaPromptGenerator.md
- QWEN_SERVER_GUIDE.md, SAPPO.md
- goodcodeguide.md, goodtestsguide.md
- learntheory.md, gametasknosec.md, subagent.md
- systemspecs.md, truthprompt.md
- Plus copies and variations

### Root (3 files)
- README.md (12.2 KB)
- CLAUDE.md (13.1 KB)
- BRIAN2_FIX_SUMMARY.md

## Data & Cache Files

### data/ Directory
- query_tracking.db (SQLite)
- csv_cache/ (cached CSV data)
- .cache/ (concept index cache)
- .claude-flow/metrics/ (Claude Flow metrics)
- edges_entity.csv, edges_semantic.csv (ConceptNet 3.4M edges)
- concept_embeddings.npz (1.66GB, 1.8M concepts, 384D)

### models/ Directory
- Qwen2.5-7B-Instruct/ (model storage + cache)

### logs/ Directory
- worker_errors/ (error logs)

## Architecture Patterns

### Modular Facade Pattern
- **Facade Layer**: facade_core.py, facade_workflow.py, facade_validation.py
- **Module Layers**: Classification, HyDE, Seeds, Controller, SNN
- **Orchestration**: endpoint.py coordinates workflow stages

### Async/Background Execution
- **Blocking**: Stage 1 classification (1-3s)
- **Background**: Stages 2-5 via FastAPI BackgroundTasks
- **Parallelization**: asyncio.to_thread() for CPU-intensive work

### Shared Memory Architecture
- ConceptNet CSV shared across 24 workers
- Embedding cache shared across workers
- Pre-compiled Brian2 networks cached

## Summary Statistics

- **Total Python Files**: 202 (backend) + 53 (tests) = 255
- **Total TypeScript Files**: 157
- **Total Documentation**: 33 markdown files
- **Total Config Files**: 10+
- **Root Backend LOC**: 8,105
- **Workflow Stage LOC**: 1,272 (4 files)
- **Parallel SNN Runner LOC**: 2,290
- **Frontend Framework**: React 19.2.0 + TypeScript
- **Build System**: Vite + npm
- **Backend Framework**: FastAPI + Brian2

## Related Memory Files

- ncrs-workflow-system-overview: Workflow execution details
- ncrs-performance-optimizations: Feature optimizations
- ncrs-git-reference: Version control state
- ncrs-file-inventory-detailed: Complete file listing

## Reference Documentation

- /home/cabdru/newdemo/docs/current-state-inventory.md (574 lines, Agent #1 baseline)
- /home/cabdru/newdemo/docs/current-state-analysis-2025-11-23.md (Agent #4 analysis)
