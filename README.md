# MCP Simple Server

A minimal, reference implementation of a Model Context Protocol server with streamable HTTP transport. Built with FastMCP following the official Anthropic MCP specification 2025-06-18. Perfect starting point for building remote MCP servers.

## 🎯 Purpose

This project serves as a simple, well-documented reference for developers who want to:

- Build their first MCP server
- Deploy MCP servers to cloud platforms (Railway, Heroku, Render)
- Understand the MCP protocol implementation
- Create a foundation for more sophisticated MCP solutions

## Features

- ✅ **Two Math Tools**: `add` and `multiply` functions
- ✅ **Streamable HTTP Transport**: Modern MCP protocol with SSE support
- ✅ **Session Management**: Proper MCP initialization flow
- ✅ **Remote Deployment**: Railway, Heroku, Render deployment configs
- ✅ **Automated Testing**: Complete protocol validation and debugging tools
- ✅ **Claude Desktop Integration**: Ready for AI assistant integration
- ✅ **Reference Implementation**: Well-documented code for learning

## Quick Start

### Local Development

```bash
git clone https://github.com/oleksandrsirenko/mcp-simple-server.git
cd mcp-simple-server
uv sync
source .venv/bin/activate
python main.py
```

Server starts at: `http://localhost:8000/mcp/`

### Test the Server

```bash
python test_server.py
```

Expected output:

```
🧪 Starting MCP Server Tests
✅ Initialize successful - Server: Simple Server
✅ Initialized notification sent
✅ Found 2 tools: add, multiply  
✅ Add tool returned correct result
✅ Multiply tool returned correct result
🎉 All tests passed!
```

## Available Tools

### `add(a, b)`

Adds two numbers together.

**Example:**

```json
{"name": "add", "arguments": {"a": 25, "b": 17}}
→ Returns: 42
```

### `multiply(a, b)`

Multiplies two numbers together.

**Example:**

```json
{"name": "multiply", "arguments": {"a": 8, "b": 6}}
→ Returns: 48
```

## Manual Testing with curl

### Local Testing (Development)

For testing your local development server running on `localhost:8000`:

#### 1. Initialize Session

```bash
curl -X POST http://localhost:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
```

#### 2. Send Initialized Notification

```bash
curl -X POST http://localhost:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: YOUR_SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
```

#### 3. List Tools

```bash
curl -X POST http://localhost:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: YOUR_SESSION_ID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
```

#### 4. Call Add Tool

```bash
curl -X POST http://localhost:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: YOUR_SESSION_ID" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"add","arguments":{"a":25,"b":17}}}'
```

### Remote Testing (Production)

For testing your deployed server, replace `localhost:8000` with your deployment URL:

```bash
# Example with Railway deployment
curl -X POST https://your-app.railway.app/mcp/ \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
```

**Note**: For comprehensive remote testing, use the automated test script:

```bash
python test_deployment.py your-app.railway.app
```

## Deployment

### Railway (Recommended)

1. **Push to GitHub**:

   ```bash
   git add .
   git commit -m "ready for deployment"
   git push origin main
   ```

