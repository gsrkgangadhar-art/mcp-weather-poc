from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
import os

railway_host = os.getenv("RAILWAY_PUBLIC_DOMAIN", "mcp-weather-poc-production.up.railway.app")

mcp = FastMCP(
    "Simple Server",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[
            "localhost:*",
            "127.0.0.1:*",
            f"{railway_host}:*",
            railway_host,
            "healthcheck.railway.app:*",
            "healthcheck.railway.app"
        ],
        allowed_origins=[
            "http://localhost:*",
            "https://localhost:*",
            f"https://{railway_host}",
            "https://healthcheck.railway.app"
        ]
    )
)

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    print("Starting MCP server")
    print("RAILWAY_PUBLIC_DOMAIN =", railway_host)
    mcp.run(transport="streamable-http", host=host, port=port)
