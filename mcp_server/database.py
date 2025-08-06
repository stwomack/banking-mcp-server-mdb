import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.mongo_db = os.getenv("MONGO_DB", "banking-mcp-demo")
        self.client = MongoClient(
            self.mongo_uri,
            serverSelectionTimeoutMS=5000,  # 5 seconds
            connectTimeoutMS=5000,          # 5 seconds
        )
        self.db = self.client[self.mongo_db]
        self.accounts = self.db.accounts
        
        # Create unique index on username
        self.accounts.create_index("username", unique=True)
    
    def get_account(self, username: str):
        return self.accounts.find_one({"username": username})
    
    def create_account(self, username: str, balance: float):
        account = {"username": username, "balance": balance}
        result = self.accounts.insert_one(account)
        return result.acknowledged
    
    def delete_account(self, username: str):
        result = self.accounts.delete_one({"username": username})
        return result.deleted_count > 0
    
    def list_accounts(self):
        return list(self.accounts.find({}, {"_id": 0}))
    
    def update_balance(self, username: str, new_balance: float):
        result = self.accounts.update_one(
            {"username": username}, 
            {"$set": {"balance": new_balance}}
        )
        return result.modified_count > 0
    
    def transfer_funds(self, from_user: str, to_user: str, amount: float):
        from_account = self.accounts.find_one({"username": from_user})
        to_account = self.accounts.find_one({"username": to_user})

        if not from_account:
            return False, f"Account {from_user} not found"
        if not to_account:
            return False, f"Account {to_user} not found"
        if from_account["balance"] < amount:
            return False, "Insufficient funds"

        new_from_balance = from_account["balance"] - amount
        new_to_balance = to_account["balance"] + amount

        self.accounts.update_one(
            {"username": from_user},
            {"$set": {"balance": new_from_balance}}
        )
        self.accounts.update_one(
            {"username": to_user},
            {"$set": {"balance": new_to_balance}}
        )
        return True, "Transfer successful"


# Global database instance - lazy loaded
_db_instance = None

def get_db():
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance

# For backward compatibility
db = get_db()