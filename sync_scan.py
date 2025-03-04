#!/usr/bin/env python3
"""
Synchronous Scan Example for AI Security SDK
This script demonstrates how to use the synchronous scan functionality
to evaluate content against security policies.
"""
import os
import sys
from pathlib import Path
from pprint import pprint

import aisecurity
from aisecurity.generated_openapi_client import Metadata
from aisecurity.generated_openapi_client.models.ai_profile import AiProfile
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

    # Create content object with test data
    content = Content(
        prompt="This is a test prompt with 72zf6.rxqfd.com/i8xps1 url",
        response="This is a test response",
    )

    # Optional parameters for the scan API
    tr_id = "1234"  # Transaction ID for correlation
    metadata = Metadata(
        app_name="ai_security_example", app_user="user", ai_model="sample_model"
    )

    print("==============================================================")
    print("Invoking synchronous scan...")
    scan_response = scanner.sync_scan(
        ai_profile=ai_profile, content=content, tr_id=tr_id, metadata=metadata
    )
    print("==============================================================")

    # Print scan response details
    pprint(f"Synchronous scan response: {scan_response}")
    print("==============================================================")

    # More detailed information about the scan response
    print(f"Scan ID: {scan_response.scan_id}")
    print(f"Report ID: {scan_response.report_id}")
    print(f"Transaction ID: {scan_response.tr_id}")
    print(f"Category: {scan_response.category}")
    print(f"Action: {scan_response.action}")
    print(
        f"Prompt Detection: URL: {scan_response.prompt_detected.url_cats}, "
        f"DLP: {scan_response.prompt_detected.dlp}, "
        f"Injection: {scan_response.prompt_detected.injection}"
    )
    print(
        f"Response Detection: URL: {scan_response.response_detected.url_cats}, "
        f"DLP: {scan_response.response_detected.dlp}"
    )


if __name__ == "__main__":
    main()
