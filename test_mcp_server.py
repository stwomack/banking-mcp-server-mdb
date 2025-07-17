#!/usr/bin/env python3
"""Test script for the MCP server implementation."""

import asyncio
import json
from mcp_client.mcp_client import MCPToolsClient

async def test_mcp_server():
    """Test the MCP server functionality."""
    print("Testing MCP Money Transfer Server...")
    
    async with MCPToolsClient() as client:
        # Test health check
        print("\n1. Testing health check...")
        health = await client.health_check()
        print(f"Health check result: {health}")

        # Test account creation
        print("\n2. Testing account creation...")
        result = await client.create_account("alice", 1000.0)
        print(f"Create account result: {result}")
        
        result = await client.create_account("bob", 500.0)
        print(f"Create account result: {result}")
        
        # Test get account
        print("\n3. Testing get account...")
        account = await client.get_account("alice")
        print(f"Get account result: {account}")
        
        # Test list accounts
        print("\n4. Testing list accounts...")
        accounts = await client.list_accounts()
        print(f"List accounts result: {accounts}")
        
        # Test deposit
        print("\n5. Testing deposit...")
        result = await client.deposit("alice", 200.0)
        print(f"Deposit result: {result}")
        
        # Test withdraw
        print("\n6. Testing withdraw...")
        result = await client.withdraw("alice", 100.0)
        print(f"Withdraw result: {result}")
        
        # Test transfer
        print("\n7. Testing transfer...")
        result = await client.transfer("alice", "bob", 250.0)
        print(f"Transfer result: {result}")
        
        # Test get balance
        print("\n8. Testing get balance...")
        balance = await client.get_balance("alice")
        print(f"Get balance result: {balance}")
        
        balance = await client.get_balance("bob")
        print(f"Get balance result: {balance}")
        
        # Test error cases
        print("\n9. Testing error cases...")
        
        # Try to create duplicate account
        result = await client.create_account("alice", 100.0)
        print(f"Duplicate account creation: {result}")
        
        # Try to get non-existent account
        result = await client.get_account("charlie")
        print(f"Non-existent account: {result}")
        
        # Try to transfer with insufficient funds
        result = await client.transfer("alice", "bob", 10000.0)
        print(f"Insufficient funds transfer: {result}")
        
        # Clean up - delete accounts
        print("\n10. Cleaning up...")
        result = await client.delete_account("alice")
        print(f"Delete alice: {result}")

        result = await client.delete_account("bob")
        print(f"Delete bob: {result}")
        
        # Verify accounts are deleted
        accounts = await client.list_accounts()
        print(f"Final accounts list: {accounts}")
        
        print("\nMCP server test completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_mcp_server())