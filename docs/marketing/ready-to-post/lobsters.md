Vestige Receipt Lock: local MCP guard against unverified "tests passed" agent claims

Tags: rust, programming, security

---

Your coding agent probably ends sessions with "all tests passed" or "the build is green."

Vestige (MCP memory server, Rust, local) adds optional Receipt Lock: operational claims are checked against structured command receipts from the transcript. No matching successful receipt → claim can be blocked; inspectable veto at ~/.vestige/sanhedrin/latest.html

```bash
npm install -g vestige-mcp-server@latest
claude mcp add vestige vestige-mcp -s user
vestige sandwich install --enable-sanhedrin
```

Same binary also does FSRS-6 cognitive memory (decay, dreaming, 3D dashboard). v2.1.23, ~86K LOC, 25 tools, AGPL-3.0.

https://github.com/samvallad33/vestige
https://github.com/samvallad33/vestige/blob/main/docs/comparison.md
