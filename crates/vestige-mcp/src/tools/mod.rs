//! MCP Tools
//!
//! Tool implementations for the Vestige MCP server.
//!
//! The unified tools (codebase_unified, intention_unified, memory_unified, search_unified)
//! are the primary API. The granular tools below are kept for backwards compatibility
//! but are not exposed in the MCP tool list.

// Active unified tools
pub mod codebase_unified;
pub mod intention_unified;
pub mod memory_unified;
pub mod search_unified;
pub mod smart_ingest;
// #57: external-source connectors (GitHub Issues / Redmine retrieval layer)
pub mod source_sync;

// v1.2: Temporal query tools
pub mod changelog;
pub mod timeline;

// v1.2: Maintenance tools
pub mod maintenance;

// v2.2: Unified maintenance surface — folds consolidate + dream + gc +
// importance_score + backup + export + restore into one action-dispatched tool.
pub mod maintain;

// v2.2: Unified status surface — folds system_status + memory_health +
// memory_timeline + memory_changelog into one view-dispatched tool.
pub mod memory_status;

// v1.3: Auto-save and dedup tools
pub mod dedup;
pub mod importance;

// v2.1.25: Merge / Supersede controls (Phase 3)
pub mod merge;

// v1.5: Cognitive tools
pub mod dream;
pub mod explore;
pub mod predict;
pub mod restore;

// v1.8: Context Packets
pub mod session_context;

// v1.9: Autonomic tools
pub mod graph;
pub mod health;

// v2.2: Unified graph surface — folds explore_connections + predict +
// memory_graph + composed_graph into one action-dispatched tool.
pub mod graph_unified;

// v2.1: Cross-reference (connect the dots)
pub mod composed_graph;
pub mod contradictions;
pub mod cross_reference;

// v2.0.5: Active Forgetting — Anderson 2025 + Davis Rac1
pub mod suppress;

// Internal/backwards-compat tools still dispatched by server.rs for specific
// tool names. Each module below has live callers via string dispatch in
// `server.rs` (match arms on request.name). The #[allow(dead_code)]
// suppresses warnings for the per-module schema/struct items that aren't
// yet consumed.
//
// The nine legacy siblings here pre-v2.0.8 (checkpoint, codebase, consolidate,
// ingest, intentions, knowledge, recall, search, stats) were removed in the
// post-v2.0.8 dead-code sweep — all nine had zero callers after the
// unification work landed `*_unified` + `maintenance::*` replacements.
#[allow(dead_code)]
pub mod context;
#[allow(dead_code)]
pub mod feedback;
#[allow(dead_code)]
pub mod memory_states;
#[allow(dead_code)]
pub mod review;
#[allow(dead_code)]
pub mod tagging;
