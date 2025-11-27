# NCRS Performance Optimizations

**Last Updated**: 2025-11-23
**Document Version**: v4.0
**Git Reference**: snnupgrade/c501348
**Data Sources**: WORKFLOW.md v4.0, git commits f37e93f + c501348 + c3ee556

## Purpose

Document the 5 major performance optimization features implemented in recent commits.

## 1. Streaming Result Collection (Commit c501348)

### Implementation
- **File**: stage_results_collection.py (156 LOC)
- **Location**: /home/cabdru/newdemo/ncrs/multi_path_controller/parallel/
- **Commit**: c501348 (2025-11-23)
- **Commit Message**: "feat(streaming): implement streaming result collection with code quality improvements"

### Purpose
Incremental path result collection during multihop loop execution instead of collecting all results at the end.

### Benefits
- **Real-time Access**: Partial results available immediately
- **Reduced Memory**: Incremental aggregation vs. accumulating all in memory
- **Earlier Error Detection**: Path failures detected during execution
- **Progressive Updates**: SSE events with intermediate results

### Key Components
- Stream-based path collection
- Incremental result aggregation
- Real-time result updates via SSE
- Memory-efficient path storage

### SSE Event
- **Event Type**: streaming_update
- **Emitter**: stage_results_collection.py
- **Frequency**: During multihop loop execution
- **Payload**: Incremental path results + metrics

### Impact
- Enables live result monitoring in frontend
- Reduces peak memory usage by ~30%
- Improves error recovery (partial results preserved)

## 2. Brian2 Pre-compilation System (Commit f37e93f)

### Implementation
- **File**: brian2_startup_precompile.py
- **Location**: /home/cabdru/newdemo/ncrs/
- **Commit**: f37e93f (2025-11-22)
- **Commit Message**: "feat(performance): implement eager Brian2 pre-compilation and worker pool warmup system"

### Purpose
Eager Cython compilation of Brian2 networks at system startup to eliminate first-query compilation delay.

### Benefits
- **Time Savings**: Saves 60-90s on first query execution
- **Predictable Performance**: All queries have consistent latency
- **SIMD Optimization**: Pre-compiled code uses SIMD instructions
- **Cache Hit**: Compiled code cached in ~/.cython/brian_extensions/

### Key Features
- Automatic compilation detection
- Cython cache management (~/.cython/)
- SIMD optimization enabled
- One-time startup cost (~60-90s)

### Trade-off
- **Startup Cost**: Adds 60-90s to system initialization
- **Benefit**: Every query saves 60-90s (100% of queries benefit)
- **Net Impact**: Positive for any system handling 2+ queries

### Technical Details
- **Cache Location**: ~/.cython/brian_extensions/
- **Compiler**: Cython with SIMD flags
- **Optimization Level**: -O3
- **Network Size**: 2.3M sparse neurons, 9 cortical columns

## 3. Worker Pool Warmup (Commit f37e93f)

### Implementation
- **File**: facade_core.py (method: _warmup_worker_pool)
- **Location**: /home/cabdru/newdemo/ncrs/facade_core.py
- **Commit**: f37e93f (2025-11-22)
- **Lines**: Part of 492 LOC facade_core.py

### Purpose
Pre-initialize 24 workers with pre-built Brian2 networks for instant query execution.

### Benefits
- **Instant Execution**: Zero worker initialization delay on queries
- **Pre-built Networks**: Brian2 networks already constructed in workers
- **Shared Resources**: ConceptNet + embeddings shared across all 24 workers
- **Consistent Performance**: All queries have same execution profile

### Key Features
- 24-worker pool pre-initialization
- Network pre-building in each worker
- Shared memory resource setup (ConceptNet CSV + embedding cache)
- Health check validation

### Startup Cost
- **Duration**: 5-10s warmup during system startup
- **Operations**:
  - Spawn 24 worker processes
  - Load ConceptNet data (3.4M edges) into shared memory
  - Load embedding cache (1.66GB) into shared memory
  - Pre-build Brian2 network in each worker
  - Validate worker health

### Resource Usage
- **Workers**: 24 processes
- **Shared Memory**: ~2GB (ConceptNet + embeddings)
- **Per-Worker Memory**: ~500MB (Brian2 network state)
- **Total Memory**: ~14GB (2GB shared + 24 × 500MB)

### Impact
- Eliminates 15-25s worker initialization delay per query
- Enables true parallel path processing (K=3 paths × 24 workers)
- Critical for multi-query throughput

## 4. Async HyDE Execution (Commit c501348)

### Implementation
- **File**: workflow_stage_hyde.py (method: execute_hyde_workflow)
- **Location**: /home/cabdru/newdemo/src/api/routes/classify/workflow_stage_hyde.py
- **Commit**: c501348 (2025-11-23)
- **Lines**: Part of 238 LOC workflow_stage_hyde.py

### Purpose
Parallel LLM calls for 5 hypothesis generation using asyncio.gather() instead of sequential execution.

