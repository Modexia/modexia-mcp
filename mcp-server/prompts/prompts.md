---
noteId: "9ebce36022ff11f182bc41f86b073160"
tags: []

---

# Modexia MCP Prompts

The following prompts should be exposed by the MCP server so that AI clients and agents can easily load them to perform specific tasks.

## 1. Create a Payment (`create_payment`)
**Description:** Helps the agent send a secure, standard payment using Modexia.
**Arguments:** `recipient` (string), `amount` (number/string), `reason` (string, optional).

**Context / Prompt Template:**
```text
You are an autonomous financial agent utilizing the Modexia MCP Server.
You have been requested to send {amount} USDC to {recipient}.

Before proceeding, please run the `get_balance` tool to ensure you have sufficient funds to cover the amount plus a 1% platform fee.
If you have sufficient balance:
1. Generate a unique idempotency key based on your current task ID or timestamp to prevent accidental double-spend.
2. Call the `transfer` tool with the recipient address, amount, and your idempotency key.
3. Wait for the transaction to complete and report the transaction hash and success status back to the user.

If the transaction fails with a `ModexiaPaymentError`, check if it's due to server-side daily limits or insufficient funds, and inform the user. Do not attempt to acquire native ETH for gas, as all Modexia transactions are gas-sponsored.
```

## 2. Setup High-Frequency Micro-payments (`setup_microtransactions`)
**Description:** Guides the agent in opening a vault channel for high-frequency streaming payments.
**Arguments:** `provider_address` (string), `deposit_amount` (number/string).

**Context / Prompt Template:**
```text
You need to establish a high-frequency micro-payment channel with {provider_address} using {deposit_amount} USDC.

Please initiate the channel setup using the following steps:
1. Verify utilizing `get_balance` that you have at least {deposit_amount} USDC available.
2. Use the `open_channel` tool to lock your deposit into the ModexiaVault for this provider. 
3. Note the returned `channelId`.
4. From now on, whenever you consume a resource from this provider, do NOT call `transfer`. Instead, use the `consume_channel` tool with the `channelId` and the micro-payment amount (e.g., 0.05).
5. When the interaction with the provider is fully completed, or the task is done, remember to call `settle_channel` to finalize the off-chain interactions and refund any remaining locked deposit.

Remember to log the channelId securely so you can reuse it across multiple turns in this session.
```

## 3. Handle 402 Paywalls (`negotiate_paywall`)
**Description:** Instructs the LLM on what to do when an API or service responds with a 402 Payment Required status.

**Context / Prompt Template:**
```text
You have encountered a `402 Payment Required` HTTP status from an external service.
Do not fail the current task. Instead, inspect the `WWW-Authenticate` header from the response. 
Extract the `amount` and the `destination` (recipient address). 
If the amount is reasonable for your current operational budget, use the `transfer` tool to pay the requested amount via Modexia. Once the payment succeeds, capture the `txId` or `txHash`.
Re-attempt the HTTP request to the external service, including the header: `X-Payment-Proof: <txId>` (or the format requested by the L402 spec).
```
