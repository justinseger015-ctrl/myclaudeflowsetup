# NCRS Current State Baseline - Updated 2025-11-23

**Original**: Agent #1 Findings (2025-11-23)
**Updated**: Agent #6 (Serena Memory Update Agent)
**Data Sources**: Agent #1 baseline, WORKFLOW.md v4.0, current-state-analysis-2025-11-23.md

## Purpose

Complete baseline snapshot of NCRS project state for sequential agent workflow reference. This memory is updated with the latest information from WORKFLOW.md v4.0 update.

## Git State

- **Branch**: snnupgrade
- **Commit**: c501348557ea2c39eab138345cde75151ba6f2d9 (feat: streaming result collection)
- **Status**: Up to date with origin, clean working tree with unstaged changes
- **Modified (unstaged)**: 4 files (.gitignore, docs2/claudeflow.md, ncrs/facade_core.py, parallel_snn_runner.py)
- **Untracked docs**: 6 analysis files in docs/

## File Inventory Summary

- **Backend Python**: 202 files total
- **Root Backend LOC**: 8,105 lines (verified from actual file count)
- **Frontend TypeScript/React**: 157 files
- **Test Python**: 53 files
- **Documentation**: 33 markdown files

## Backend Key Modules

### Core Files (Top 15)
- ncrs/parallel_snn_runner.py: 2,290 LOC (largest module, parallel SNN execution)
- ncrs/synapse_builder.py: 816 LOC
- ncrs/utils.py: 830 LOC
- ncrs/state_manager.py: 771 LOC
- ncrs/facade_workflow.py: 631 LOC (workflow orchestration)
- ncrs/runtime_mode_controller.py: 623 LOC
- ncrs/facade_core.py: 492 LOC (main entry point + worker warmup)
- ncrs/hop_utils.py: 457 LOC
- ncrs/unified_cortex.py: 439 LOC (9 cortical columns)
- ncrs/controller.py: 354 LOC
- ncrs/exceptions.py: 312 LOC
- ncrs/csv_data_cache.py: 307 LOC
- ncrs/node_mapping_cache.py: 268 LOC
- ncrs/neuron_factory.py: 244 LOC
- ncrs/config.py: 237 LOC

## Workflow Stages (5 active)

### Classification (Stage 1 - Implicit)
- **Implementation**: LLMQueryClassifier (no dedicated file)
- **Purpose**: Query type determination via Qwen RPC
- **Duration**: 1-3s (blocking, user-facing)

### Workflow API Stages (4 files, 1,272 LOC total)

Located: /home/cabdru/newdemo/src/api/routes/classify/

1. **workflow_stage_hyde.py**: 238 LOC
   - HyDE goal generation
   - 5 async LLM calls (60% faster than sequential)
   - Outputs 384D goal embedding

2. **workflow_stage_seeds.py**: 350 LOC
   - Seed concept extraction
   - LLM + fuzzy + semantic search
   - Dual search engine

3. **workflow_stage_multihop_init.py**: 207 LOC
   - Multi-path initialization
   - K=3 path setup
   - Network graph loading

4. **workflow_stage_multihop_loop.py**: 477 LOC
   - Main iterative hop execution
   - Streaming result collection (NEW)
   - Path termination detection
   - Real-time SSE events

### Supporting Files
- endpoint.py: 325 LOC (main API endpoint)
- utils.py: 127 LOC (API utilities)
- models.py: 109 LOC (API data models)

**Total Workflow API LOC**: 1,833 (including endpoint + utils + models)

## Frontend Structure

- **157 TypeScript/React files**
- **Location**: src/web/src/
- **Key dirs**: components/ (15 subdirs), pages/, stores/, hooks/, services/, types/
- **Major features**: 3D visualization (Three.js), workflow tracking, pipeline visualization, stage details
- **Framework**: React 19.2.0 + TypeScript + Vite

## New Features (Recent Commits)

### 1. Streaming Result Collection (c501348)
- **Implementation**: stage_results_collection.py (156 LOC)
- **Purpose**: Incremental path results during multihop loop
- **Benefits**: Real-time access, reduced memory, earlier error detection

### 2. Brian2 Pre-compilation (f37e93f)
- **Implementation**: brian2_startup_precompile.py
- **Purpose**: Eager Cython compilation at startup
- **Benefits**: Saves 60-90s on first query, one-time startup cost

### 3. Worker Pool Warmup (f37e93f)
- **Implementation**: facade_core.py (_warmup_worker_pool method)
- **Purpose**: Pre-initialize 24 workers with networks
- **Benefits**: Instant execution, 5-10s startup cost

