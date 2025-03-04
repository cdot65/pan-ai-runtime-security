#!/usr/bin/env python3
"""
Asyncio Concurrent SDK Usage Example for AI Security
This script demonstrates how to use asyncio for concurrent operations
with the AI Security SDK for improved performance.
"""
import asyncio
import os
import sys
from pathlib import Path
from pprint import pprint

import aisecurity
from aisecurity.generated_openapi_client import AiProfile, Metadata
from aisecurity.generated_openapi_client import AsyncScanObject
from aisecurity.generated_openapi_client import ScanRequest
from aisecurity.generated_openapi_client import ScanRequestContentsInner
from aisecurity.scan.models.content import Content
from aisecurity.scan.asyncio.scanner import Scanner  # Note the asyncio.scanner import
from dotenv import load_dotenv


def load_environment():
    """Load environment variables from .env file"""
    # First try to load from current directory
    env_path = Path(".") / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        # If not found, try the script's directory
        script_dir = Path(__file__).parent.absolute()
        env_path = script_dir / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
        else:
            print("No .env file found in current directory or script directory")
            sys.exit(1)

    # Get credentials from environment variables with fallbacks
    api_key = os.environ.get("PANW_AI_SEC_API_KEY", None)
    api_endpoint = os.environ.get("PANW_AI_SEC_API_ENDPOINT", None)
    profile_name = os.environ.get("PANW_AI_PROFILE_NAME", None)

    # Validate required credentials
    if not api_key:
        print("Missing required PANW_AI_SEC_API_KEY environment variable")
        sys.exit(1)

    return {
        "api_key": api_key,
        "api_endpoint": api_endpoint,
        "profile_name": profile_name,
    }


async def run_concurrent_scans(env):
    """
    Run multiple scan operations concurrently

    Args:
        env (dict): Environment configuration including API credentials
    """
    # Initialize SDK
    aisecurity.init(api_key=env["api_key"], api_endpoint=env["api_endpoint"])

    # Create scanner instance for asyncio operations
    ai_security_scanner = Scanner()

    # Create AI profile with environment variables
    ai_profile = AiProfile(profile_name=env["profile_name"])

    # Create content object
    content1 = Content(
        prompt="This is a test prompt with 72zf6.rxqfd.com/i8xps1 url",
        response="This is a test response",
    )

    # Optional metadata
    tr_id = "1234"
    metadata = Metadata(
        app_name="concurrent_sdk", app_user="user", ai_model="sample_model"
    )

    # Prepare async scan objects
    async_scan_objects = [
        AsyncScanObject(
            req_id=1,
            scan_req=ScanRequest(
                tr_id="tx-001",
                ai_profile=ai_profile,
                contents=[
                    ScanRequestContentsInner(
                        prompt=content1.prompt, response=content1.response
                    )
                ],
            ),
        ),
        AsyncScanObject(
            req_id=2,
            scan_req=ScanRequest(
                tr_id="tx-002",
                ai_profile=ai_profile,
                contents=[
                    ScanRequestContentsInner(
                        prompt="Another test prompt", response="Another test response"
                    )
                ],
            ),
        ),
    ]

    # Run sync_scan and async_scan concurrently
    print("Executing concurrent operations...")
    sync_scan_task = ai_security_scanner.sync_scan(
        ai_profile=ai_profile, content=content1, tr_id=tr_id, metadata=metadata
    )
    async_scan_task = ai_security_scanner.async_scan(async_scan_objects)

    # Wait for both tasks to complete
    sync_result, async_result = await asyncio.gather(sync_scan_task, async_scan_task)

    # Process and print results
    print("==============================================================")
    print("Sync scan response:")
    pprint(sync_result)
    print("==============================================================")
    print("Async scan response:")
    pprint(async_result)
    print("==============================================================")

    # Query for additional results if available
    if async_result and async_result.scan_id and async_result.report_id:
        # Query by scan IDs
        scan_by_ids_response, query_by_scan_ids_latency = (
            await ai_security_scanner.query_by_scan_ids(scan_ids=[async_result.scan_id])
        )
        print(f"Scan by IDs response [latency {query_by_scan_ids_latency} ms]:")
        pprint(scan_by_ids_response)
        print("==============================================================")

        # Query by report IDs
        report_by_ids_response, query_by_report_ids_latency = (
            await ai_security_scanner.query_by_report_ids(
                report_ids=[async_result.report_id]
            )
        )
        print(f"Report by IDs response [latency {query_by_report_ids_latency} ms]:")
        pprint(report_by_ids_response)
        print("==============================================================")

    # Clean up resources
    await ai_security_scanner.close()


def main():
    """Main execution function"""
    # Load environment variables
    env = load_environment()

    try:
        # Run the async function in the asyncio event loop
        asyncio.run(run_concurrent_scans(env))
        print("AI Security concurrent scanning example completed successfully")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
