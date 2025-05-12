#!/usr/bin/env python3
"""
Synchronous Scan Example for AI Security SDK
This script demonstrates how to use the synchronous scan functionality
to evaluate content against security policies.
"""

# Standard library imports
import logging

# Import SDK modules
import aisecurity
from aisecurity.generated_openapi_client import Metadata
from aisecurity.generated_openapi_client.models.ai_profile import AiProfile

# IMPORTANT: For traditional (non-asyncio), import Scanner from aisecurity.scan.inline.scanner
from aisecurity.scan.inline.scanner import Scanner
from aisecurity.scan.models.content import Content

# Import local utilities
from utils import load_environment, print_detailed_scan_result


def main():
    """Main execution function"""
    print("=== SYNCHRONOUS SCAN AI SECURITY SDK EXAMPLE ===\n")

    # Load environment variables
    env = load_environment()

    # Configure logging based on an environment variable
    logging.basicConfig(level=getattr(logging, env["log_level"]))

    print("1. Initializing SDK...")
    # Initialize the SDK with the API key and endpoint
    aisecurity.init(api_key=env["api_key"], api_endpoint=env["api_endpoint"])
    print(f"   SDK initialized with endpoint: {env['api_endpoint']}")

    print("\n2. Creating scanner...")
    # Create the scanner instance
    scanner = Scanner()
    print("   Scanner created successfully")

    print("\n3. Setting up AI profile...")
    # Create an AI profile with environment variables
    if env["profile_id"]:
        ai_profile = AiProfile(profile_id=env["profile_id"])
        print(f"   Using profile ID: {env['profile_id']}")
    else:
        ai_profile = AiProfile(profile_name=env["profile_name"])
        print(f"   Using profile name: {env['profile_name']}")

    print("\n4. Creating content for scanning...")
    # Create a content object with test data containing a malicious URL
    content = Content(
        prompt="This is a test prompt with 72zf6.rxqfd.com/i8xps1 URL that should be detected",
        response="This is a test response without any malicious content",
    )
    print("   Content created with test data (including malicious URL)")

    print("\n5. Setting up optional metadata...")
    # Optional parameters for the scan API
    tr_id = "sync-scan-example-001"  # Transaction ID for correlation
    metadata = Metadata(
        app_name="ai_security_sync_example",
        app_user="example_user",
        ai_model="example_model"
    )
    print("   Metadata configured")

    print("\n6. Performing synchronous scan...")
    print("=" * 60)
    # Perform the synchronous scan with all parameters
    scan_response = scanner.sync_scan(
        ai_profile=ai_profile,
        content=content,
        tr_id=tr_id,
        metadata=metadata
    )
    print("=" * 60)

    print("\n7. Detailed scan results:")
    # Print detailed scan results
    print_detailed_scan_result(scan_response)

    print("\n=== EXAMPLE COMPLETED ===")


if __name__ == "__main__":
    main()
