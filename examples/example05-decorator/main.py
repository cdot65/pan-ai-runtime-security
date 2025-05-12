#!/usr/bin/env python3
"""
Decorator Pattern Example for AI Security SDK
This script demonstrates how to use the decorator pattern to automatically
scan user inputs for security threats before processing them.

Required Environment Variables:
- PANW_AI_SEC_API_KEY: Your Palo Alto Networks AI Security API key
- At least one of the following profile identifiers:
  - PANW_AI_PROFILE_NAME: The name of your AI security profile
  - PANW_AI_PROFILE_ID: The ID of your AI security profile

Optional Environment Variables:
- PANW_AI_SEC_API_ENDPOINT: The API endpoint URL (defaults to Palo Alto Networks cloud endpoint)
"""
import logging
import sys
from functools import wraps

import aisecurity
from aisecurity.generated_openapi_client.models.ai_profile import AiProfile
from aisecurity.scan.inline.scanner import Scanner
from aisecurity.scan.models.content import Content

# Import local utilities
from utils import load_environment


def ai_runtime_init(profile_id=None, profile_name=None, api_key=None, api_endpoint=None):
    """
    Initialize the AI Runtime Security SDK

    Args:
        profile_id (str, optional): The AI security profile ID
        profile_name (str, optional): The AI security profile name
        api_key (str): The API key for authentication
        api_endpoint (str): The API endpoint URL

    Returns:
        dict: Configuration dictionary with scanner and profile
    """
    print("1. Initializing the AI Security SDK...")
    aisecurity.init(api_key=api_key, api_endpoint=api_endpoint)
    print(f"   SDK initialized with endpoint: {api_endpoint}")

    print("\n2. Creating scanner...")
    # Create the scanner instance
    scanner = Scanner()
    print("   Scanner created successfully")

    print("\n3. Setting up AI profile...")
    # Create AI profile with either ID or name (at least one must be provided)
    if profile_id:
        ai_security_profile = AiProfile(profile_id=profile_id)
        print(f"   Using profile ID: {profile_id}")
    elif profile_name:
        ai_security_profile = AiProfile(profile_name=profile_name)
        print(f"   Using profile name: {profile_name}")
    else:
        # Use a default profile if none provided
        ai_security_profile = AiProfile(profile_name="default_profile")
        print("   Using default profile name: default_profile")

    return {
        "scanner": scanner,
        "ai_security_profile": ai_security_profile,
    }


def check_user_content(ai_runtime_profile, error_func=None, debug=False):
    """
    Decorator to protect against malicious prompts

    Args:
        ai_runtime_profile (dict): Configuration with scanner and profile
        error_func (callable, optional): Function to call if input is blocked
        debug (bool): Enable debugging output

    Returns:
        callable: Decorator function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_input = kwargs["user_input"]

            # Create content object with user input as prompt
            content = Content(prompt=user_input)
            scanner = ai_runtime_profile["scanner"]
            ai_profile = ai_runtime_profile["ai_security_profile"]

            try:
                print("\n4. Scanning user input for security threats...")
                print("=" * 60)
                scan_response = scanner.sync_scan(
                    ai_profile=ai_profile, content=content
                )
                print("=" * 60)

                is_blocked = scan_response.action != "allow" if scan_response else True

                if debug:
                    print("\n5. Scan Results:")
                    print(f"   Scan ID: {scan_response.scan_id}")
                    print(f"   Report ID: {scan_response.report_id}")
                    if hasattr(scan_response, "tr_id"):
                        print(f"   Transaction ID: {scan_response.tr_id}")
                    print(f"   Category: {scan_response.category}")
                    print(f"   Action: {scan_response.action}")

                    # Display detection details if available
                    if hasattr(scan_response, "prompt_detected"):
                        pd = scan_response.prompt_detected
                        print("\n   Prompt Detection Details:")
                        if hasattr(pd, "url_cats"):
                            print(f"   - URL Categories: {pd.url_cats}")
                        if hasattr(pd, "dlp"):
                            print(f"   - DLP: {pd.dlp}")
                        if hasattr(pd, "injection"):
                            print(f"   - Injection: {pd.injection}")

                    if hasattr(scan_response, "response_detected"):
                        rd = scan_response.response_detected
                        print("\n   Response Detection Details:")
                        if hasattr(rd, "url_cats"):
                            print(f"   - URL Categories: {rd.url_cats}")
                        if hasattr(rd, "dlp"):
                            print(f"   - DLP: {rd.dlp}")

                    print(f"\n   Is blocked: {is_blocked}")

            except Exception as e:
                if debug:
                    print(f"\n   Exception: {e}")
                # If we can't reach the API, default to safe behavior in dev environments
                # In production, you might want to block by default
                is_blocked = True

                # Extract the meaningful part of the error message
                error_message = str(e)
                if "NameResolutionError" in error_message:
                    print("\n⚠️ Could not connect to AI Security API - check network connection and API endpoint")
                elif "Invalid API key" in error_message:
                    print("\n⚠️ Invalid API key - check your PANW_AI_SEC_API_KEY environment variable")
                elif "neither profile ID nor profile name is present" in error_message:
                    print("\n⚠️ Missing profile configuration - set either PANW_AI_PROFILE_ID or PANW_AI_PROFILE_NAME")

            print("\n6. Processing according to scan verdict...")
            if is_blocked and error_func:
                return error_func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def dummy_error_message(user_input):
    """
    Example error handling function

    Args:
        user_input (str): The user input that was blocked
    """
    print(f"   ⚠️ Security alert: Cannot process this input: {user_input}")


def main():
    """Main execution function"""
    print("=== DECORATOR PATTERN AI SECURITY SDK EXAMPLE ===\n")

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    try:
        # Load environment variables
        env = load_environment()

        # Initialize the AI runtime profile
        ai_runtime_profile = ai_runtime_init(
            profile_id=env["profile_id"],
            profile_name=env["profile_name"],
            api_key=env["api_key"],
            api_endpoint=env["api_endpoint"],
        )

        # Define the business logic function protected by the security decorator
        @check_user_content(ai_runtime_profile, dummy_error_message, debug=True)
        def process_user_input(user_input):
            """Business logic that processes user input after security check"""
            print(f"   ✅ Processing safe input: {user_input}")
            return f"Processed: {user_input}"

        # Test with different example inputs
        example_inputs = [
            "Tell me a joke",
            "This is a test prompt with 72zf6.rxqfd.com/i8xps1 URL that should be detected",
            "Here's my bank account 8775664322 and routing number 2344567",
            "What's the weather like today?",
        ]

        # Process each input
        for i, input_text in enumerate(example_inputs, 1):
            print(f"\nUser Input #{i}: {input_text}")
            result = process_user_input(user_input=input_text)
            if result:
                print(f"   Result: {result}")

        print("\n=== EXAMPLE COMPLETED ===")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
