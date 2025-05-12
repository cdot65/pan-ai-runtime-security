#!/usr/bin/env python3
"""
Asyncio Concurrent SDK Usage Example for AI Security
This script demonstrates how to use asyncio for concurrent operations
with the AI Security SDK for improved performance.
"""
import asyncio
import logging

import aisecurity
from aisecurity.generated_openapi_client.models.ai_profile import AiProfile
from aisecurity.generated_openapi_client.models.async_scan_object import AsyncScanObject
from aisecurity.generated_openapi_client.models.metadata import Metadata
from aisecurity.generated_openapi_client.models.scan_request import ScanRequest
from aisecurity.generated_openapi_client.models.scan_request_contents_inner import (
    ScanRequestContentsInner,
)
from aisecurity.scan.asyncio.scanner import Scanner  # Note the asyncio.scanner import
from aisecurity.scan.models.content import Content

# Import local utilities
from utils import load_environment


async def run_concurrent_scans(env):
    """
    Run multiple scan operations concurrently

    Args:
        env (dict): Environment configuration including API credentials
    """
    # Configure logging based on environment variable
    logging.basicConfig(level=getattr(logging, env["log_level"]))

    print("1. Initializing SDK...")
    # Initialize SDK
    aisecurity.init(api_key=env["api_key"], api_endpoint=env["api_endpoint"])
    print(f"   SDK initialized with endpoint: {env['api_endpoint']}")

    print("\n2. Creating scanner...")
    # Create scanner instance for asyncio operations
    ai_security_scanner = Scanner()
    print("   Scanner created successfully")

    print("\n3. Setting up AI profile...")
    # Create AI profile with environment variables
    if env["profile_id"]:
        ai_profile = AiProfile(profile_id=env["profile_id"])
        print(f"   Using profile ID: {env['profile_id']}")
    else:
        ai_profile = AiProfile(profile_name=env["profile_name"])
        print(f"   Using profile name: {env['profile_name']}")

    print("\n4. Creating content for batch scanning...")
    # Create content object
    content1 = Content(
        prompt="This is a test prompt with 72zf6.rxqfd.com/i8xps1 URL that should be detected",
        response="This is a test response for the first item",
    )

    content2 = Content(
        prompt="This is another test prompt without any malicious content",
        response="This is another test response for the second item",
    )
    print("   Created 2 content items for batch processing")

    # Optional metadata
    tr_id = "concurrent-tx-001"
    metadata = Metadata(
        app_name="concurrent_sdk", app_user="user", ai_model="sample_model"
    )

    print("\n5. Preparing async scan objects...")
    # Prepare async scan objects for batch processing
    async_scan_objects = [
        AsyncScanObject(
            req_id=1,
            scan_req=ScanRequest(
                tr_id="async-tx-001",
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
                tr_id="async-tx-002",
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

    print("\n6. Running concurrent operations...")
    print("=" * 60)
    # Run sync_scan and async_scan concurrently
    sync_scan_task = ai_security_scanner.sync_scan(
        ai_profile=ai_profile, content=content1, tr_id=tr_id, metadata=metadata
    )
    async_scan_task = ai_security_scanner.async_scan(async_scan_objects)

    # Wait for both tasks to complete
    sync_result, async_result = await asyncio.gather(sync_scan_task, async_scan_task)
    print("=" * 60)

    # Process and print results
    print("\n7. Synchronous scan results:")
    print(f"   Scan ID: {sync_result.scan_id}")
    print(f"   Report ID: {sync_result.report_id}")
    print(f"   Transaction ID: {sync_result.tr_id}")

    # Print verdict and action
    if hasattr(sync_result, "action"):
        action = sync_result.action
        print(f"   Action: {action.capitalize()}")
        if action == "allow":
            print("   ✅ Content allowed")
        else:
            print("   ⚠️ Content blocked")

    print("\n8. Asynchronous scan results:")
    print(f"   Scan ID: {async_result.scan_id}")
    print(f"   Report ID: {async_result.report_id}")
    print("   ✅ Async scan request submitted successfully")

    # Query for additional results if available
    if async_result and async_result.scan_id and async_result.report_id:
        print("\n9. Querying for additional scan results...")
        print("=" * 60)

        # Initialize retry variables
        max_retries = 3
        retry_count = 0
        retry_wait = 10  # seconds
        scan_completed = False

        # Query by scan IDs
        while retry_count < max_retries and not scan_completed:
            if retry_count > 0:
                print(f"\n   Waiting {retry_wait} seconds before retry {retry_count}/{max_retries-1}...")
                await asyncio.sleep(retry_wait)
                print("   Retrying query for scan status...")

            scan_by_ids_response = await ai_security_scanner.query_by_scan_ids(
                scan_ids=[async_result.scan_id]
            )
            print("=" * 60 if retry_count == 0 else "")

            # Check if any of the scans are complete
            if scan_by_ids_response and len(scan_by_ids_response) > 0:
                for scan in scan_by_ids_response:
                    if hasattr(scan, 'status') and scan.status == 'complete':
                        scan_completed = True
                        break

            retry_count += 1

            # Break if scan is completed or max retries reached
            if scan_completed or retry_count >= max_retries:
                break

        # Print scan details
        print("\n   Scan Status Details:")
        if scan_by_ids_response and len(scan_by_ids_response) > 0:
            for scan in scan_by_ids_response:
                if hasattr(scan, 'scan_id'):
                    print(f"   - Scan ID: {scan.scan_id}")
                if hasattr(scan, 'status'):
                    status = scan.status.upper() if hasattr(scan, 'status') else "UNKNOWN"
                    print(f"   - Status: {status}")
                if hasattr(scan, 'created_at'):
                    print(f"   - Created: {scan.created_at}")
                if hasattr(scan, 'completed_at'):
                    print(f"   - Completed: {scan.completed_at}")
        else:
            print("   No scan details available")

        # Give some time for the report to be ready
        await asyncio.sleep(5)

        print("\n10. Querying for detailed report...")
        print("=" * 60)

        # Initialize retry variables
        max_retries = 3
        retry_count = 0
        retry_wait = 10  # seconds
        has_results = False

        # Query by report IDs
        while retry_count < max_retries and not has_results:
            if retry_count > 0:
                print(f"\n   Waiting {retry_wait} seconds before retry {retry_count}/{max_retries-1}...")
                await asyncio.sleep(retry_wait)
                print("   Retrying query for report results...")

            report_by_ids_response = await ai_security_scanner.query_by_report_ids(
                report_ids=[async_result.report_id]
            )
            print("=" * 60 if retry_count == 0 else "")

            # Check for detection results
            if report_by_ids_response:
                reports = report_by_ids_response.reports if hasattr(report_by_ids_response, 'reports') else report_by_ids_response

                if reports:
                    for report in reports:
                        if hasattr(report, 'detection_results') and report.detection_results:
                            has_results = True
                            break

            retry_count += 1

            # Break if results found or max retries reached
            if has_results or retry_count >= max_retries:
                break

        # Process detailed report results
        print("\n   Report Details:")
        if report_by_ids_response:
            reports = report_by_ids_response.reports if hasattr(report_by_ids_response, 'reports') else report_by_ids_response

            if reports:
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

                        print("   " + "-" * 40)
            else:
                print("   No reports available in response")
        else:
            print("   No report data available")

    # Clean up resources
    await ai_security_scanner.close()


async def main_async():
    """Asynchronous main execution function"""
    print("=== ASYNCIO CONCURRENT AI SECURITY SDK EXAMPLE ===\n")

    # Load environment variables
    env = load_environment()

    try:
        # Run the concurrent scans
        await run_concurrent_scans(env)
    except Exception as e:
        print(f"Error running concurrent scans: {e}")
        raise

    print("\n=== EXAMPLE COMPLETED ===")


def main():
    """Main execution function"""
    try:
        # Run the async function in the asyncio event loop
        asyncio.run(main_async())
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
