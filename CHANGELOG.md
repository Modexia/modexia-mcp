---
noteId: "df9fa6f04bd711f1ba5939de03e16c35"
tags: []

---

# Changelog

All notable changes to the Modexia MCP Server (`modexia-mcp`) will be documented in this file.

## [0.3.0] - 2026-05-09

### 🚀 Intent-to-Pay Integration

AI agents can now make payments through a cryptographically signed intent pipeline with rich compliance feedback.

#### Added

- **`submit_intent(recipient, amount, memo)`** — New MCP tool. Creates a signed intent, submits through the 11-step validation pipeline, and returns rich compliance metadata including `daily_spent`, `daily_remaining`, `wallet_balance_after`, and actionable `suggestion` on rejection.
- **`get_intent(intent_id)`** — New MCP tool. Look up the status and details of a previously submitted payment intent by UUID.
- **`list_intents(limit)`** — New MCP tool. List recent payment intents for audit trail review.
- **`create_intent_payment_instruction`** — New prompt. Guides agents on using the v2 intent system: prefer `submit_intent`, always include memo, read suggestions, use `daily_remaining` for planning.

#### Changed

- **`transfer()`** — Now accepts an optional `memo` parameter for audit trail visibility.
- **`get_history()`** — Now surfaces the `memo` field on each transaction in the response.
- Bumped `modexiaagentpay` dependency to `>=0.7.0`.

### 🔒 Security

- Intent tokens are HMAC-SHA256 signed using the API key — tamper-proof.
- Replay protection via nonce uniqueness enforcement.
- Intent expiry validation (default 5 minutes TTL).
- Token size limited to 10KB (DoS prevention).
- Memo truncated to 500 characters (DB bloat prevention).

---

## [0.2.1] - 2026-04-18

### Security

- Updated dependencies to resolve known vulnerabilities.

---

## [0.2.0] - 2026-04-15

### Added

- **Vault Channel Tools:** `open_channel`, `consume_channel`, `settle_channel`, `get_channel`, `list_channels` for high-frequency micropayments.
- **Cross-Chain Transfer:** `cross_chain_transfer` tool for CCTP-based transfers via Squid Router.
- **`smart_fetch`** — Auto-negotiate 402 HTTP paywalls.
- **`setup_microtransactions_instruction`** — Prompt for vault channel workflow.

---

## [0.1.0] - 2026-03-01

### Added

- Initial public release.
- `get_balance`, `transfer`, `get_history` tools.
- `create_payment_instruction` prompt.
- `modexia://docs/llms_context` resource.
- stdio and SSE transport support.
