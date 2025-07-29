# Metasploit MCP Server

A Model Context Protocol (MCP) server for interacting with the Metasploit Framework.

## Features

- List exploits and payloads
- Generate payloads
- Run exploits, post modules, and auxiliary modules
- Manage sessions and listeners
- Send commands to active sessions

## Installation

```bash
pip install gc-metasploit
```

Or install with uvx:

```bash
uvx gc-metasploit
```

## Usage

Ensure Metasploit RPC is running:

```bash
msfrpcd -P your_password -S -a 127.0.0.1
```

Then start the MCP server:

```bash
# As a command-line tool (HTTP/SSE mode by default):
gc-metasploit

# Or as a module:
python -m gc_metasploit.server

# Specify transport mode and options:
gc-metasploit --transport http --host 0.0.0.0 --port 8085
gc-metasploit --transport stdio
```

### Transport Options

The server supports two transport methods:

- **HTTP/SSE (Server-Sent Events)**: Default mode for interoperability with most MCP clients
- **STDIO (Standard Input/Output)**: Used with Claude Desktop and similar direct pipe connections

For Claude Desktop integration, configure `claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "metasploit": {
            "command": "gc-metasploit",
            "args": [
                "--transport",
                "stdio"
            ],
            "env": {
                "MSF_PASSWORD": "yourpassword"
            }
        }
    }
}
```

For other MCP clients that use HTTP/SSE:

1. Start the server in HTTP mode (default):
   ```bash
   gc-metasploit --transport http --host 0.0.0.0 --port 8085
   ```

2. Configure your MCP client to connect to:
   - SSE endpoint: `http://your-server-ip:8085/sse`

### Environment Variables

- `MSF_PASSWORD`: Metasploit RPC password (default: 'yourpassword')
- `MSF_SERVER`: Metasploit RPC server (default: '127.0.0.1')
- `MSF_PORT`: Metasploit RPC port (default: '55553')
- `MSF_SSL`: Use SSL (default: 'false')
- `PAYLOAD_SAVE_DIR`: Directory to save generated payloads (default: '~/payloads')

## License

Apache 2.0