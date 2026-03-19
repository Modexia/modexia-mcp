## 🏦 Modexia AgentPay MCP

This repository contains the **Modexia AgentPay MCP Server** implementation plus supporting assets and configuration used during development.

- **MCP server package**: `mcp-server/` (published to PyPI as `modexia-mcp`)
- **Entry point**: `mcp-server/server.py`
- **Docs & prompts**: `mcp-server/docs/`, `mcp-server/prompts/`

For day‑to‑day usage of the MCP server (e.g., with Claude Desktop), please see the detailed guide in `mcp-server/README.md`.

## 📁 Repository Layout

- `mcp-server/` – Python MCP server package and development environment  
  - `server.py` – main MCP server implementation  
  - `pyproject.toml` – Python project metadata and dependencies  
  - `docs/modexia_context.md` – additional design and context docs  
  - `prompts/prompts.md` – prompt templates and examples  
  - `claude_desktop_config.json` – example Claude Desktop MCP config  
- `LICENSE` – Apache 2.0 license for this repo

## 🧩 Using the MCP Server

You normally **do not need to clone this repo** to use Modexia AgentPay with an MCP‑compatible client. Instead, configure your client to run the published PyPI package.

For example, in Claude Desktop you can use the config from `mcp-server/README.md`, which looks like:

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

See `mcp-server/README.md` for:

- **Installation & setup**
- **Tool descriptions** (`get_balance`, `get_history`, `transfer`, channel tools, `smart_fetch`, etc.)
- **Security model & best practices**

## 🛠 Development

If you are working on the MCP server itself:

1. Change into the server directory:
   ```bash
   cd mcp-server
   ```
2. Create/activate a Python environment (e.g., with `uv`, `venv`, or your preferred tool).
3. Install dependencies using `pyproject.toml` (for `uv`, `uv sync`).
4. Run tests or experiments using the example scripts such as `test_history.py`.

Follow the guidelines in `mcp-server/README.md` and `docs/modexia_context.md` for more details on the protocol behavior and intended usage.

