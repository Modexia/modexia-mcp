<div align="center">
  <img src="assets/modexialogo.png" alt="Modexia Logo" width="120" style="border-radius: 20px; margin-bottom: 20px;" />
  <h1>Modexia AgentPay MCP Server</h1>
  <p><b>The official Model Context Protocol (MCP) server for autonomous AI Agents to interact with Modexia's crypto infrastructure.</b></p>
  
  [![PyPI version](https://badge.fury.io/py/modexia-mcp.svg)](https://badge.fury.io/py/modexia-mcp)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</div>
[![MCP Badge](https://lobehub.com/badge/mcp/modexia-modexia-mcp)](https://lobehub.com/mcp/modexia-modexia-mcp)

<br />

Welcome to the **Modexia AgentPay MCP Server** (`modexia-mcp`). This server bridges the gap between Large Language Models and the real-world digital economy.

By integrating this standard Model Context Protocol (MCP) server into your AI stack (Claude Desktop, LobeChat, Dify, or custom multi-agent swarms), you instantly equip your AI Agents with a **programmatic Smart Contract Wallet**. 

Instead of your agents hitting `402 Payment Required` errors and failing, they can now autonomously negotiate paywalls, purchase premium data, execute zero-gas microtransactions via Circle Gateway, and trade compute resources with other agents in high-frequency vault channels. 

**Modexia gives your AI a bank account, and MCP gives it the tools to use it.**

---

## What's New in v0.4.1

**Circle Gateway Nanopayments (x402)**
This release brings full agentic support for gas-free, sub-cent microtransactions directly to the MCP level.

* `nanopay` — Fetch an x402-protected URL and automatically negotiate the payment using EIP-3009 offline signatures. Includes inline auto-refill logic.
* `nanopay_activate` — One-time activation for the agent.
* `nanopay_deposit` / `nanopay_withdraw` — Manage gateway funds directly from the main wallet.
* `nanopay_balance` — Track the True Available Balance (Gateway deposits minus pending/unsettled signatures).
* **Structured Error Handling** — The MCP tools now pass back structured `ModexiaPaymentError` codes (e.g., `INSUFFICIENT_MAIN_BALANCE`) so the LLM can reason about failures and take corrective action.

---

## Previous: What's New in v0.3.0 (Intent-to-Pay)

**Intent-Based Payments (v2)**
Execute standard USDC payments through a strict compliance pipeline with rich feedback.

* `submit_intent` — Create a signed intent, validate against policies, and execute on-chain.
* `get_intent` / `list_intents` — Audit trail and tracking.

---

## Features

- **Circle Gateway Integration:** Direct programmatic access to Circle's USDC nanopayment infrastructure.
- **Gas-Free Microtransactions:** Send payments as low as $0.000001 with zero blockchain fees.
- **EIP-3009 Offline Signatures:** Secure, off-chain payment authorizations that prevent double-spending.
- **Intent-Based Routing:** Strict policy enforcement, daily spend limits, and cryptographic audit trails.
- **Automated Paywall Negotiation:** Automatically detect `402 Payment Required` headers and fulfill them inline.
- **Smart Auto-Refill:** Seamlessly top-up gateway balances from the main wallet when funds run low.

---

## Exposed MCP Components

### Tools

| Tool Name | Description |
|-----------|-------------|
| `nanopay` | Auto-negotiate and pay for `402 Payment Required` URLs using EIP-3009 offline signatures. |
| `nanopay_activate` | One-time activation command to enable Circle Gateway nanopayments for the agent. |
| `nanopay_deposit` | Deposit funds from the main agent wallet to the nanopayment Gateway. |
| `nanopay_withdraw` | Withdraw unused funds from the Gateway back to the main wallet. |
| `nanopay_balance` | Check the True Available Balance (Gateway deposits minus pending signatures). |
| `submit_intent` | Execute a standard USDC payment with compliance and policy enforcement. |
| `get_intent` | Retrieve the status and compliance metadata of a previously submitted payment intent. |
| `list_intents` | Fetch recent payment intents for audit trail review. |
| `open_channel` | Lock funds into a smart contract for high-frequency micro-transactions. |
| `consume_channel` | Execute instant, gas-free micro-payments inside an open channel. |
| `settle_channel` | Close the vault and distribute funds on-chain. |
| `get_channel` | Check the current capacity and state of a specific payment channel. |
| `list_channels` | List all payment channels associated with the agent's wallet. |
| `get_balance` | Retrieve the current USDC balance of the agent's primary Smart Contract Wallet. |
| `get_history` | Fetch the recent transaction history for the agent. |
| `transfer` | Execute a standard synchronous USDC transfer (v1). |
| `cross_chain_transfer` | Execute a cross-chain CCTP payment via Squid Router (e.g., Ethereum -> Akash). |
| `smart_fetch` | Legacy HTTP auto-negotiation for HTTP-based Paywalls. |

### Prompts

| Prompt Name | Description |
|-------------|-------------|
| `nanopay_usage_instruction` | Best practices for funding the gateway and executing `nanopay` operations. |
| `create_intent_payment_instruction` | Rules for structuring compliant payments, adding memos, and handling policy rejections. |
| `setup_microtransactions_instruction` | Step-by-step guide on opening, consuming, and settling vault channels. |
| `create_payment_instruction` | Standard rules for legacy idempotency-based transfers. |

### Resources

| Resource URI | Description |
|--------------|-------------|
| `modexia://docs/llms_context` | The complete Modexia Developer Protocol Guide with overarching economic rules for swarms. |

---

## Configuration & Setup

This server requires a Modexia API Key to function. You can obtain one by creating a developer account at [modexia.software](https://modexia.software).

| Variable | Description |
|----------|-------------|
| `MODEXIA_API_KEY` | **Required.** Your Modexia developer key (e.g. `mx_test_...`) |
| `MODEXIA_BASE_URL` | Optional. Overrides the API endpoint. Defaults to the Sandbox Environment. |

### Using `uvx` (Recommended)
You can run this server directly in any MCP client that supports standard executable commands:
```bash
uvx modexia-mcp
```

### Claude Desktop
To use Modexia with Claude Desktop, add the following to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "modexia": {
      "command": "uvx",
      "args": ["modexia-mcp"],
      "env": {
        "MODEXIA_API_KEY": "mx_test_YourApiKeyHere"
      }
    }
  }
}
```

---

## Contributing to Open Source

We actively welcome community contributions to make this MCP server even better. Because it acts as the primary interface for autonomous AI agents, we heavily prioritize stability and strict prompt engineering.

1. **Clone the Repo:** `git clone https://github.com/Modexia/modexia-mcp.git`
2. **Install Dependencies:** `pip install -e .`
3. **Run Locally:** You can run the server in stdio mode for local testing via `python -m modexia_mcp`
4. **Submit PRs:** Open a Pull Request targeting the `main` branch.

---

## Security Model
The Modexia MCP Server **never** exposes your private keys to the LLM context. The AI only has permission to trigger explicitly configured MCP tools. Policy limits (e.g., maximum daily spend, hourly caps) are enforced automatically on the Modexia backend. Even a hallucinating AI cannot drain your wallet above your predefined guards.

## License & Support
**modexia-mcp** is an open-source tool governed by the [MIT License](LICENSE). 

Need help scaling your agent swarm or configuring your API keys? Access your developer dashboard and explore the docs at [modexia.software](https://modexia.software).
