import asyncio
import logging
from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker
from .workflows import (
    CreateAccountWorkflow,
    DeleteAccountWorkflow,
    GetAccountWorkflow,
    ListAccountsWorkflow,
    DepositWorkflow,
    WithdrawWorkflow,
    TransferWorkflow,
    HealthCheckWorkflow
)
from .activities import (
    create_account_activity,
    delete_account_activity,
    get_account_activity,
    list_accounts_activity,
    deposit_activity,
    withdraw_activity,
    transfer_activity,
    health_check_activity
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TASK_QUEUE = "banking-task-queue"

async def main():
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    # Create worker
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[
            CreateAccountWorkflow,
            DeleteAccountWorkflow,
            GetAccountWorkflow,
            ListAccountsWorkflow,
            DepositWorkflow,
            WithdrawWorkflow,
            TransferWorkflow,
            HealthCheckWorkflow
        ],
        activities=[
            create_account_activity,
            delete_account_activity,
            get_account_activity,
            list_accounts_activity,
            deposit_activity,
            withdraw_activity,
            transfer_activity,
            health_check_activity
        ]
    )
    
    logger.info("Banking MCP Temporal Worker starting...")
    logger.info(f"Task queue: {TASK_QUEUE}")
    
    # Start worker
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())