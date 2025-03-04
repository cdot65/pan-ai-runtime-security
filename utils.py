#!/usr/bin/env python3
"""
Utility Functions for AI Security SDK Examples
This module provides common utility functions used across the example scripts.
"""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def load_environment():
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
        "https://security.api.aisecurity.paloaltonetworks.com",
    )
    profile_id = os.environ.get("DEMO_AI_PROFILE_ID", None)
    profile_name = os.environ.get("DEMO_AI_PROFILE_NAME", None)
    log_level = os.environ.get("LOG_LEVEL", "INFO")

    # Validate required credentials
    if not api_key:
        print("Missing required PANW_AI_SEC_API_KEY environment variable")
        print("Please set this in your .env file")
        sys.exit(1)

    if not profile_id and not profile_name:
        print("Warning: Neither DEMO_AI_PROFILE_ID nor DEMO_AI_PROFILE_NAME is set")
        print("At least one should be provided for the examples to work correctly")

    return {
        "api_key": api_key,
        "api_endpoint": api_endpoint,
        "profile_id": profile_id,
        "profile_name": profile_name,
        "log_level": log_level,
    }


def get_example_contents():
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


def print_scan_result_summary(scan_response):
    """
    Print a summary of scan results

    Args:
        scan_response: The response from a security scan
    """
    print(f"Scan ID: {scan_response.scan_id}")
    print(f"Report ID: {scan_response.report_id}")
    print(f"Transaction ID: {scan_response.tr_id}")
    print(f"Category: {scan_response.category}")
    print(f"Action: {scan_response.action}")

    # Prettify the detection results
    if scan_response.prompt_detected:
        detections = []
        if scan_response.prompt_detected.url_cats:
            detections.append("URL categories")
        if scan_response.prompt_detected.dlp:
            detections.append("DLP")
        if scan_response.prompt_detected.injection:
            detections.append("Injection")

        if detections:
            print(f"Prompt detected issues: {', '.join(detections)}")
        else:
            print("No issues detected in prompt")

    if scan_response.response_detected:
        detections = []
        if scan_response.response_detected.url_cats:
            detections.append("URL categories")
        if scan_response.response_detected.dlp:
            detections.append("DLP")

        if detections:
            print(f"Response detected issues: {', '.join(detections)}")
        else:
            print("No issues detected in response")

    # Print action summary
    if scan_response.action == "allow":
        print("✅ Content allowed")
    else:
        print("⚠️ Content blocked")
