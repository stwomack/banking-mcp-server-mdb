# Banking MCP Server (MongoDB Backend)

A simple Model Context Protocol (MCP) server for basic banking operations (CRUD) using MongoDB as the backend. This project demonstrates how to build an MCP server for account management and money transfers. This readme really needs some lovin. Not everything is documented.

## Features
- Create, delete, and list accounts
- Deposit, withdraw, and transfer funds
- Persistent storage with MongoDB

## Prerequisites
- Python 3.8+
- MongoDB (local or cloud)
- [uv](https://github.com/astral-sh/uv) (recommended)

## Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd banking-mcp-server-mdb
   ```
2. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```
3. **Configure MongoDB**
   Create a `.env` file in the project root:
   ```env
   MONGO_URI=mongodb://localhost:27017
   MONGO_DB=money_transfer_db
   ```
   Start your MongoDB server if not already running.
4. **Start the MCP server** (Note: This doesn't do anything by itself. It's meant to be called via MCP Clients or toold like ClaudeDesktop)
   ```bash
   ./start_banking_mcp_server_mdb.sh
   ```
5. **If running the temporal version for durable MCP, start the temporal worker**
   ```
   python -m mcp_server.worker
   ```

## Claude Desktop Configuration
Add this to your `/Users/swomack/Library/Application Support/Claude/claude_desktop_config.json` file to use the server:
```json
"mcpServers": {
  "bank_accounts": {
    "command": "/absolute/path/to/banking-mcp-server-mdb/start_banking_mcp_server_mdb.sh",
    "args": []
  }
}
```
Replace the path with your actual project location.

## Available Tools
- `create_account(username, balance=0.0)`: Create a new account
- `delete_account(username)`: Delete an account
- `get_account(username)`: Get account info
- `list_accounts()`: List all accounts
- `deposit(username, amount)`: Deposit funds
- `withdraw(username, amount)`: Withdraw funds
- `transfer(from_user, to_user, amount)`: Transfer funds between accounts

## Example Usage
Ask Claude:
- Create an account: `Create a bank account for Alice with $100.`
- Transfer funds: `Transfer $50 from Alice to Bob.`
- List accounts: `Show all accounts.`

---
This project is for demonstration purposes only. 
