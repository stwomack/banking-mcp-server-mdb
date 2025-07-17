from temporalio import activity
from pymongo.errors import DuplicateKeyError
from .database import get_db
from typing import Dict, Any, List


@activity.defn
async def create_account_activity(username: str, balance: float = 0.0) -> Dict[str, Any]:
    try:
        db = get_db()
        success = db.create_account(username, balance)
        if success:
            return {
                "success": True,
                "username": username,
                "balance": balance,
                "message": "Account created successfully"
            }
        else:
            return {
                "success": False,
                "error": "Failed to create account"
            }
    except DuplicateKeyError:
        return {
            "success": False,
            "error": "Username already exists"
        }
    except Exception as e:
        activity.logger.error(f"Error creating account: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}"
        }


@activity.defn
async def delete_account_activity(username: str) -> Dict[str, Any]:
    try:
        db = get_db()
        success = db.delete_account(username)
        if success:
            return {
                "success": True,
                "username": username,
                "message": "Account deleted successfully"
            }
        else:
            return {
                "success": False,
                "error": "Account not found"
            }
    except Exception as e:
        activity.logger.error(f"Error deleting account: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}"
        }


@activity.defn
async def get_account_activity(username: str) -> Dict[str, Any]:
    try:
        db = get_db()
        account = db.get_account(username)
        if account:
            return {
                "success": True,
                "username": account["username"],
                "balance": account["balance"]
            }
        else:
            return {
                "success": False,
                "error": "Account not found"
            }
    except Exception as e:
        activity.logger.error(f"Error getting account: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}"
        }


@activity.defn
async def list_accounts_activity() -> List[Dict[str, Any]]:
    try:
        db = get_db()
        accounts = db.list_accounts()
        return [{"username": acc["username"], "balance": acc["balance"]} for acc in accounts]
    except Exception as e:
        activity.logger.error(f"Error listing accounts: {str(e)}")
        return []


@activity.defn
async def deposit_activity(username: str, amount: float) -> Dict[str, Any]:
    try:
        if amount <= 0:
            return {
                "success": False,
                "error": "Amount must be positive"
            }
        
        db = get_db()
        account = db.get_account(username)
        if not account:
            return {
                "success": False,
                "error": "Account not found"
            }
        
        new_balance = account["balance"] + amount
        success = db.update_balance(username, new_balance)
        if success:
            return {
                "success": True,
                "message": f"Deposited ${amount} to {username}",
                "from_balance": new_balance
            }
        else:
            return {
                "success": False,
                "error": "Failed to deposit funds"
            }
    except Exception as e:
        activity.logger.error(f"Error depositing funds: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}"
        }


@activity.defn
async def withdraw_activity(username: str, amount: float) -> Dict[str, Any]:
    try:
        if amount <= 0:
            return {
                "success": False,
                "error": "Amount must be positive"
            }
        
        db = get_db()
        account = db.get_account(username)
        if not account:
            return {
                "success": False,
                "error": "Account not found"
            }
        
        if account["balance"] < amount:
            return {
                "success": False,
                "error": "Insufficient funds"
            }
        
        new_balance = account["balance"] - amount
        success = db.update_balance(username, new_balance)
        if success:
            return {
                "success": True,
                "message": f"Withdrew ${amount} from {username}",
                "from_balance": new_balance
            }
        else:
            return {
                "success": False,
                "error": "Failed to withdraw funds"
            }
    except Exception as e:
        activity.logger.error(f"Error withdrawing funds: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}"
        }


@activity.defn
async def transfer_activity(from_user: str, to_user: str, amount: float) -> Dict[str, Any]:
    try:
        if amount <= 0:
            return {
                "success": False,
                "error": "Amount must be positive"
            }
        
        if from_user == to_user:
            return {
                "success": False,
                "error": "Cannot transfer to the same account"
            }
        
        db = get_db()
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
            return {
                "success": False,
                "error": message
            }
    except Exception as e:
        activity.logger.error(f"Error transferring funds: {str(e)}")
        return {
            "success": False,
            "error": f"Database error: {str(e)}"
        }


@activity.defn
async def health_check_activity() -> Dict[str, Any]:
    try:
        return {
            "status": "healthy",
            "service": "MCP Money Transfer Server (Temporal)"
        }
    except Exception as e:
        activity.logger.error(f"Error in health check: {str(e)}")
        return {
            "status": "unhealthy",
            "service": "MCP Money Transfer Server (Temporal)",
            "error": str(e)
        }