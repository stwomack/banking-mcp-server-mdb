#!/usr/bin/env python3
"""Simple test for the Temporal-based MCP server."""

import asyncio
from mcp_server.workflows import HealthCheckWorkflow
from mcp_server.activities import health_check_activity
from temporalio.client import Client
from temporalio.worker import Worker

async def test_temporal_directly():
    """Test Temporal workflows directly."""
    print("Testing Temporal workflows directly...")
    
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    # Start worker
    worker = Worker(
        client,
        task_queue="banking-task-queue",
        workflows=[HealthCheckWorkflow],
        activities=[health_check_activity]
    )
    
    # Run workflow
    print("Starting health check workflow...")
    result = await client.execute_workflow(
        HealthCheckWorkflow.run,
        id="health-check-test",
        task_queue="banking-task-queue"
    )
    
    print(f"Result: {result}")
    return result

if __name__ == "__main__":
    asyncio.run(test_temporal_directly())