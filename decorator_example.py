#!/usr/bin/env python3
"""
Decorator Pattern Example for AI Security SDK
This script demonstrates how to use the decorator pattern to automatically
scan user inputs for security threats before processing them.
"""
import os
import sys
from functools import wraps
from pathlib import Path

import aisecurity
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
    profile_id = os.environ.get("DEMO_AI_PROFILE_ID", None)
    profile_name = os.environ.get("DEMO_AI_PROFILE_NAME", None)

    # Validate required credentials
    if not api_key:
        print("Missing required PANW_AI_SEC_API_KEY environment variable")
        sys.exit(1)

    return {
        "api_key": api_key,
        "api_endpoint": api_endpoint,
        "profile_id": profile_id,
        "profile_name": profile_name,
    }


def ai_runtime_init(profile_name, api_key, api_endpoint):
    """
    Initialize the AI Runtime Security SDK

    Args:
        profile_name (str): The AI security profile name
        api_key (str): The API key for authentication
        api_endpoint (str): The API endpoint URL

    Returns:
        dict: Configuration dictionary with scanner and profile
    """
    aisecurity.init(api_key=api_key, api_endpoint=api_endpoint)
    return {
        "scanner": Scanner(),
        "ai_security_profile": AiProfile(profile_name=profile_name),
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
                scan_response = scanner.sync_scan(
                    ai_profile=ai_profile, content=content
                )
                is_blocked = scan_response.action != "allow" if scan_response else True

                if debug:
                    print(f"Scan response: {scan_response}")
                    print(f"Action: {scan_response.action}")
                    print(f"Is blocked: {is_blocked}")

            except Exception as e:
                if debug:
                    print(f"Exception: {e}")
                is_blocked = True

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
    print(f"⚠️ Security alert: Cannot process this input: {user_input}")


def main():
    """Main execution function"""
    # Load environment variables
    env = load_environment()

    # Initialize the AI runtime profile
    ai_runtime_profile = ai_runtime_init(
        profile_name=env["profile_name"],
        api_key=env["api_key"],
        api_endpoint=env["api_endpoint"],
    )

    # Define the business logic function protected by the security decorator
    @check_user_content(ai_runtime_profile, dummy_error_message, debug=True)
    def process_user_input(user_input):
        """Business logic that processes user input after security check"""
        print(f"✅ Processing safe input: {user_input}")

    # Test with different example inputs
    example_inputs = [
        "Tell me a joke",
        "This is a test prompt with 72zf6.rxqfd.com/i8xps1 url",
        "Here's my bank account 8775664322 and routing number 2344567",
        "What's the weather like today?",
    ]

    # Process each input
    for i, input_text in enumerate(example_inputs, 1):
        print(f"\nUser Input #{i}: {input_text}")
        process_user_input(user_input=input_text)


if __name__ == "__main__":
    main()
