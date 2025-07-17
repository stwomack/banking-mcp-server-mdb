from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from dataclasses import dataclass
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

retry_policy = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    maximum_interval=timedelta(seconds=60),
    maximum_attempts=3,
)

@dataclass
class AccountOperationResult:
    success: bool
    data: Dict[str, Any]
    error: str = ""

@workflow.defn
class CreateAccountWorkflow:
    @workflow.run
    async def run(self, username: str, balance: float = 0.0) -> AccountOperationResult:
        result = await workflow.execute_activity(
            "create_account_activity",
            args=[username, balance],
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy
        )
        return AccountOperationResult(
            success=result.get("success", False),
            data=result,
            error=result.get("error", "")
        )

@workflow.defn
class DeleteAccountWorkflow:
    @workflow.run
    async def run(self, username: str) -> AccountOperationResult:
        result = await workflow.execute_activity(
            "delete_account_activity",
            args=[username],
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy
        )
        return AccountOperationResult(
            success=result.get("success", False),
            data=result,
            error=result.get("error", "")
        )

@workflow.defn
class GetAccountWorkflow:
    @workflow.run
    async def run(self, username: str) -> AccountOperationResult:
        result = await workflow.execute_activity(
            "get_account_activity",
            args=[username],
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy
        )
        return AccountOperationResult(
            success=result.get("success", False),
            data=result,
            error=result.get("error", "")
        )

@workflow.defn
class ListAccountsWorkflow:
    @workflow.run
    async def run(self) -> AccountOperationResult:
        result = await workflow.execute_activity(
            "list_accounts_activity",
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy
        )
        return AccountOperationResult(
            success=True,
            data={"accounts": result}
        )

@workflow.defn
class DepositWorkflow:
    @workflow.run
    async def run(self, username: str, amount: float) -> AccountOperationResult:
        result = await workflow.execute_activity(
            "deposit_activity",
            args=[username, amount],
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy
        )
        return AccountOperationResult(
            success=result.get("success", False),
            data=result,
            error=result.get("error", "")
        )

@workflow.defn
class WithdrawWorkflow:
    @workflow.run
    async def run(self, username: str, amount: float) -> AccountOperationResult:
        result = await workflow.execute_activity(
            "withdraw_activity",
            args=[username, amount],
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy
        )
        return AccountOperationResult(
            success=result.get("success", False),
            data=result,
            error=result.get("error", "")
        )

@workflow.defn
class TransferWorkflow:
    @workflow.run
    async def run(self, from_user: str, to_user: str, amount: float) -> AccountOperationResult:
        result = await workflow.execute_activity(
            "transfer_activity",
            args=[from_user, to_user, amount],
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy
        )
        return AccountOperationResult(
            success=result.get("success", False),
            data=result,
            error=result.get("error", "")
        )

@workflow.defn
class HealthCheckWorkflow:
    @workflow.run
    async def run(self) -> AccountOperationResult:
        result = await workflow.execute_activity(
            "health_check_activity",
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy
        )
        return AccountOperationResult(
            success=True,
            data=result
        )