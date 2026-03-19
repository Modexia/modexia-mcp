import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from typing import Optional
import sys

# We suppress import errors in case modexiaagentpay isn't fully installed yet.
try:
    from modexia import ModexiaClient
except ImportError:
    ModexiaClient = None

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

# We set up a FastMCP instance. FastMCP automatically creates tools/resources/prompts via decorators
mcp_server = FastMCP(
    "ModexiaAgentpay",
    dependencies=["modexiaagentpay", "python-dotenv"]
)

def get_modexia_client():
    if ModexiaClient is None:
        raise RuntimeError("modexiaagentpay is not installed properly.")
        
    api_key = os.getenv("MODEXIA_API_KEY")
    base_url = os.getenv("MODEXIA_BASE_URL", "https://sandbox.modexia.software")
    if not api_key:
        raise ValueError("MODEXIA_API_KEY environment variable is missing. It must be provided (e.g. mx_test_...).")
    
    import sys
    print(f"🪲 [DEBUG] Running tool using base_url: {base_url}", file=sys.stderr)
    
    # We pass base_url explicitly in case python-dotenv missed it or it wasn't exported globally
    return ModexiaClient(api_key=api_key, base_url=base_url)

# -----------------
# TOOLS
# -----------------
@mcp_server.tool()
def get_balance() -> str:
    """Retrieve the current USDC wallet balance for the Agent's Smart Contract Wallet."""
    client = get_modexia_client()
    return client.retrieve_balance()

@mcp_server.tool()
def transfer(recipient: str, amount: float, idempotency_key: Optional[str] = None) -> dict:
    """
    Send a standard Modexia payment (USDC) to a recipient.
    Recommended to always provide an idempotency_key to prevent double charges.
    """
    client = get_modexia_client()
    
    try:
        receipt = client.transfer(recipient, amount, wait=True, idempotency_key=idempotency_key)
        
        return {
            "success": receipt.success,
            "txId": getattr(receipt, "txId", None),
            "status": getattr(receipt, "status", "COMPLETE"),
            "txHash": getattr(receipt, "txHash", None),
            "errorReason": getattr(receipt, "errorReason", None)
        }
    except TimeoutError as e:
        # Blockchain took longer than 30s, but it was submitted
        return {
            "success": True,
            "status": "PENDING",
            "message": "Transaction submitted successfully but is taking longer than usual to settle on the blockchain.",
            "errorReason": str(e)
        }

@mcp_server.tool()
def get_history(limit: int = 5) -> dict:
    """Fetch the recent transaction history for the authenticated agent."""
    client = get_modexia_client()
    resp = client.get_history(limit=limit)
    return {
        "transactions": [
            {
                "txId": getattr(t, "txId", ""), 
                "amount": getattr(t, "amount", ""), 
                "state": getattr(t, "state", ""), 
                "providerAddress": getattr(t, "providerAddress", "")
            }
            for t in resp.transactions
        ],
        "hasMore": getattr(resp, "hasMore", False)
    }

@mcp_server.tool()
def open_channel(provider: str, deposit_amount: float, duration_hours: float = 24.0) -> dict:
    """
    Open a high-frequency micro-payment vault channel with on-chain deposit.
    Blocks funds for the specific provider, allowing instant, gas-free payments via `consume_channel`.
    """
    client = get_modexia_client()
    return client.open_channel(provider, deposit_amount, duration_hours)

@mcp_server.tool()
def consume_channel(channel_id: str, amount: float, idempotency_key: Optional[str] = None) -> dict:
    """
    Execute an instant, gas-free micro-payment inside an already open channel.
    Call this as many times as needed while the channel is open.
    """
    client = get_modexia_client()
    res = client.consume_channel(channel_id, amount, idempotency_key=idempotency_key)
    return {
        "success": getattr(res, "success", False),
        "remaining": getattr(res, "remaining", "0"),
        "isDuplicate": getattr(res, "isDuplicate", False)
    }

@mcp_server.tool()
def settle_channel(channel_id: str) -> dict:
    """Settle an open micro-payment channel, paying the provider, and refunding the remainder back to you."""
    client = get_modexia_client()
    return client.settle_channel(channel_id)

