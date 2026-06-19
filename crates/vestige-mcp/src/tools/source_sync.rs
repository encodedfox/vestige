//! `source_sync` MCP tool (#57) — index an external system into Vestige.
//!
//! Turns Vestige into a durable, offline, provenance-linked retrieval layer
//! over a long-lived external system. The first connector is GitHub Issues:
//! point it at `owner/repo` and Vestige indexes every issue + its comments as
//! source-aware memories you can search semantically and cite back to the
//! canonical issue URL — re-runnable idempotently (no duplicates) and able to
//! tombstone issues that vanish upstream.
//!
//! Unlike the official GitHub MCP server (a stateless live API proxy), this
//! keeps a local index: searchable offline, embedded for semantic recall,
//! joinable with the rest of your memory, and temporally versioned.
//!
//! ## Auth (security)
//!
//! The GitHub token is read from the `GITHUB_TOKEN` (or `VESTIGE_GITHUB_TOKEN`)
//! environment variable, never from tool arguments, so credentials are not
//! logged in the conversation. Public repositories work without a token at a
//! lower rate limit.

use std::sync::Arc;

use serde::Deserialize;
use serde_json::{Value, json};

use vestige_core::storage::Storage;

/// JSON schema for the `source_sync` tool.
pub fn schema() -> Value {
    json!({
        "type": "object",
        "properties": {
            "source": {
                "type": "string",
                "enum": ["github"],
                "description": "External system to sync. Currently: 'github' (GitHub Issues).",
                "default": "github"
            },
            "repo": {
                "type": "string",
                "description": "GitHub repository as 'owner/name', e.g. 'samvallad33/vestige'."
            },
            "reconcile": {
                "type": "boolean",
                "description": "Also tombstone local memories for issues no longer visible upstream (an extra full enumeration pass). Default false on incremental syncs.",
                "default": false
            },
            "max_pages": {
                "type": "integer",
                "description": "Max API pages to fetch this run (each page is up to 100 issues). Lets a first sync of a large repo be resumed across calls. Default 10.",
                "default": 10,
                "minimum": 1,
                "maximum": 1000
            }
        },
        "required": ["repo"]
    })
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct SourceSyncArgs {
    #[serde(default = "default_source")]
    source: String,
    repo: String,
    #[serde(default)]
    reconcile: bool,
    #[serde(default, alias = "max_pages")]
    max_pages: Option<usize>,
}

fn default_source() -> String {
    "github".to_string()
}

/// Read the GitHub token from the environment (never from tool args).
fn github_token() -> Option<String> {
    std::env::var("GITHUB_TOKEN")
        .or_else(|_| std::env::var("VESTIGE_GITHUB_TOKEN"))
        .ok()
        .filter(|s| !s.trim().is_empty())
}

pub async fn execute(storage: &Arc<Storage>, args: Option<Value>) -> Result<Value, String> {
    let args: SourceSyncArgs = match args {
        Some(v) => serde_json::from_value(v).map_err(|e| format!("Invalid arguments: {e}"))?,
        None => return Err("Missing arguments".to_string()),
    };

    if args.source != "github" {
        return Err(format!(
            "Unsupported source '{}'. Currently only 'github' is supported.",
            args.source
        ));
    }

    let (owner, repo) = args
        .repo
        .split_once('/')
        .filter(|(o, r)| !o.is_empty() && !r.is_empty())
        .ok_or_else(|| {
            "repo must be in 'owner/name' form, e.g. 'samvallad33/vestige'".to_string()
        })?;

    execute_github(
        storage,
        owner,
        repo,
        args.reconcile,
        args.max_pages.unwrap_or(10),
    )
    .await
}

/// Connectors are feature-gated; surface a clear message when the build omits
/// them rather than failing obscurely.
#[cfg(not(feature = "connectors"))]
async fn execute_github(
    _storage: &Arc<Storage>,
    _owner: &str,
    _repo: &str,
    _reconcile: bool,
    _max_pages: usize,
) -> Result<Value, String> {
    Err("This Vestige build was compiled without the 'connectors' feature. \
         Rebuild with --features connectors to enable source_sync."
        .to_string())
}

#[cfg(feature = "connectors")]
async fn execute_github(
    storage: &Arc<Storage>,
    owner: &str,
    repo: &str,
    reconcile: bool,
    max_pages: usize,
) -> Result<Value, String> {
    use vestige_core::connectors::github::{GithubConfig, GithubConnector};
    use vestige_core::connectors::run_sync;

    let config = GithubConfig::new(owner, repo).with_token(github_token());
    let connector =
        GithubConnector::new(config).map_err(|e| format!("connector init failed: {e}"))?;

    let report = run_sync(storage.as_ref(), &connector, reconcile, max_pages)
        .await
        .map_err(|e| format!("sync failed: {e}"))?;

    let scope = format!("{owner}/{repo}");
    let total = report.created + report.updated + report.unchanged;
    let authed = github_token().is_some();

    let summary = format!(
        "Synced {scope}: {} created, {} updated, {} unchanged{} ({total} records seen{}).",
        report.created,
        report.updated,
        report.unchanged,
        if report.reconciled {
            format!(", {} tombstoned", report.tombstoned)
        } else {
            String::new()
        },
        if authed { "" } else { ", unauthenticated" },
    );

    Ok(json!({
        "ok": true,
        "summary": summary,
        "source": "github",
        "scope": scope,
        "created": report.created,
        "updated": report.updated,
        "unchanged": report.unchanged,
        "tombstoned": report.tombstoned,
        "reconciled": report.reconciled,
        "cursor": report.new_cursor.map(|d| d.to_rfc3339()),
        "authenticated": authed,
        "warnings": report.warnings,
        "hint": if total == 0 && !authed {
            "No records returned. For private repos or higher rate limits, set GITHUB_TOKEN in the server environment."
        } else if report.new_cursor.is_some() && total >= 100 {
            "More may remain — run source_sync again to continue from the saved cursor."
        } else {
            "Search these with the normal search tools; results cite the GitHub issue URL."
        }
    }))
}
