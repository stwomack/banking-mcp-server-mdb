from pydantic import BaseModel, Field
from typing import Optional


class Account(BaseModel):
    username: str = Field(..., description="Unique username for the account")
    balance: float = Field(..., description="Account balance")


class AccountCreate(BaseModel):
    username: str = Field(..., description="Unique username for the account")
    balance: float = Field(default=0.0, description="Initial account balance")


class DepositRequest(BaseModel):
    username: str = Field(..., description="Username of the account to deposit to")
    amount: float = Field(..., gt=0, description="Amount to deposit (must be positive)")


class WithdrawRequest(BaseModel):
    username: str = Field(..., description="Username of the account to withdraw from")
    amount: float = Field(..., gt=0, description="Amount to withdraw (must be positive)")


class TransferRequest(BaseModel):
    from_user: str = Field(..., description="Username of the sender")
    to_user: str = Field(..., description="Username of the receiver")
    amount: float = Field(..., gt=0, description="Amount to transfer (must be positive)")


class AccountResponse(BaseModel):
    username: str
    balance: float
    message: Optional[str] = None


class TransactionResponse(BaseModel):
    success: bool
    message: str
    from_balance: Optional[float] = None
    to_balance: Optional[float] = None