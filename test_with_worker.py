#!/usr/bin/env python3
"""Test script that runs worker and tests the system."""

import asyncio
import subprocess
import time
import signal
import os
from mcp_server.workflows import HealthCheckWorkflow
from mcp_server.activities import health_check_activity
from temporalio.client import Client

async def test_with_worker():
    """Test the system with a running worker."""
    print("Starting worker in background...")
    
    # Start worker as subprocess
    worker_process = subprocess.Popen(
        ["python", "-m", "mcp_server.worker"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Give worker time to start
    await asyncio.sleep(3)
    
    try:
        # Connect to Temporal server
        client = await Client.connect("localhost:7233")
        
        # Test health check workflow
        print("Testing health check workflow...")
        result = await client.execute_workflow(
            HealthCheckWorkflow.run,
            id="health-check-test-123",
            task_queue="banking-task-queue"
        )
        
        print(f"Health check result: {result}")
        
        # Test more workflows if health check passes
        if result.success:
            print("Health check passed! Testing other workflows...")
            
            # Test create account
            from mcp_server.workflows import CreateAccountWorkflow
            result = await client.execute_workflow(
                CreateAccountWorkflow.run,
                args=["testuser", 100.0],
                id="create-account-test-123",
                task_queue="banking-task-queue"
            )
            print(f"Create account result: {result}")
            
            # Test get account
            from mcp_server.workflows import GetAccountWorkflow
            result = await client.execute_workflow(
                GetAccountWorkflow.run,
                args=["testuser"],
                id="get-account-test-123",
                task_queue="banking-task-queue"
            )
            print(f"Get account result: {result}")
        
        print("All tests completed!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up worker process
        print("Stopping worker...")
        worker_process.terminate()
        try:
            worker_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            worker_process.kill()

if __name__ == "__main__":
    asyncio.run(test_with_worker())