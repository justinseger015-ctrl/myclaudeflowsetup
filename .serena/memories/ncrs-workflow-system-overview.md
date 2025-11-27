# NCRS Workflow System Overview

**Last Updated**: 2025-11-23
**Document Version**: v4.0
**Git Reference**: snnupgrade/c501348
**Data Sources**: WORKFLOW.md v4.0, current-state-analysis-2025-11-23.md

## Purpose

High-level overview of NCRS query processing workflow architecture for future agent reference.

## 5-Stage Workflow Architecture

### Stage 1: Classification (Implicit)
- **Executor**: LLMQueryClassifier via Qwen RPC
- **Purpose**: Determine query type (causal, factual, temporal, etc.)
- **Duration**: 1-3s (blocking, user-facing)
- **Output**: Query type + classification confidence
- **SSE Event**: query_classified

### Stage 2: HyDE Generation (workflow_stage_hyde.py - 238 LOC)
- **Executor**: HyDE ensemble generator
- **Purpose**: Create 5 hypothetical document embeddings
- **Duration**: 2-5s (background)
- **Optimization**: Async parallel LLM calls (60% faster than sequential)
- **Output**: 384D goal embedding from 5 hypothesis embeddings
- **SSE Event**: goal_generated

### Stage 3: Seed Extraction (workflow_stage_seeds.py - 350 LOC)
- **Executor**: ExtractionOrchestrator + DualSearchEngine
- **Purpose**: Extract seed concepts using LLM + ConceptNet hybrid search
- **Duration**: 10-20s (background)
- **Output**: Candidate seed concepts with match types
- **SSE Event**: seeds_extracted

### Stage 4: Multihop Initialization (workflow_stage_multihop_init.py - 207 LOC)
- **Executor**: Path initialization system
- **Purpose**: Initialize K=3 parallel reasoning paths from seeds
- **Duration**: 15-25s (background)
- **Output**: Path metadata, ConceptNet graph loaded
- **SSE Event**: multihop_initialized

### Stage 5: Multihop Loop (workflow_stage_multihop_loop.py - 477 LOC)
- **Executor**: Iterative hop reasoning engine
- **Purpose**: Execute multi-hop reasoning with streaming results
- **Duration**: 30-70s (background)
- **Features**: 
  - Streaming result collection (incremental path results)
  - Parallel SNN execution (24 workers)
  - Goal distance validation (fail-fast)
  - Real-time SSE events
- **Output**: Final reasoning paths with termination reasons
- **SSE Events**: hop_completed, path_terminated, frontier_updated, streaming_update

## Execution Model

### User-Facing Latency
- **Blocking Stage**: Classification only (1-3s)
- **HTTP Response**: Returned after classification completes
- **Background Processing**: Stages 2-5 run via FastAPI BackgroundTasks

### Background Workflow
- **Total Duration**: 68-160s (~134s median)
- **Parallelization**: 
  - HyDE: 5 async LLM calls
  - SNN: 24 workers process paths concurrently
- **Event-Driven**: SSE stream provides real-time progress

## Event System Overview

### Real-Time SSE Events (15+ types)
- **Workflow Progress**: query_classified, goal_generated, seeds_extracted, multihop_initialized
- **Execution Updates**: hop_completed, path_terminated, frontier_updated, streaming_update
- **Error Handling**: multihop_error, snn_simulation_failed, error_occurred
- **Health Monitoring**: heartbeat (30s interval), stream_closed, stream_timeout

### Event Delivery
- **Protocol**: Server-Sent Events (SSE)
- **Endpoint**: GET /api/v1/stream
- **Format**: `event: {type}\ndata: {json}\n\n`
- **Keep-Alive**: Ping every 30 seconds

## Performance Characteristics

### Optimization Features (Commit f37e93f + c501348)
1. **Brian2 Pre-compilation**: Saves 60-90s on first query (one-time startup cost)
2. **Worker Pool Warmup**: 24 pre-initialized workers with pre-built networks (5-10s startup)
3. **Async HyDE**: 60% faster hypothesis generation via asyncio.gather()
4. **Streaming Results**: Incremental path collection reduces memory, enables progressive updates
5. **Goal Validation**: Fail-fast validation prevents invalid path computation

### Resource Usage
- **SNN Network**: 2.3M sparse neurons, 9 cortical columns
- **Worker Pool**: 24 workers (shared ConceptNet + embeddings)
- **Memory**: ~500MB per query (embeddings + Brian2 state)
- **Parallel Paths**: K=3 (configurable K_max)

## Database Integration

### SQLite Database (query_tracking.db)
- **Location**: /home/cabdru/newdemo/data/query_tracking.db
- **Tables**: queries, goal_embeddings, answer_embeddings, hypotheses, seeds, paths, metrics
- **Retry Mechanism**: Exponential backoff (5 retries) for deadlock prevention

## External Dependencies

1. **Qwen RPC Server** (localhost:9090)
   - Model: Qwen2.5-7B-Instruct
   - Purpose: Classification, HyDE, seed extraction
   - Health check: RPC health_check() method

2. **ConceptNet Data** (CSV)
   - Files: edges_entity.csv, edges_semantic.csv
   - Size: 3.4M edges total
   - Location: data/ directory

3. **Embedding Cache** (NPZ)
   - File: concept_embeddings.npz
   - Size: 1.66GB (1.8M concepts, 384D vectors)
   - Format: sentence-transformers embeddings

## Related Memory Files

- ncrs-architecture-summary: Detailed component architecture
- ncrs-performance-optimizations: Feature-specific optimization details
- ncrs-git-reference: Version control state
- ncrs-current-state-baseline: Complete system baseline

## Reference Documentation

- /home/cabdru/newdemo/docs2/WORKFLOW.md (v4.0)
- /home/cabdru/newdemo/docs/current-state-analysis-2025-11-23.md
