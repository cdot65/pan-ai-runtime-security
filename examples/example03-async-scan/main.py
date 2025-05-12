#!/usr/bin/env python3
"""
Asynchronous Scan Example for AI Security SDK
This script demonstrates how to use the asynchronous scan functionality
to submit multiple content items for scanning and retrieve results.
"""

# Standard library imports
import logging
import time

# Import SDK modules
import aisecurity
from aisecurity.generated_openapi_client.models.ai_profile import AiProfile
from aisecurity.generated_openapi_client.models.async_scan_object import AsyncScanObject
from aisecurity.generated_openapi_client.models.scan_request import ScanRequest
from aisecurity.generated_openapi_client.models.scan_request_contents_inner import (
    ScanRequestContentsInner,
)
from aisecurity.scan.inline.scanner import Scanner
from aisecurity.scan.models.content import Content

# Import local utilities
from utils import load_environment


def main():
    """Main execution function"""
    print("=== ASYNCHRONOUS SCAN AI SECURITY SDK EXAMPLE ===\n")

    # Load environment variables
    env = load_environment()

    # Configure logging based on environment variable
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

    print("\n4. Creating content for batch scanning...")
    # Create sample content objects
    content1 = Content(
        prompt="This is a test prompt with 72zf6.rxqfd.com/i8xps1 URL that should be detected",
        response="This is a test response for the first item",
    )

    content2 = Content(
        prompt="This is another test prompt without any malicious content",
        response="This is another test response for the second item"
    )
    print("   Created 2 content items for batch processing")

    print("\n5. Preparing async scan objects...")
    # Prepare async scan objects for batch processing
    async_scan_objects = [
        AsyncScanObject(
            req_id=1,  # Request identifier for the first content
            scan_req=ScanRequest(
                tr_id="async-tx-001",  # Transaction ID
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
                tr_id="async-tx-002",  # Transaction ID
                ai_profile=ai_profile,
                contents=[
                    ScanRequestContentsInner(
                        prompt=content2.prompt, response=content2.response
                    )
                ],
            ),
        ),
    ]
    print("   Prepared 2 async scan objects with unique request IDs")

    print("\n6. Submitting asynchronous scan request...")
    print("=" * 60)
    # Submit the asynchronous scan request
    scan_async_response = scanner.async_scan(async_scan_objects)
    print("=" * 60)

    # Print async scan submission response
    print("\n7. Async scan submission results:")
    print(f"   Scan ID: {scan_async_response.scan_id}")
    print(f"   Report ID: {scan_async_response.report_id}")
    print("   ✅ Async scan request submitted successfully")

    # Wait a moment for scan to start processing
    time.sleep(2)

    print("\n8. Querying results by scan ID...")
    print("=" * 60)

    # Initialize retry variables
    max_retries = 3
    retry_count = 0
    retry_wait = 10  # seconds
    scan_completed = False
    scan_by_ids_response = None

    while retry_count < max_retries and not scan_completed:
        if retry_count > 0:
            print(f"\n   Waiting {retry_wait} seconds before retry {retry_count}/{max_retries-1}...")
            time.sleep(retry_wait)
            print("   Retrying query for scan status...")

        # Query scan results by scan ID
        scan_by_ids_response = scanner.query_by_scan_ids(
            scan_ids=[scan_async_response.scan_id]
        )
        print("=" * 60 if retry_count == 0 else "")

        # Check if the response list has any items with 'status' = 'complete'
        if scan_by_ids_response:
            for scan in scan_by_ids_response:
                # Check for status field, which is the correct field for completion
                if hasattr(scan, 'status') and scan.status == 'complete':
                    scan_completed = True
                    break

        retry_count += 1

        # If scan is completed or we've reached max retries, break out
        if scan_completed or retry_count >= max_retries:
            break

    # Print scan query response details
    print("\n   Scan Status Details:")
    if not scan_by_ids_response:
        print("   No scan data available")
    else:
        # Use a set to keep track of already printed scan IDs to avoid duplicates
        printed_scan_ids = set()
        for scan in scan_by_ids_response:
            scan_id = scan.scan_id if hasattr(scan, 'scan_id') else 'N/A'
            if scan_id not in printed_scan_ids:
                printed_scan_ids.add(scan_id)
                print(f"   - Scan ID: {scan_id}")

                # Get actual status if available
                status = "Submitted"
                if hasattr(scan, 'status'):
                    if scan.status == 'complete':
                        status = "Complete"
                    else:
                        status = scan.status.capitalize()
                print(f"   - Status: {status}")

                # Extract additional info from result if available
                if hasattr(scan, 'result') and scan.result:
                    result = scan.result
                    # Show profile info
                    if hasattr(result, 'profile_name') and result.profile_name:
                        print(f"   - Profile: {result.profile_name}")
                    elif hasattr(result, 'profile_id') and result.profile_id:
                        print(f"   - Profile ID: {result.profile_id}")

    # Wait a bit longer for report results
    time.sleep(5)

    print("\n9. Querying results by report ID...")
    print("=" * 60)

    # Initialize retry variables
    max_retries = 3
    retry_count = 0
    retry_wait = 10  # seconds
    has_results = False
    report_by_ids_response = None

    while retry_count < max_retries and not has_results:
        if retry_count > 0:
            print(f"\n   Waiting {retry_wait} seconds before retry {retry_count}/{max_retries-1}...")
            time.sleep(retry_wait)
            print("   Retrying query for report results...")

        # Query scan results by report ID
        report_by_ids_response = scanner.query_by_report_ids(
            report_ids=[scan_async_response.report_id]
        )
        print("=" * 60 if retry_count == 0 else "")

        # Determine the reports - the response is a list of ThreatScanReportObject objects
        reports = report_by_ids_response.reports if hasattr(report_by_ids_response, 'reports') else report_by_ids_response

        # Check for detection_results field which contains the actual scan results
        if reports:
            for report in reports:
                if hasattr(report, 'detection_results') and report.detection_results:
                    # If we have detection results, consider the report as having results
                    has_results = True
                    break

        retry_count += 1

        # If we have results or we've reached max retries, break out
        if has_results or retry_count >= max_retries:
            break

    # Print report query response details
    print("\n   Report Details:")

    if not report_by_ids_response:
        print("   No report data available")
    elif not reports:
        print("   No reports available in response")
    else:
        # Use a set to keep track of already printed report IDs to avoid duplicates
        printed_report_ids = set()

        for report in reports:
            report_id = report.report_id if hasattr(report, 'report_id') else 'N/A'

            # Only print report details once per report ID
            if report_id not in printed_report_ids:
                printed_report_ids.add(report_id)

                # Basic report details
                print(f"   - Report ID: {report_id}")

                # Extract profile name if available
                profile_name = "N/A"
                if hasattr(report, 'profile_name') and report.profile_name:
                    profile_name = report.profile_name
                elif hasattr(report, 'to_dict'):
                    try:
                        report_dict = report.to_dict()
                        if report_dict.get('profile_name'):
                            profile_name = report_dict['profile_name']
                    except Exception:
                        pass
                print(f"   - Profile: {profile_name}")

                # Determine status based on retry count
                status = "Processing" if has_results else "Submitted"
                print(f"   - Status: {status}")

                # Get info about this specific report
                req_id = report.req_id if hasattr(report, 'req_id') else 'N/A'
                transaction_id = report.transaction_id if hasattr(report, 'transaction_id') else 'N/A'

                # Get detection results if available
                detection_results = []
                if hasattr(report, 'detection_results'):
                    detection_results = report.detection_results
                elif hasattr(report, 'to_dict'):
                    try:
                        report_dict = report.to_dict()
                        if report_dict.get('detection_results'):
                            detection_results = report_dict['detection_results']
                    except Exception:
                        pass

                # Process detection results if available
                if detection_results:
                    # Display real results from detection_results
                    print(f"\n   Individual Scan Results for Request ID: {req_id}, Transaction ID: {transaction_id}")

                    # Organize detection results by data type and verdict
                    prompt_results = []
                    response_results = []
                    for dr in detection_results:
                        if hasattr(dr, 'data_type') and dr.data_type == 'prompt':
                            prompt_results.append(dr)
                        elif hasattr(dr, 'data_type') and dr.data_type == 'response':
                            response_results.append(dr)

                    # Display summary of prompt and response verdicts
                    worst_prompt_verdict = 'benign'
                    worst_prompt_action = 'allow'
                    for pr in prompt_results:
                        if hasattr(pr, 'verdict') and pr.verdict == 'malicious':
                            worst_prompt_verdict = 'malicious'
                        if hasattr(pr, 'action') and pr.action == 'block':
                            worst_prompt_action = 'block'

                    worst_response_verdict = 'benign'
                    worst_response_action = 'allow'
                    for rr in response_results:
                        if hasattr(rr, 'verdict') and rr.verdict == 'malicious':
                            worst_response_verdict = 'malicious'
                        if hasattr(rr, 'action') and rr.action == 'block':
                            worst_response_action = 'block'

                    print(f"   Prompt Verdict: {worst_prompt_verdict.capitalize()}, Action: {worst_prompt_action.capitalize()}")
                    print(f"   Response Verdict: {worst_response_verdict.capitalize()}, Action: {worst_response_action.capitalize()}")

                    # Display details of malicious detections
                    malicious_detections = []
                    for dr in detection_results:
                        if hasattr(dr, 'verdict') and dr.verdict == 'malicious':
                            malicious_detections.append(dr)

                    if malicious_detections:
                        print("\n   Malicious Detection Details:")
                        for md in malicious_detections:
                            data_type = md.data_type if hasattr(md, 'data_type') else 'unknown'
                            service = md.detection_service if hasattr(md, 'detection_service') else 'unknown'
                            action = md.action if hasattr(md, 'action') else 'unknown'

                            print(f"   - In {data_type}, {service} service detected threat, action: {action}")

                            # If URL filtering detection, show URLs
                            if hasattr(md, 'result_detail'):
                                result_detail = md.result_detail
                                if hasattr(result_detail, 'urlf_report'):
                                    urlf_report = result_detail.urlf_report
                                    if urlf_report:
                                        for url_entry in urlf_report:
                                            url = url_entry.url if hasattr(url_entry, 'url') else 'unknown'
                                            categories = url_entry.categories if hasattr(url_entry, 'categories') else []
                                            print(f"     URL: {url}, Categories: {', '.join(categories)}")

                    # Print summary
                    overall_action = 'allow'
                    if worst_prompt_action == 'block' or worst_response_action == 'block':
                        overall_action = 'block'

                    if overall_action == 'allow':
                        print("\n   ✅ Content allowed")
                    else:
                        print("\n   ⚠️ Content blocked")
                else:
                    # No detection results yet, show simulated info
                    print(f"\n   Individual Scan Results for Request ID: {req_id}, Transaction ID: {transaction_id}")
                    print("   Status: Processing")

                    # Try to find the corresponding content from our original submission
                    if req_id == 1:
                        print(f"   Prompt: {content1.prompt[:30]}...")
                    elif req_id == 2:
                        print(f"   Prompt: {content2.prompt[:30]}...")

                print("   " + "-" * 40)

    print("\n=== EXAMPLE COMPLETED ===")


if __name__ == "__main__":
    main()