2. **Deploy to Railway**:

   - Go to [railway.app](https://railway.app)
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Dockerfile and deploys

3. **Test your deployment**:

   ```bash
   python test_deployment.py your-app-name.up.railway.app
   ```

4. **Your MCP URL**: `https://your-app.railway.app/mcp/`

### Heroku

```bash
heroku create your-mcp-server
git push heroku main
```

**Your MCP URL**: `https://your-mcp-server.herokuapp.com/mcp/`

### Render

1. Connect GitHub repository to Render
2. Render auto-detects `render.yaml` and Dockerfile
3. Deploys automatically

**Your MCP URL**: `https://your-service.onrender.com/mcp/`

### Docker

```bash
docker build -t mcp-simple-server .
docker run -p 8000:8000 mcp-simple-server
```

## Claude Desktop Integration

### Local Server Configuration

```json
{
  "mcpServers": {
    "simple-server": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/mcp-simple-server"
    }
  }
}
```

### Remote Server Configuration (Recommended)

For remote servers deployed to Railway, Heroku, or Render, use the `mcp-remote` package:

```json
{
  "mcpServers": {
    "simple-server-remote": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://your-app.railway.app/mcp/",
        "--allow-http",
        "--header",
        "Accept: application/json, text/event-stream"
      ]
    }
  }
}
```

**Key Configuration Notes:**

- Use `npx` with the `-y` flag to auto-install `mcp-remote`
- Include the trailing slash in the URL: `/mcp/`
- Add the `--allow-http` flag for HTTP connections
- Include the Accept header for proper SSE support

### Alternative: Direct Python Proxy (Advanced)

For advanced users or debugging purposes, you can create a custom Python proxy:

```json
{
  "mcpServers": {
    "simple-server-proxy": {
      "command": "python",
      "args": ["claude_mcp_proxy.py"],
      "cwd": "/path/to/mcp-simple-server"
    }
  }
}
```

**Note**: This requires the `claude_mcp_proxy.py` script from the repository and is mainly for debugging purposes. Use `mcp-remote` for production.

**Configuration File Locations:**

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

## Test with Claude

After integration, ask Claude:

- "Can you add 42 and 18 for me?"
- "What's 7 times 9?"
- "What tools do you have available?"

Claude will use your MCP server to perform calculations! 🎉

## Development

### Adding New Tools

```python
@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract two numbers"""
    return a - b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### Environment Variables

- `HOST`: Server host (default: 127.0.0.1, use 0.0.0.0 for deployment)
- `PORT`: Server port (default: 8000, Railway sets this automatically)

```bash
HOST=0.0.0.0 PORT=3000 python main.py
```

Note: For Railway deployment, FastMCP will automatically bind to `0.0.0.0:$PORT`.

## Project Structure

```
mcp-simple-server/
├── main.py                    # MCP server (~25 lines)
├── test_server.py             # Local server tests (~300 lines)
├── test_deployment.py         # Remote deployment tests
├── test_host_binding.py       # Host binding tests
├── test_proxy_script.py       # Proxy testing script
├── test_streamable_app.py     # Streamable HTTP tests
├── test_tool_verification.py  # Tool verification tests
├── debug_railway_server.py    # Railway debugging utilities
├── debug_fastmcp.py           # FastMCP debugging utilities
├── claude_mcp_proxy.py        # Claude Desktop proxy (optional)
├── start.sh                   # Shell startup script
├── pyproject.toml             # Project configuration
├── README.md                  # This documentation
├── uv.lock                    # Dependency lock file
├── .gitignore                 # Git ignore patterns
├── .python-version            # Python version specification
├── Dockerfile                 # Docker deployment
├── railway.toml               # Railway configuration
├── Procfile                   # Heroku configuration
└── render.yaml                # Render configuration
```

## Architecture

- **FastMCP**: High-level MCP implementation from Anthropic
- **Streamable HTTP**: Modern transport with SSE streaming support
- **Session Management**: Stateful connections with session IDs
- **JSON-RPC 2.0**: Standard protocol for message exchange
- **Protocol 2025-06-18**: Latest MCP specification
- **Port 8000**: Default FastMCP server port (configurable via PORT env var)

## Technical Details

### Server Implementation

- **Framework**: FastMCP (official Anthropic library)
- **Transport**: Streamable HTTP with Server-Sent Events
- **Protocol**: MCP 2025-06-18 specification
- **Dependencies**: `httpx>=0.28.1`, `mcp>=1.9.4`

### MCP Protocol Flow

1. Client sends `initialize` request
2. Server responds with capabilities and session ID
3. Client sends `initialized` notification
4. Normal operations begin (tools/list, tools/call, etc.)

### Tool Response Format

Tools return simple Python values (float, int, str) which FastMCP automatically wraps in the proper MCP response format.

## Troubleshooting

### Server Won't Start

```bash
# Check if port is in use
lsof -i :8000

# Try different port
PORT=3000 python main.py
```

### MCP Protocol Errors

```bash
# Run automated test
python test_server.py

# Check server logs for detailed errors
```

### Claude Desktop Not Connecting

1. **Verify JSON configuration syntax** - Use a JSON validator
2. **Check server URL accessibility** - Test with `curl` or browser
3. **Restart Claude Desktop** after config changes
4. **Ensure proper MCP endpoint path** - Use `/mcp/` with trailing slash
5. **Use `mcp-remote` for remote servers** - Don't use `curl` for remote connections

### Test Remote Deployment

Test your deployed server with the provided script:

```bash
# Test your deployed server (replace with your URL)
python test_deployment.py your-app.railway.app

# Or with full URL
python test_deployment.py https://your-app.railway.app
```

This will run the complete MCP protocol test suite against your remote server.

### Common Issues

- **Wrong endpoint**: Use `/mcp/` (with trailing slash)
- **Missing headers**: Include all required MCP headers
- **Session management**: Must send `initialized` notification after `initialize`
- **Remote connections**: Use `mcp-remote`, not `curl` for Claude Desktop
- **Port binding**: Use `0.0.0.0:$PORT` for deployment, not `127.0.0.1`

## Dependencies

```toml
dependencies = [
    "httpx>=0.28.1",   # HTTP client for testing
    "mcp>=1.9.4",      # Official Anthropic MCP library
]
```

The project uses:

- **mcp**: Official Anthropic MCP Python SDK
- **httpx**: Modern HTTP client for automated testing
- **Python**: Requires Python >=3.10

## Contributing

1. Fork the repository
2. Make your changes
3. Run tests: `python test_server.py`
4. Test deployment: `python test_deployment.py your-test-url`
5. Ensure all tests pass
6. Submit a pull request

## License

MIT License

## Resources

- [MCP Specification 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/)
- [FastMCP Documentation](https://mcp.so/docs)
- [Claude Desktop](https://claude.ai/download)
- [Railway Deployment](https://railway.app)
- [Render Deployment](https://render.com)
- [mcp-remote Package](https://www.npmjs.com/package/mcp-remote)