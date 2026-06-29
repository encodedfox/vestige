<div align="center">

<h1>Vestige</h1>

### Your AI has the memory of a goldfish. Vestige gives it a hippocampus.

<em>Local-first cognitive memory for AI agents. 130 years of neuroscience, compiled into one 23MB Rust binary. Zero cloud. Your data never leaves your machine.</em>

[![GitHub stars](https://img.shields.io/github/stars/samvallad33/vestige?style=for-the-badge&logo=github&color=8b5cf6)](https://github.com/samvallad33/vestige/stargazers)
[![Release](https://img.shields.io/github/v/release/samvallad33/vestige?style=for-the-badge&color=06b6d4)](https://github.com/samvallad33/vestige/releases/latest)
[![Tests](https://img.shields.io/badge/tests-1550_passing-22c55e?style=for-the-badge)](https://github.com/samvallad33/vestige/actions)
[![License](https://img.shields.io/badge/license-AGPL--3.0-3b82f6?style=for-the-badge)](LICENSE)

[**⚡ Quick Start**](#-60-second-start) · [**🧠 Why It's Different**](#-why-this-isnt-rag-with-a-fancy-name) · [**🔬 The Science**](#-this-is-real-neuroscience-not-a-metaphor) · [**🛠 13 Tools**](#-13-tools-one-brain) · [**📊 Dashboard**](#-watch-your-ai-think-in-3d)

</div>

---

> ### The moment that made this real
>
> You spent 40 minutes last Tuesday explaining to your agent why the staging connection pooler corrupts data during migrations. You moved on.
>
> Today — new session, new context window — it cheerfully suggests *disabling the pooler during a migration.* The lesson is gone. The agent that "remembers everything" remembers **nothing** that matters.
>
> **Vestige is the fix.** Not a bigger context window. Not a vector dump. A memory that **decides what to keep, reaches backward to find the root cause of a failure, and tells you when you're about to contradict something you already learned.**

---

## ⚡ 60-second start

```bash
npm install -g vestige-mcp-server@latest      # 1. install (one binary, no Docker, no API key)
claude mcp add vestige vestige-mcp -s user    # 2. connect to Claude Code
```

That's it. Now talk to your agent like it has a memory — because now it does:

```
You:  "Remember: we always disable SimSIMD on release builds, it breaks old x86 CPUs."
        ...days later, fresh session, zero context...
You:  "Should I enable SimSIMD for the release?"
AI:   ⚠️ Your claim contradicts a stored decision — you decided to DISABLE it (it breaks old x86 CPUs).
```

> That last line is **`claim_contradicts_memory`** — a real status the engine returns. Most memory systems give you confident silence. Vestige tells you when you're about to repeat a mistake. *(Works with Codex, Cursor, VS Code, Claude Desktop, Windsurf, JetBrains, Zed — anything that speaks MCP. [Full setup ↓](#-works-in-every-editor-you-use))*

---

## 🧠 Why this isn't "RAG with a fancy name"

RAG is a bucket. You throw everything in and hope nearest-neighbor finds it later. Vestige is an **active organ** — it gates what enters, lets the unimportant fade, and reasons across what's left.

|  | 🪣 RAG / Vector Store | 🧠 Vestige |
|---|---|---|
| **What it stores** | Everything you give it | Only what's **surprising or new** (Prediction-Error Gating — the hippocampal bouncer) |
| **What it forgets** | Nothing — bloats forever | Unused memories **decay** on the real FSRS-6 forgetting curve; context stays lean |
| **Finding the root cause** | Can't — the cause isn't *similar* to the bug | **Reaches backward in time** to the causally-upstream memory (the headline v2.2 feature ↓) |
| **Contradictions** | Silent — happily serves the stale answer | Returns **`claim_contradicts_memory`** and shows you the conflict |
| **Duplicates** | You dedup by hand | Self-heals: *"likes dark mode"* + *"prefers dark themes"* → merged |
| **Forgetting on demand** | DELETE only | **`suppress`** — compounding top-down inhibition, neighbor cascade, reversible for 24h |
| **Consolidation** | None | **Dreams** — replays memories, finds hidden connections, synthesizes insights |
| **Where it lives** | Usually someone else's cloud | **100% on your machine.** One binary. No telemetry. |

---

## 🔥 The feature no other AI memory has: Memory with hindsight

Here's the thing vector search **structurally cannot do.**

A bug appears today. The root cause was a quiet decision you made *three weeks ago* — a changed env var, a config tweak, a service you swapped. That root cause is **not similar to the bug.** It shares no keywords. A vector search will never surface it, because it's not *similar* — it's *causally upstream.*

Vestige's **Retroactive Salience Backfill** — a faithful port of **Zaki/Cai et al., 2024, *Nature* 637:145–155** (offline ensemble co-reactivation links memories across days) — does what your brain does after a failure: it **reaches backward through time**, finds the dormant memory that *caused* this, and promotes it — because they share an **entity** (the same file, env var, or service), not because they share words.

```bash
vestige backfill --contrast      # show the root cause a vector search would have missed
```

> **Run 2 is smarter than run 1.** Every failure your agent records makes the *next* session diagnose faster. That compounding is the moat — and it runs automatically inside consolidation, no babysitting.

This shipped in **v2.2.0** alongside a 34→13 tool consolidation and a rebuilt retrieval engine. [Full release notes →](https://github.com/samvallad33/vestige/releases/tag/v2.2.0)

---

## 🔬 This is real neuroscience, not a metaphor

Every mechanism below is a cited paper, implemented in Rust, running locally. This is the difference between *"we use embeddings"* and *a memory system.*

| Mechanism | What it does for you | Grounded in |
|---|---|---|
| **Prediction-Error Gating** | Redundant info gets merged, contradictory gets superseded, only the novel gets stored | The hippocampal novelty signal |
| **FSRS-6 Spaced Repetition** | 21 parameters of the mathematics of forgetting — used memories stay, unused fade | Modern spaced-repetition research |
| **Retroactive Salience Backfill** | Backward causal reach to the root cause of a failure | Zaki/Cai et al. 2024, *Nature* 637:145–155 |
| **Synaptic Tagging** | A memory that looked trivial this morning can be tagged critical tonight | [Frey & Morris 1997](https://doi.org/10.1038/385533a0) |
| **Spreading Activation** | Search "auth bug," surface last week's JWT update — memory is a graph, not a list | [Collins & Loftus 1975](https://doi.org/10.1037/0033-295X.82.6.407) |
| **Dual-Strength Model** | Storage strength vs. retrieval strength — deeply stored ≠ instantly recalled, just like you | [Bjork & Bjork 1992](https://doi.org/10.1016/S0079-7421(08)60016-9) |
| **Memory Dreaming** | Sleep-like consolidation: replays, connects, synthesizes insights to a graph | Active-dreaming consolidation |
| **Active Forgetting (`suppress`)** | Top-down inhibition that *compounds* and cascades to neighbors — reversible for 24h | [Anderson 2025](https://www.nature.com/articles/s41583-025-00929-y) · [Davis 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7477079/) |

[**Read the full science doc →**](docs/SCIENCE.md) — every feature, every paper.

---

## 🛠 13 tools, one brain

v2.2.0 consolidated a sprawling 34-tool surface into **13 sharp ones** your agent actually reaches for. Old names still work as hidden aliases — nothing breaks.

| Tool | What it does |
|---|---|
| 🔍 `recall` | The retrieval engine — folds search + deep reasoning + contradiction detection into one call. F32 embeddings, Reciprocal Rank Fusion, claim-vs-memory checks. |
| 🧠 `backfill` | **Memory with hindsight** — backward causal reach to a failure's root cause (Cai 2024). |
| 💾 `smart_ingest` | Stores with CREATE / UPDATE / SUPERSEDE via Prediction-Error Gating. Batch session-end saves. |
| 🗂 `memory` | Get, edit, promote 👍, demote 👎, check state, purge content + embeddings. |
| 🧩 `graph` | Reasoning chains, associations, bridges, predictions, force-directed export. |
| 🌙 `maintain` | Consolidate, dream, GC, importance-score, backup, export, restore — one maintenance verb. |
| 🧹 `dedup` | Self-healing duplicate detection + merge (8 old tools → 1). |
| 🚫 `suppress` | Top-down active forgetting — compounds, cascades, reversible 24h. The memory is *inhibited, not erased.* |
| 📟 `memory_status` | Health + stats + trends + recommendations in one packet. |
| 🧬 `codebase` · `intention` · `source_sync` · `session_start` | Per-project code memory · "remind me when X" · external-source connectors · one-call session init. |

---

## 📊 Watch your AI think in 3D

```bash
vestige dashboard      # → http://localhost:3927/dashboard
```

Every memory is a glowing node in a real-time, force-directed 3D graph. Connections form as you work. Nodes **pulse** when accessed, **burst** on creation, **fade** on decay. Kick off a consolidation and the whole graph slides into **purple dream mode**, replaying memories that light up in sequence.

Built with SvelteKit 2 · Svelte 5 · Three.js · WebGL bloom · live WebSocket events. 1000+ nodes at 60fps. Installable as a PWA.

---

## 🧩 Works in every editor you use

Vestige speaks MCP, so any client that can register a stdio MCP server can use it.

| Editor | One-liner |
|---|---|
| **Claude Code** | `claude mcp add vestige vestige-mcp -s user` |
| **Codex** | `codex mcp add vestige -- vestige-mcp` |
| **Cursor / VS Code / Windsurf / JetBrains / Xcode / OpenCode** | [Integration guides →](docs/integrations/) |
| **Claude Desktop** | [2-minute setup →](docs/CONFIGURATION.md#claude-desktop-macos) |

<details>
<summary><b>Other install methods (Intel Mac, Windows, build-from-source)</b></summary>

**Update an existing install:**
```bash
vestige update                          # binaries only
vestige update --sandwich-companion     # also refresh optional Claude Code companion files
```

**macOS (Intel):** Microsoft is dropping x86_64 macOS ONNX Runtime prebuilts after v1.23.0, so the Intel Mac build links dynamically against a Homebrew ONNX Runtime:
```bash
brew install onnxruntime
npm install -g vestige-mcp-server@latest
echo 'export ORT_DYLIB_PATH="'"$(brew --prefix onnxruntime)"'/lib/libonnxruntime.dylib"' >> ~/.zshrc && source ~/.zshrc
claude mcp add vestige vestige-mcp -s user
```
Full guide: [`docs/INSTALL-INTEL-MAC.md`](docs/INSTALL-INTEL-MAC.md).

**Windows + Claude Desktop:** quit Claude Desktop from the tray, then in PowerShell:
```powershell
npm install -g vestige-mcp-server@latest
vestige-mcp --version
```
Point `%APPDATA%\Claude\claude_desktop_config.json` at it:
```json
{ "mcpServers": { "vestige": { "command": "vestige-mcp" } } }
```
If it can't find the command, run `where vestige-mcp` and use the exact `.cmd` path.

**Build from source (Rust 1.91+):**
```bash
git clone https://github.com/samvallad33/vestige && cd vestige
cargo build --release -p vestige-mcp
# Apple Silicon GPU: --features metal   ·   NVIDIA: --features qwen3-embeddings,cuda
```
</details>

---

## 🚀 Make your AI use memory automatically

Registering the server exposes the tools; a short instruction tells the agent *when* to call them. Drop in the protocol and your agent saves and recalls on its own:

| You say | Vestige does |
|---|---|
| *"Remember this"* | Saves immediately |
| *"I always..."* / *"I prefer..."* | Saves as a durable preference |
| *"Remind me when..."* | Creates a future trigger (`intention`) |
| *"This is important"* | Saves **and** promotes it |

[Agent memory protocol →](docs/AGENT-MEMORY-PROTOCOL.md) · [Claude Code template →](docs/CLAUDE-SETUP.md)

---

## 🏗 Under the hood

```
┌──────────────────────────────────────────────────────────┐
│  SvelteKit Dashboard — Three.js 3D graph · WebGL bloom    │
├──────────────────────────────────────────────────────────┤
│  Axum HTTP + WebSocket (:3927) — REST + live event stream │
├──────────────────────────────────────────────────────────┤
│  MCP Server (stdio JSON-RPC) — 13 tools · 30 modules      │
├──────────────────────────────────────────────────────────┤
│  Cognitive Engine                                          │
│   FSRS-6 · Spreading Activation · Prediction-Error Gating │
│   Retroactive Salience Backfill · Synaptic Tagging        │
│   Memory Dreamer · Hippocampal Index · Active Forgetting  │
├──────────────────────────────────────────────────────────┤
│  Storage — SQLite + FTS5 · USearch HNSW · Nomic Embed v1.5│
│   Optional: Qwen3 reranker · SQLCipher · Metal/CUDA       │
└──────────────────────────────────────────────────────────┘
```

| | |
|---|---|
| **Language** | Rust 2024 (MSRV 1.91) — **86,000+ lines** |
| **Binary** | ~23MB, single file |
| **Embeddings** | Nomic Embed Text v1.5 (768d→256d Matryoshka, 8192 ctx); Qwen3 optional |
| **Vector search** | USearch HNSW (≈20× faster than FAISS) |
| **Storage** | SQLite + FTS5, optional SQLCipher encryption |
| **Tests** | **1,550 passing** · clippy `-D warnings` clean |
| **First run** | Downloads ~130MB embedding model once, then **fully offline forever** |
| **Platforms** | macOS (ARM + Intel) · Linux x86_64 · Windows x86_64 — all prebuilt |

---

## 📚 Go deeper

| | |
|---|---|
| [**FAQ**](docs/FAQ.md) | 30+ real questions answered |
| [**The Science**](docs/SCIENCE.md) | Every feature, every paper |
| [**Storage Modes**](docs/STORAGE.md) | Global · per-project · multi-instance |
| [**Configuration**](docs/CONFIGURATION.md) | CLI, env vars, every knob |
| [**Changelog**](CHANGELOG.md) | The full story, version by version |

---

<div align="center">

### If your agent should remember what you taught it yesterday — star it. ⭐

<sub><b>86,000+ lines of Rust · 13 tools · 30 cognitive modules · 130 years of memory research · one 23MB binary that never phones home.</b></sub>

<sub>Built by <a href="https://github.com/samvallad33">@samvallad33</a> · AGPL-3.0 · 100% local, 100% yours</sub>

</div>