@mcp_server.tool()
def get_channel(channel_id: str) -> dict:
    """Get the current status, deposit amount, and remaining balance of a specific payment channel."""
    client = get_modexia_client()
    status = client.get_channel(channel_id)
    return {
        "channelId": getattr(status, "channelId", channel_id),
        "providerAddress": getattr(status, "providerAddress", ""),
        "deposit": getattr(status, "deposit", "0"),
        "remaining": getattr(status, "remaining", "0"),
        "state": getattr(status, "state", ""),
        "isExpired": getattr(status, "isExpired", False)
    }

@mcp_server.tool()
def list_channels(limit: int = 50) -> dict:
    """List all payment channels associated with the authenticated agent's wallet."""
    client = get_modexia_client()
    channels = client.list_channels(limit=limit)
    return {
        "channels": [
            {
                "channelId": getattr(c, "channelId", ""),
                "providerAddress": getattr(c, "providerAddress", ""),
                "deposit": getattr(c, "deposit", "0"),
                "remaining": getattr(c, "remaining", "0"),
                "state": getattr(c, "state", "")
            } for c in channels
        ]
    }

@mcp_server.tool()
def smart_fetch(method: str, url: str) -> dict:
    """
    Fetch an external resource via HTTP. If the resource responds with a 402 Payment Required
    and a WWW-Authenticate header, this tool will automatically negotiate and pay the invoice 
    via Modexia AgentPay, then retry the request with the cryptographic proof of payment.
    """
    client = get_modexia_client()
    resp = client.smart_fetch(method, url)
    try:
        data = resp.json()
    except Exception:
        data = resp.text[:2000] # truncate pure text
    
    return {
        "status_code": resp.status_code,
        "data": data
    }

# -----------------
# RESOURCES
# -----------------
@mcp_server.resource("modexia://docs/llms_context")
def get_modexia_context() -> str:
    """
    Retrieve the comprehensive Modexia developer guide, containing rules on 
    how AI agents should execute payments, open channels, and handle 402 Paywalls.
    Always read this before performing complex financial operations on Modexia.
    """
    # The absolute path to the context we created
    file_path = "/home/modaniels/Documents/MODEXIA/ModexiaAgentpay/apps/web/public/llms.txt"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading Modexia context: {str(e)}"

# -----------------
# PROMPTS
# -----------------
@mcp_server.prompt()
def create_payment_instruction() -> str:
    """Provides internal guidelines to an agent on how to correctly structure a standard payment with Modexia."""
    return (
        "You are an autonomous financial agent utilizing the Modexia MCP Server. "
        "Before proceeding with a payment, run `get_balance` to ensure sufficient funds (+1% fee). "
        "1. Generate a unique idempotency key based on your task ID. "
        "2. Call `transfer` with the recipient address, amount, and idempotency key. "
        "3. Wait for the transaction and report success. "
        "Do NOT try to acquire ETH. Gas is sponsored by Modexia."
    )

@mcp_server.prompt()
def setup_microtransactions_instruction() -> str:
    """Provides internal guidelines to an agent on how to securely open and use a micro-payment channel."""
    return (
        "You need to establish a high-frequency payment channel using Modexia. "
        "1. `get_balance` to verify deposit is available. "
        "2. Call `open_channel` to lock the deposit into a ModexiaVault for the provider. "
        "3. Log the returned `channelId`. "
        "4. From now on, use `consume_channel` with `channelId` and micro-amounts. "
        "5. Once entirely done, call `settle_channel`."
    )


def main():
    import sys
    import os
    port = os.getenv("PORT")

    if port:
        print(f"🚀 Starting Modexia MCP Server on SSE transport (Port {port})...", file=sys.stderr)
        mcp_server.run(transport='sse', host='0.0.0.0', port=int(port))
    else:
        print("🚀 Modexia MCP Server is running locally on stdio transport and waiting for connections...", file=sys.stderr)
        mcp_server.run(transport='stdio')

if __name__ == "__main__":
    main()
