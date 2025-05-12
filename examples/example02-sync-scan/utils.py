#!/usr/bin/env python3
"""
Utility Functions for AI Security SDK Synchronous Scan Example
This module provides utility functions for the synchronous scan example script.
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
