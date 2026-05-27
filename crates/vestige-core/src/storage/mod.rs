//! Storage Module
//!
//! SQLite-based storage layer with:
//! - FTS5 full-text search with query sanitization
//! - Embedded vector storage
//! - FSRS-6 state management
//! - Temporal memory support

mod migrations;
mod portable;
mod sqlite;

pub use migrations::MIGRATIONS;
pub use portable::{
    PORTABLE_ARCHIVE_FORMAT, PortableArchive, PortableImportMode, PortableImportReport,
    PortableTable, PortableValue,
};
pub use sqlite::{
    ConnectionRecord, ConsolidationHistoryRecord, DreamHistoryRecord, FilePortableSyncBackend,
    InsightRecord, IntentionRecord, PortableSyncBackend, PortableSyncReport, Result,
    SmartIngestResult, StateTransitionRecord, Storage, StorageError,
};
