from mcp.server.fastmcp import FastMCP
from pymongo.errors import DuplicateKeyError
from .database import db
from .models import (
    AccountCreate, 
    AccountResponse, 
    DepositRequest, 
    WithdrawRequest, 
    TransferRequest,
    TransactionResponse
)

# Create an MCP server
mcp = FastMCP("Money Transfer Server")

@mcp.tool()
def create_account(username: str, balance: float = 0.0) -> dict:
    try:
        success = db.create_account(username, balance)
        if success:
            return {
                "username": username,
                "balance": balance,
                "message": "Account created successfully"
            }
        else:
            return {"error": "Failed to create account"}
    except DuplicateKeyError:
        return {"error": "Username already exists"}

@mcp.tool()
def delete_account(username: str) -> dict:
    success = db.delete_account(username)
    if success:
        return {
            "username": username,
            "message": "Account deleted successfully"
        }
    else:
        return {"error": "Account not found"}

@mcp.tool()
def get_account(username: str) -> dict:
    account = db.get_account(username)
    if account:
        return {
            "username": account["username"],
            "balance": account["balance"]
        }
    else:
        return {"error": "Account not found"}

@mcp.tool()
def list_accounts() -> list:
    accounts = db.list_accounts()
    return [{"username": acc["username"], "balance": acc["balance"]} for acc in accounts]

@mcp.tool()
def deposit(username: str, amount: float) -> dict:
    if amount <= 0:
        return {"error": "Amount must be positive"}
    account = db.get_account(username)
    if not account:
        return {"error": "Account not found"}
    new_balance = account["balance"] + amount
    success = db.update_balance(username, new_balance)
    if success:
        return {
            "success": True,
            "message": f"Deposited ${amount} to {username}",
            "from_balance": new_balance
        }
    else:
        return {"error": "Failed to deposit funds"}

@mcp.tool()
def withdraw(username: str, amount: float) -> dict:
    if amount <= 0:
        return {"error": "Amount must be positive"}
    account = db.get_account(username)
    if not account:
        return {"error": "Account not found"}
    if account["balance"] < amount:
        return {"error": "Insufficient funds"}
    new_balance = account["balance"] - amount
    success = db.update_balance(username, new_balance)
    if success:
        return {
            "success": True,
            "message": f"Withdrew ${amount} from {username}",
            "from_balance": new_balance
        }
    else:
        return {"error": "Failed to withdraw funds"}

@mcp.tool()
def transfer(from_user: str, to_user: str, amount: float) -> dict:
    if amount <= 0:
        return {"error": "Amount must be positive"}
    if from_user == to_user:
        return {"error": "Cannot transfer to the same account"}
    success, message = db.transfer_funds(from_user, to_user, amount)
    if success:
        from_account = db.get_account(from_user)
        to_account = db.get_account(to_user)
        return {
            "success": True,
            "message": message,
            "from_balance": from_account["balance"],
            "to_balance": to_account["balance"]
        }
    else:
        return {"error": message}

@mcp.tool()
def health_check() -> dict:
    return {"status": "healthy", "service": "MCP Money Transfer Server"}

if __name__ == "__main__":
    mcp.run()
