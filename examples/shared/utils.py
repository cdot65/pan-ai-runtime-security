#!/usr/bin/env python3
"""
Utility Functions for AI Security SDK Examples
This module provides common utility functions used across the example scripts.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv


def load_environment() -> Dict[str, Optional[str]]:
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
            # Try parent directory (for shared environment)
            parent_dir = script_dir.parent.absolute()
            env_path = parent_dir / ".env"
            if env_path.exists():
                load_dotenv(dotenv_path=env_path)
            else:
                print("No .env file found in current or parent directories")
                print("Please copy .env.example to .env and add your credentials")
                sys.exit(1)

    # Get credentials from environment variables with fallbacks
    api_key = os.environ.get("PANW_AI_SEC_API_KEY", None)
    api_endpoint = os.environ.get("PANW_AI_SEC_API_ENDPOINT", "https://service.api.aisecurity.paloaltonetworks.com")
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


def get_example_contents() -> list:
    """
    Get a list of example content for testing

    Returns:
        list: Sample content items with prompts and responses
    """
    return [
        {
            "prompt": "Tell me a joke",
            "response": "Why did the chicken cross the road? To get to the other side!",
        },
        {
            "prompt": "This is a test prompt with 72zf6.rxqfd.com/i8xps1 URL",
            "response": "This is a test response",
        },
        {
            "prompt": "Normal request about weather",
            "response": "The weather forecast shows sunny conditions.",
        },
        {
            "prompt": "Secret bank account 8775664322 routing number 2344567",
            "response": "I cannot process requests with sensitive information.",
        },
    ]


def print_scan_result_summary(scan_response: Any) -> None:
    """
    Print a summary of scan results

    Args:
        scan_response: The response from a security scan
    """
    try:
        print(f"Scan ID: {scan_response.scan_id}")
        print(f"Report ID: {scan_response.report_id}")
        print(f"Transaction ID: {scan_response.tr_id}")
        print(f"Category: {scan_response.category}")
        print(f"Action: {scan_response.action}")

        # Prettify the detection results
        if hasattr(scan_response, "prompt_detected"):
            print_detection_summary("Prompt", scan_response.prompt_detected)

        if hasattr(scan_response, "response_detected"):
            print_detection_summary("Response", scan_response.response_detected)

        # Print action summary
        if scan_response.action == "allow":
            print("✅ Content allowed")
        else:
            print("⚠️ Content blocked")
    except AttributeError as e:
        print(f"Error accessing scan response attribute: {e}")
    except Exception as e:
        print(f"Error printing scan result: {e}")


def print_detection_summary(source: str, detection: Any) -> None:
    """
    Print a summary of detections for a given source (prompt or response)

    Args:
        source: The source of the detection ("Prompt" or "Response")
        detection: The detection object containing flags
    """
    detections = []

    try:
        if hasattr(detection, "url_cats") and detection.url_cats:
            detections.append("URL categories")
        if hasattr(detection, "dlp") and detection.dlp:
            detections.append("DLP")
        if hasattr(detection, "injection") and source == "Prompt" and detection.injection:
            detections.append("Injection")

        if detections:
            print(f"{source} detected issues: {', '.join(detections)}")
        else:
            print(f"No issues detected in {source.lower()}")
    except Exception as e:
        print(f"Error printing detection summary: {e}")
