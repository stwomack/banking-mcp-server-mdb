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
import asyncio
import uuid
from datetime import datetime
from temporalio.client import Client
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

# Create an MCP server
mcp = FastMCP("Money Transfer Server (Temporal)")

# Global Temporal client
temporal_client = None
TASK_QUEUE = "banking-task-queue"

async def get_temporal_client():
    global temporal_client
    if temporal_client is None:
        temporal_client = await Client.connect("localhost:7233")
    return temporal_client

@mcp.tool()
async def create_account(username: str, balance: float = 0.0) -> dict:
    try:
        client = await get_temporal_client()
        workflow_id = f"create-account-{username}-{uuid.uuid4().hex[:8]}"
        
        result = await client.execute_workflow(
            CreateAccountWorkflow.run,
            args=[username, balance],
            id=workflow_id,
            task_queue=TASK_QUEUE
        )
        
        if result.success:
            return result.data
        else:
            return {"error": result.error}
    except Exception as e:
        return {"error": f"Workflow execution failed: {str(e)}"}

@mcp.tool()
async def delete_account(username: str) -> dict:
    try:
        client = await get_temporal_client()
        workflow_id = f"delete-account-{username}-{uuid.uuid4().hex[:8]}"
        
        result = await client.execute_workflow(
            DeleteAccountWorkflow.run,
            args=[username],
            id=workflow_id,
            task_queue=TASK_QUEUE
        )
        
        if result.success:
            return result.data
        else:
            return {"error": result.error}
    except Exception as e:
        return {"error": f"Workflow execution failed: {str(e)}"}

@mcp.tool()
async def get_account(username: str) -> dict:
    try:
        client = await get_temporal_client()
        workflow_id = f"get-account-{username}-{uuid.uuid4().hex[:8]}"
        
        result = await client.execute_workflow(
            GetAccountWorkflow.run,
            args=[username],
            id=workflow_id,
            task_queue=TASK_QUEUE
        )
        
        if result.success:
            return result.data
        else:
            return {"error": result.error}
    except Exception as e:
        return {"error": f"Workflow execution failed: {str(e)}"}

@mcp.tool()
async def list_accounts() -> list:
    try:
        client = await get_temporal_client()
        workflow_id = f"list-accounts-{uuid.uuid4().hex[:8]}"
        
        result = await client.execute_workflow(
            ListAccountsWorkflow.run,
            id=workflow_id,
            task_queue=TASK_QUEUE
        )
        
        if result.success:
            return result.data["accounts"]
        else:
            return []
    except Exception as e:
        return []

@mcp.tool()
async def deposit(username: str, amount: float) -> dict:
    try:
        client = await get_temporal_client()
        workflow_id = f"deposit-{username}-{uuid.uuid4().hex[:8]}"
        
        result = await client.execute_workflow(
            DepositWorkflow.run,
            args=[username, amount],
            id=workflow_id,
            task_queue=TASK_QUEUE
        )
        
        if result.success:
            return result.data
        else:
            return {"error": result.error}
    except Exception as e:
        return {"error": f"Workflow execution failed: {str(e)}"}

@mcp.tool()
async def withdraw(username: str, amount: float) -> dict:
    try:
        client = await get_temporal_client()
        workflow_id = f"withdraw-{username}-{uuid.uuid4().hex[:8]}"
        
        result = await client.execute_workflow(
            WithdrawWorkflow.run,
            args=[username, amount],
            id=workflow_id,
            task_queue=TASK_QUEUE
        )
        
        if result.success:
            return result.data
        else:
            return {"error": result.error}
    except Exception as e:
        return {"error": f"Workflow execution failed: {str(e)}"}

@mcp.tool()
async def transfer(from_user: str, to_user: str, amount: float) -> dict:
    try:
        client = await get_temporal_client()
        workflow_id = f"transfer-{from_user}-{to_user}-{uuid.uuid4().hex[:8]}"
        
        result = await client.execute_workflow(
            TransferWorkflow.run,
            args=[from_user, to_user, amount],
            id=workflow_id,
            task_queue=TASK_QUEUE
        )
        
        if result.success:
            return result.data
        else:
            return {"error": result.error}
    except Exception as e:
        return {"error": f"Workflow execution failed: {str(e)}"}

@mcp.tool()
async def health_check() -> dict:
    try:
        client = await get_temporal_client()
        workflow_id = f"health-check-{uuid.uuid4().hex[:8]}"
        
        result = await client.execute_workflow(
            HealthCheckWorkflow.run,
            id=workflow_id,
            task_queue=TASK_QUEUE
        )
        
        if result.success:
            return result.data
        else:
            return {"status": "unhealthy", "service": "MCP Money Transfer Server (Temporal)", "error": result.error}
    except Exception as e:
        return {"status": "unhealthy", "service": "MCP Money Transfer Server (Temporal)", "error": f"Workflow execution failed: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
