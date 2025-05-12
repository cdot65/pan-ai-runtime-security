#!/usr/bin/env python3
"""
Utility Functions for AI Security SDK Asynchronous Scan Example
This module provides utility functions for the asynchronous scan example script.
"""

import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


def load_environment() -> dict[str, str | None]:
    """
    Load environment variables from .env file

    Returns:
        dict: Environment configuration including API credentials
    """
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
            print("Please copy .env.example to .env and add your credentials")
            sys.exit(1)

    # Get credentials from environment variables with fallbacks
    api_key = os.environ.get("PANW_AI_SEC_API_KEY", None)
    api_endpoint = os.environ.get(
        "PANW_AI_SEC_API_ENDPOINT",
        "https://service.api.aisecurity.paloaltonetworks.com"
    )
    profile_name = os.environ.get("PANW_AI_PROFILE_NAME", None)
    profile_id = os.environ.get("PANW_AI_PROFILE_ID", None)
    log_level = os.environ.get("LOG_LEVEL", "INFO")

    # Validate required credentials
    if not api_key:
        print("Missing required PANW_AI_SEC_API_KEY environment variable")
        print("Please set this in your .env file")
        sys.exit(1)

    if not profile_name and not profile_id:
        print("Warning: Neither PANW_AI_PROFILE_NAME nor PANW_AI_PROFILE_ID is set")
        print("At least one should be provided for the examples to work correctly")

    return {
        "api_key": api_key,
        "api_endpoint": api_endpoint,
        "profile_name": profile_name,
        "profile_id": profile_id,
        "log_level": log_level,
    }


def print_detailed_scan_result(scan_response: Any) -> None:
    """
    Print a detailed summary of scan results

    Args:
        scan_response: The response from a security scan
    """
    try:
        print(f"Scan ID: {scan_response.scan_id}")
        print(f"Report ID: {scan_response.report_id}")
        print(f"Transaction ID: {scan_response.tr_id}")
        print(f"Category: {scan_response.category}")
        print(f"Action: {scan_response.action}")

        # Detailed detection information
        if hasattr(scan_response, "prompt_detected"):
            if hasattr(scan_response.prompt_detected, "url_cats"):
                print(f"Prompt URL Detection: {scan_response.prompt_detected.url_cats}")
            if hasattr(scan_response.prompt_detected, "dlp"):
                print(f"Prompt DLP Detection: {scan_response.prompt_detected.dlp}")
            if hasattr(scan_response.prompt_detected, "injection"):
                print(f"Prompt Injection Detection: {scan_response.prompt_detected.injection}")

        if hasattr(scan_response, "response_detected"):
            if hasattr(scan_response.response_detected, "url_cats"):
                print(f"Response URL Detection: {scan_response.response_detected.url_cats}")
            if hasattr(scan_response.response_detected, "dlp"):
                print(f"Response DLP Detection: {scan_response.response_detected.dlp}")

        # Print action summary
        if scan_response.action == "allow":
            print("✅ Content allowed")
        else:
            print("⚠️ Content blocked")
    except AttributeError as e:
        print(f"Error accessing scan response attribute: {e}")
    except Exception as e:
        print(f"Error printing scan result: {e}")


def print_async_scan_results(report_response: Any) -> None:
    """
    Print detailed results from an asynchronous scan report

    Args:
        report_response: The response from querying report IDs
    """
    try:
        if not hasattr(report_response, "reports") or not report_response.reports:
            print("No report data available")
            return

        for report in report_response.reports:
            print(f"\nReport ID: {report.report_id}")

            if hasattr(report, "profile_id") and report.profile_id:
                print(f"Profile ID: {report.profile_id}")

            if hasattr(report, "profile_name") and report.profile_name:
                print(f"Profile Name: {report.profile_name}")

            if hasattr(report, "report_status"):
                print(f"Status: {report.report_status}")

            if not hasattr(report, "results") or not report.results:
                print("No results available in this report")
                continue

            print("\nIndividual Scan Results:")
            for result in report.results:
                print(f"\nRequest ID: {result.req_id}")

                if hasattr(result, "tr_id"):
                    print(f"Transaction ID: {result.tr_id}")

                if hasattr(result, "scan_id"):
                    print(f"Scan ID: {result.scan_id}")

                if hasattr(result, "category"):
                    print(f"Category: {result.category}")

                if hasattr(result, "action"):
                    print(f"Action: {result.action}")

                # Print detection details
                if hasattr(result, "prompt_detected"):
                    prompt_detected = result.prompt_detected
                    print("\nPrompt Detection Results:")

                    if hasattr(prompt_detected, "url_cats"):
                        print(f"  URL Categories: {prompt_detected.url_cats}")

                    if hasattr(prompt_detected, "dlp"):
                        print(f"  DLP: {prompt_detected.dlp}")

                    if hasattr(prompt_detected, "injection"):
                        print(f"  Injection: {prompt_detected.injection}")

                if hasattr(result, "response_detected"):
                    response_detected = result.response_detected
                    print("\nResponse Detection Results:")

                    if hasattr(response_detected, "url_cats"):
                        print(f"  URL Categories: {response_detected.url_cats}")

                    if hasattr(response_detected, "dlp"):
                        print(f"  DLP: {response_detected.dlp}")

                # Print result summary
                if hasattr(result, "action"):
                    if result.action == "allow":
                        print("\n✅ Content allowed")
                    else:
                        print("\n⚠️ Content blocked")

                print("-" * 50)

    except AttributeError as e:
        print(f"Error accessing report attribute: {e}")
    except Exception as e:
        print(f"Error printing async scan results: {e}")