### 4. Async HyDE Execution (c501348)
- **Implementation**: workflow_stage_hyde.py (asyncio.gather)
- **Purpose**: Parallel LLM calls for hypotheses
- **Benefits**: 60% faster than sequential

### 5. Goal Distance Validation (c3ee556)
- **Implementation**: workflow_stage_multihop_init.py
- **Purpose**: Fail-fast validation before SNN
- **Benefits**: Prevents wasted computation, enhanced errors

## External Services

### 1. Qwen RPC Server (REQUIRED)
- **Host**: localhost:9090
- **Model**: Qwen2.5-7B-Instruct
- **Purpose**: Classification, HyDE, seed extraction
- **Start**: python scripts/qwen_model_server.py

### 2. ConceptNet Data (REQUIRED)
- **Files**: edges_entity.csv, edges_semantic.csv
- **Location**: data/ directory
- **Size**: 3.4M edges total

### 3. Embedding Cache (REQUIRED)
- **File**: data/concept_embeddings.npz
- **Size**: 1.66GB (1.8M concepts, 384D vectors)
- **Format**: NumPy NPZ compressed

## Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| SNN Network | 2.3M sparse neurons | 9 cortical columns |
| ConceptNet | 3.4M edges | CSV data |
| Embeddings | 1.8M concepts, 1.66GB | 384D vectors |
| Workers | 24 workers | Pre-warmed at startup |
| Parallel Paths | K=3 | Configurable K_max |
| HyDE Speedup | 60% faster | Async vs sequential |
| Brian2 Compilation | 60-90s saved | Pre-compiled at startup |
| Worker Warmup | 5-10s | One-time startup cost |

## Database Files

- **query_tracking.db**: /home/cabdru/newdemo/data/query_tracking.db (SQLite, 38 fields)
- **memory.db**: /home/cabdru/newdemo/.swarm/memory.db (Claude Flow)
- **serena.db**: /home/cabdru/newdemo/serena/ncrs.db (Serena IDE)

## Subdirectories (ncrs/) - 28 total

Major ones: multi_path_controller/ (7 subdirs), classification/, seed_extraction/, seed_selection/, hop_runner/, hybrid/, network_builder/, orchestrator/, monitoring/, integration/, llm/, utils/, database/, evaluation/, analysis/, decoders/, embeddings/, extraction/, fixes/, goal_region/, snn/, optimization/, rpc/, config/

## Documentation

### docs/ (12 files)
Recent analysis files including streaming-collection-design.md (59 KB), performance analysis, implementation guides

### docs2/ (21 files)
Comprehensive docs including WORKFLOW.md (v4.0, updated 2025-11-23), API_GUIDE.md, architecture docs, theory docs

### Root (3 files)
- README.md (12.2 KB)
- CLAUDE.md (13.1 KB)
- BRIAN2_FIX_SUMMARY.md

### docs3/
- christheory/ directory (theory documentation)

## Configuration

### Python
- **pyproject.toml**: 6.1 KB (Python 3.11+, Brian2 2.9.0)

### Node/JavaScript
- **src/web/package.json**: React 19.2.0, TypeScript, Vite, Three.js
- **src/web/tsconfig.json**: TypeScript config
- **src/web/vite.config.ts**: Vite build config

### Project
- **.env**: Environment variables
- **.mcp.json**: MCP server config
- **.gitignore**: Git ignore rules
- **.pre-commit-config.yaml**: Pre-commit hooks
- **.pylintrc**: Linting rules
- **Makefile**: Build automation

### Claude Code
- **.claude/**: Agent definitions (54+ agents), Skills (25+), Commands, Hooks

## Complete Baseline Location

- **Full inventory document**: /home/cabdru/newdemo/docs/current-state-inventory.md (574 lines, 18 KB)
- **Current state analysis**: /home/cabdru/newdemo/docs/current-state-analysis-2025-11-23.md (680 lines)
- **Updated workflow doc**: /home/cabdru/newdemo/docs2/WORKFLOW.md (v4.0, 1,870 lines)
- **All absolute paths documented**
- **Ready for downstream agents**

## Related Serena Memory Files

- **ncrs-workflow-system-overview**: Workflow execution details
- **ncrs-architecture-summary**: Detailed component architecture
- **ncrs-performance-optimizations**: Feature-specific optimization details
- **ncrs-git-reference**: Version control state and recent commits
- **ncrs-file-inventory-detailed**: Complete file listing by category

## Update History

- **Original**: Created by Agent #1 (Baseline Agent) on 2025-11-23
- **Update 1**: Enhanced by Agent #6 (Serena Memory Update Agent) on 2025-11-23
  - Added 5 new features from WORKFLOW.md v4.0
  - Updated workflow stage details
  - Added external service information
  - Added performance characteristics
  - Cross-referenced with new Serena memory files
