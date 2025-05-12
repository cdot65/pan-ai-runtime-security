#!/usr/bin/env python3
"""
Asynchronous Scan Example for AI Security SDK
This script demonstrates how to use the asynchronous scan functionality
to submit multiple content items for scanning and retrieve results.
"""
import os
import sys
from pathlib import Path
from pprint import pprint

import aisecurity
from aisecurity.generated_openapi_client.models.ai_profile import AiProfile
from aisecurity.generated_openapi_client.models.async_scan_object import AsyncScanObject
from aisecurity.generated_openapi_client.models.scan_request import ScanRequest
from aisecurity.generated_openapi_client.models.scan_request_contents_inner import (
    ScanRequestContentsInner,
)
from aisecurity.scan.models.content import Content
from aisecurity.scan.sync.scanner import Scanner
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


def main():
    """Main execution function"""
    # Load environment variables
    env = load_environment()

    # Initialize SDK with API key and endpoint
    aisecurity.init(api_key=env["api_key"], api_endpoint=env["api_endpoint"])

    print("Creating scanner...")
    scanner = Scanner()

    # Create AI profile with environment variables
    ai_profile = AiProfile(profile_name=env["profile_name"])

    # Create sample content objects
    content1 = Content(
        prompt="This is a test prompt with 72zf6.rxqfd.com/i8xps1 url",
        response="This is a test response",
    )

    content2 = Content(
        prompt="This is another test prompt", response="This is another test response"
    )

    # Prepare async scan objects for batch processing
    async_scan_objects = [
        AsyncScanObject(
            req_id=1,  # Request identifier for the first content
            scan_req=ScanRequest(
                tr_id="tx-001",  # Transaction ID
                ai_profile=ai_profile,
                contents=[
                    ScanRequestContentsInner(
                        prompt=content1.prompt, response=content1.response
                    )
                ],
            ),
        ),
        AsyncScanObject(
            req_id=2,  # Request identifier for the second content
            scan_req=ScanRequest(
                tr_id="tx-002",  # Transaction ID
                ai_profile=ai_profile,
                contents=[
                    ScanRequestContentsInner(
                        prompt=content2.prompt, response=content2.response
                    )
                ],
            ),
        ),
    ]

    print("==============================================================")
    print("Submitting asynchronous scan request...")
    scan_async_response = scanner.async_scan(async_scan_objects)
    print("==============================================================")

    # Print async scan submission response
    pprint(f"Async scan response: {scan_async_response}")
    print(f"Scan ID: {scan_async_response.scan_id}")
    print(f"Report ID: {scan_async_response.report_id}")
    print("==============================================================")

    # Query scan results by scan ID
    print("Querying results by scan ID...")
    scan_by_ids_response = scanner.query_by_scan_ids(
        scan_ids=[scan_async_response.scan_id]
    )
    print("==============================================================")
    pprint(f"Scan by IDs response: {scan_by_ids_response}")
    print("==============================================================")

    # Query scan results by report ID
    print("Querying results by report ID...")
    report_by_ids_response = scanner.query_by_report_ids(
        report_ids=[scan_async_response.report_id]
    )
    print("==============================================================")
    pprint(f"Report by IDs response: {report_by_ids_response}")
    print("==============================================================")


if __name__ == "__main__":
    main()
