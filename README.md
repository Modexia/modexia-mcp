# Modexia AgentPay: Deep Context & Developer Guide

## 1. Introduction & Overview
Modexia is a financial infrastructure layer built specifically for autonomous AI agents. It bridges Web2 authentication (Supabase) with Web3 Smart Contract Accounts (ERC-4337 on the Base Network). 

This allows an AI agent to programmatically control a non-custodial wallet and make fast, cheap payments (USDC) to other agents, services, or users without needing to manage complex crypto infrastructure directly.

## 2. Architecture & Security Model

### 2.1 Current State: API Key & Managed Wallets
Currently, ModexiaAgentpay prioritizes developer experience and simple integration. Agents interact with the protocol primarily through **API Keys**. The Modexia platform acts as a trusted facilitator that manages the underlying blockchain complexity on behalf of the agent.

#### Flow:
1. **Developer Setup:** A developer registers on the Modexia platform and receives an API Key. Underlying this account is a Circle Developer-Controlled Wallet (managed by Modexia).
2. **Channel Opening (On-Chain):** When the developer's agent needs to pay a provider, the backend (using the API Key for auth) triggers a transaction to lock USDC into the `ModexiaVault` smart contract.
3. **Usage (Off-Chain):** The agent consumes the provider's API. The Modexia backend tracks the usage and the amount owed off-chain in its database.
4. **Settlement:** When the consumption ends, the Modexia backend (acting on behalf of the agent) submits the final owed amount to the `ModexiaVault` contract via `settleChannel()`. The Vault distributes the USDC to the provider, takes a platform fee, and refunds the rest to the agent's wallet.

### 2.2 Future State: Trustless State Channels (EIP-712)
Eventually, Modexia will upgrade to **Fully Trustless State Channels** using cryptographic signatures, where the agent environment manages its own private key and signs "Receipts" (micro-payments) off-chain, which the provider directly submits to the `ModexiaVault` contract.

## 3. SDK Capabilities (Python)
Currently, Modexia is interacted with via the Python SDK (`modexiaagentpay`).

### Installation
`pip install modexiaagentpay`

### Initialization
Authentication and environment selection are handled via the API Key prefix:
- `mx_test_...` -> Targets Sandbox (Base-Sepolia)
- `mx_live_...` -> Targets Production (Base-Mainnet)

```python
from modexia import create_client
client = create_client(api_key="mx_test_...")
```

### Core Operations

#### 1. Checking Balance
Returns the available USDC balance of the Agent's Smart Contract Wallet.
```python
balance = client.retrieve_balance() # or client.get_balance()
print(f"Balance: {balance} USDC")
```

#### 2. Direct Payment (Transfer Funds)
Sends USDC to a specific wallet address. The platform charges a 1% fee on top of the amount.
```python
receipt = client.transfer(
    recipient="0x7d5...",
    amount=5.00,       # Amount in USDC (Decimal)
    wait=True,         # Poll for blockchain finality (Recommended)
    idempotency_key="task_123" # Optional: Prevent double-spend
)
```

#### 3. Smart Fetch (x402 / Paywall Negotiation)
A wrapper around HTTP GET. Automatically detects `402 Payment Required`, parses the `WWW-Authenticate` header for price/destination, pays the invoice via Modexia, and retries the request with a proof-of-payment header.
```python
# Automatically pays if status is 402
response = client.smart_fetch("https://premium-api.com/data")
```

#### 4. Vault Channels (Micro-payments)
For high-frequency or streaming capability:
1. `client.open_channel(provider, depositAmount)` locks funds on-chain.
2. `client.consume_channel(channelId, amount)` pays a small amount instantly via backend tracking.
3. `client.settle_channel(channelId)` closes the channel and settles on-chain.

## 4. Building RAG & AI Agents with Modexia
When building AI Agents using Modexia (especially with TS tools like Vercel AI SDK or MCP), the Agent needs precise context.

### RAG Integration
If your agent receives a request to perform a payment, but needs to check policies or external constraints first, it should leverage Retrieval-Augmented Generation (RAG). By reading this documentation (often exposed via MCP resources), the AI can understand that a `transfer` must be provided a valid `0x...` string and a decimal amount.

### Best Practices for AI Integration
- **Idempotency Keys:** Agents should ALWAYS generate a unique standard string (like a combination of the task ID and step) for the `idempotency_key` when calling payment features to avoid double-charging if the AI retries the action.
- **Error Handling:** AI agents should be aware of `ModexiaPaymentError` (insufficient funds, limit exceeded) and `ModexiaAuthError`. If a 402 Error is received dynamically, agents can use the `smart_fetch` command or manually instruct the transfer command.
- **Gas Fees:** The AI should know that it does NOT need ETH. Gas fees are sponsored by the Modexia Paymaster. Limits are purely enforced in USDC.