### Benefits
- **60% Faster**: 5 parallel LLM calls vs. 5 sequential calls
- **Reduced HyDE Latency**: Stage 2 duration reduced from ~8s to ~3s
- **Better Resource Utilization**: Network I/O parallelized
- **Same LLM Quality**: No change to hypothesis generation quality

### Key Features
- 5 parallel LLM calls via asyncio.gather()
- Async hypothesis generation
- Concurrent embedding computation
- Error handling for individual call failures

### Technical Details
- **LLM Server**: Qwen RPC (localhost:9090)
- **Model**: Qwen2.5-7B-Instruct
- **Calls**: 5 parallel inference requests
- **Output**: 5 hypothetical document answers
- **Embedding**: sentence-transformers (384D vectors)
- **Aggregation**: Mean of 5 embeddings → goal embedding

### Performance Comparison
- **Sequential**: ~8s (5 calls × 1.6s each)
- **Parallel**: ~3s (max of 5 parallel calls)
- **Speedup**: 2.67x (62.5% reduction)

## 5. Goal Distance Validation (Commit c3ee556)

### Implementation
- **File**: workflow_stage_multihop_init.py (validation logic)
- **Location**: /home/cabdru/newdemo/src/api/routes/classify/workflow_stage_multihop_init.py
- **Commit**: c3ee556 (2025-11-22)
- **Commit Message**: "fix(multihop): add fail-fast goal distance validation and enhance Brian2 error handling"

### Purpose
Early detection of invalid goal distances before expensive multihop path execution.

### Benefits
- **Fail-Fast**: Detects invalid paths before SNN simulation
- **Resource Savings**: Prevents wasted computation on invalid paths
- **Enhanced Errors**: Comprehensive error messages with context
- **Faster Failure**: Immediate error vs. discovering during execution

### Key Features
- Goal distance validation before path execution
- Brian2 error context capture
- Comprehensive error messages
- Early termination on validation failure

### Validation Checks
1. **Distance Feasibility**: Goal embedding distance within valid range
2. **Seed Viability**: Seed concepts have valid embeddings
3. **Network Connectivity**: Paths exist in ConceptNet graph
4. **Resource Availability**: Brian2 network ready

### Error Handling
- **Invalid Distance**: Immediate error with distance metrics
- **Missing Seeds**: Report missing concepts with suggestions
- **Graph Issues**: ConceptNet connectivity problems
- **Brian2 Errors**: Enhanced error context with network state

### Impact
- Prevents ~30s wasted computation on invalid paths
- Improves debugging with enhanced error messages
- Better user experience (fast failure vs. long timeout)

## Combined Performance Impact

### Startup Time
- **Brian2 Pre-compilation**: +60-90s (one-time)
- **Worker Pool Warmup**: +5-10s (one-time)
- **Total Startup**: +65-100s (one-time cost)

### First Query
- **Without Optimizations**: 60-90s (Brian2 compilation) + 15-25s (worker init) + 134s (execution) = 209-249s
- **With Optimizations**: 0s (pre-compiled) + 0s (pre-warmed) + 81s (execution with async HyDE + streaming) = 81s
- **Speedup**: 2.6-3.1x faster

### Subsequent Queries
- **HyDE Speedup**: 60% faster (8s → 3s)
- **Worker Init**: 0s (already warmed)
- **Brian2 Compilation**: 0s (cached)
- **Streaming**: Progressive results (memory efficient)

### Resource Usage
- **Memory**: +14GB (shared resources + worker pool)
- **CPU**: Better utilization (parallel LLM + SNN)
- **Disk**: +500MB (Cython cache)

## Verification Commands

### Check Brian2 Compilation Cache
```bash
ls -lh ~/.cython/brian_extensions/
# Should show compiled .so files
```

### Check Worker Pool Status
```bash
# In facade_core.py logs during startup
grep "Worker pool warmup" logs/app.log
# Should show "24 workers pre-initialized"
```

### Monitor Streaming Results
```bash
# SSE event stream
curl -N http://localhost:8000/api/v1/stream
# Should show streaming_update events during multihop loop
```

### Measure HyDE Performance
```bash
# Check HyDE duration in database
sqlite3 data/query_tracking.db "SELECT hyde_duration_ms FROM queries ORDER BY created_at DESC LIMIT 10;"
# Should show ~2000-4000ms (vs ~7000-9000ms sequential)
```

## Related Memory Files

- ncrs-workflow-system-overview: How optimizations fit into workflow
- ncrs-architecture-summary: System architecture context
- ncrs-git-reference: Commit history for features

## Reference Documentation

- /home/cabdru/newdemo/docs2/WORKFLOW.md (v4.0, section: New Features)
- /home/cabdru/newdemo/docs/per_simulation_optimization_report.md
- /home/cabdru/newdemo/docs/streaming-collection-design.md (59 KB)
- /home/cabdru/newdemo/docs/streaming-collection-implementation.md
