import asyncio
import json
import subprocess
from typing import Dict, Any, Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    """MCP client for connecting to the money transfer server."""

    def __init__(self, server_command: list = None):
        if server_command is None:
            server_command = ["uv", "run", "-m", "mcp_server.main"]
        self.server_command = server_command
        self.session: Optional[ClientSession] = None
        self.exit_stack: Optional[AsyncExitStack] = None

    async def connect(self):
        """Connect to the MCP server."""
        self.exit_stack = AsyncExitStack()

        # Start server as subprocess
        server_params = StdioServerParameters(
            command=self.server_command[0],
            args=self.server_command[1:],
            env=None
        )

        # Create stdio client
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )

        # Create session
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(stdio_transport[0], stdio_transport[1])
        )

        # Initialize the session
        await self.session.initialize()

    async def disconnect(self):
        """Disconnect from the MCP server."""
        if self.exit_stack:
            await self.exit_stack.aclose()

    async def list_tools(self) -> Dict[str, Any]:
        """List available tools from the MCP server."""
        if not self.session:
            raise RuntimeError("Not connected to MCP server")

        result = await self.session.list_tools()
        return result.tools

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the MCP server."""
        if not self.session:
            raise RuntimeError("Not connected to MCP server")

        result = await self.session.call_tool(tool_name, arguments)
        if result.content:
            content = result.content[0].text
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"result": content}
        return {}


# MCP-based tool implementations
class MCPToolsClient:
    """Tool implementations using MCP client."""

    def __init__(self):
        self.client = MCPClient()

    async def __aenter__(self):
        await self.client.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.disconnect()

    async def create_account(self, username: str, balance: float = 0.0) -> Dict[str, Any]:
        """Create a new account with the given username and initial balance."""
        try:
            result = await self.client.call_tool("create_account", {
                "username": username,
                "balance": balance
            })
            return result
        except Exception as e:
            return {"error": f"Failed to create account: {str(e)}"}

    async def get_account(self, username: str) -> Dict[str, Any]:
        """Get account information for the given username."""
        try:
            result = await self.client.call_tool("get_account", {
                "username": username
            })
            return result
        except Exception as e:
            return {"error": f"Failed to get account: {str(e)}"}

    async def list_accounts(self) -> Dict[str, Any]:
        """List all accounts in the system."""
        try:
            result = await self.client.call_tool("list_accounts", {})
            return result
        except Exception as e:
            return {"error": f"Failed to list accounts: {str(e)}"}

    async def delete_account(self, username: str) -> Dict[str, Any]:
        """Delete the account with the given username."""
        try:
            result = await self.client.call_tool("delete_account", {
                "username": username
            })
            return result
        except Exception as e:
            return {"error": f"Failed to delete account: {str(e)}"}

    async def deposit(self, username: str, amount: float) -> Dict[str, Any]:
        """Deposit money into the specified account."""
        try:
            result = await self.client.call_tool("deposit", {
                "username": username,
                "amount": amount
            })
            return result
        except Exception as e:
            return {"error": f"Failed to deposit: {str(e)}"}

    async def withdraw(self, username: str, amount: float) -> Dict[str, Any]:
        """Withdraw money from the specified account."""
        try:
            result = await self.client.call_tool("withdraw", {
                "username": username,
                "amount": amount
            })
            return result
        except Exception as e:
            return {"error": f"Failed to withdraw: {str(e)}"}

    async def transfer(self, from_user: str, to_user: str, amount: float) -> Dict[str, Any]:
        """Transfer money from one account to another."""
        try:
            result = await self.client.call_tool("transfer", {
                "from_user": from_user,
                "to_user": to_user,
                "amount": amount
            })
            return result
        except Exception as e:
            return {"error": f"Failed to transfer: {str(e)}"}

    async def get_balance(self, username: str) -> Dict[str, Any]:
        """Get the current balance for the specified account."""
        try:
            result = await self.client.call_tool("get_account", {
                "username": username
            })
            if "error" in result:
                return result
            return {"username": username, "balance": result.get("balance")}
        except Exception as e:
            return {"error": f"Failed to get balance: {str(e)}"}

    async def health_check(self) -> Dict[str, Any]:
        """Check the health of the MCP server."""
        try:
            result = await self.client.call_tool("health_check", {})
            return result
        except Exception as e:
            return {"error": f"Health check failed: {str(e)}"}


# Synchronous wrapper functions for backward compatibility
def run_async_tool(coro):
    """Run an async tool function synchronously."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

async def with_mcp_client(func, *args, **kwargs):
    """Helper to run a function with MCP client context."""
    async with MCPToolsClient() as client:
        return await func(client, *args, **kwargs)

# Synchronous tool functions that use MCP
def create_account_sync(username: str, balance: float = 0.0) -> Dict[str, Any]:
    """Create a new account with the given username and initial balance."""
    return run_async_tool(
        with_mcp_client(lambda client, u, b: client.create_account(u, b), username, balance)
    )

def get_account_sync(username: str) -> Dict[str, Any]:
    """Get account information for the given username."""
    return run_async_tool(
        with_mcp_client(lambda client, u: client.get_account(u), username)
    )

def list_accounts_sync() -> Dict[str, Any]:
    """List all accounts in the system."""
    return run_async_tool(
        with_mcp_client(lambda client: client.list_accounts())
    )

def delete_account_sync(username: str) -> Dict[str, Any]:
    """Delete the account with the given username."""
    return run_async_tool(
        with_mcp_client(lambda client, u: client.delete_account(u), username)
    )

def deposit_sync(username: str, amount: float) -> Dict[str, Any]:
    """Deposit money into the specified account."""
    return run_async_tool(
        with_mcp_client(lambda client, u, a: client.deposit(u, a), username, amount)
    )

def withdraw_sync(username: str, amount: float) -> Dict[str, Any]:
    """Withdraw money from the specified account."""
    return run_async_tool(
        with_mcp_client(lambda client, u, a: client.withdraw(u, a), username, amount)
    )

def transfer_sync(from_user: str, to_user: str, amount: float) -> Dict[str, Any]:
    """Transfer money from one account to another."""
    return run_async_tool(
        with_mcp_client(lambda client, f, t, a: client.transfer(f, t, a), from_user, to_user, amount)
    )

def get_balance_sync(username: str) -> Dict[str, Any]:
    """Get the current balance for the specified account."""
    return run_async_tool(
        with_mcp_client(lambda client, u: client.get_balance(u), username)
    )

def health_check_sync() -> Dict[str, Any]:
    """Check the health of the MCP server."""
    return run_async_tool(
        with_mcp_client(lambda client: client.health_check())
    )