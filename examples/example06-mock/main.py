#!/usr/bin/env python3
"""
Mock Implementation of AI Security SDK for Testing
This script demonstrates how the examples would work with mocked responses
without requiring actual API credentials or network connectivity.
"""
import logging
import sys
import uuid
from datetime import datetime
from functools import wraps


# Mock classes to simulate the SDK behavior
class PromptDetected:
    """Mock implementation of PromptDetected class"""
    def __init__(self, url_cats=False, dlp=False, injection=False):
        self.url_cats = url_cats
        self.dlp = dlp
        self.injection = injection

    def __repr__(self):
        return (
            f"PromptDetected(url_cats={self.url_cats}, dlp={self.dlp}, "
            f"injection={self.injection})"
        )


class ResponseDetected:
    """Mock implementation of ResponseDetected class"""
    def __init__(self, url_cats=False, dlp=False):
        self.url_cats = url_cats
        self.dlp = dlp

    def __repr__(self):
        return f"ResponseDetected(url_cats={self.url_cats}, dlp={self.dlp})"


class ScanResponse:
    """Mock implementation of ScanResponse class"""
    def __init__(self, prompt, response=None, action="allow"):
        self.scan_id = str(uuid.uuid4())
        self.report_id = f"R{self.scan_id}"
        self.tr_id = "mock-transaction-id"
        self.profile_id = "mock-profile-id"
        self.profile_name = "mock-profile-name"
        self.action = action  # "allow" or "block"

        # Detect "malicious" content based on simple patterns
        url_in_prompt = "url" in prompt.lower()
        sensitive_in_prompt = (
            "bank account" in prompt.lower()
            or "password" in prompt.lower()
            or "routing number" in prompt.lower()
        )
        injection_in_prompt = "ignore" in prompt.lower()

        # Set category based on detected issues
        if url_in_prompt:
            self.category = "security"
        elif sensitive_in_prompt:
            self.category = "dlp"
        elif injection_in_prompt:
            self.category = "policy"
        else:
            self.category = "none"

        self.prompt_detected = PromptDetected(
            url_cats=url_in_prompt,
            dlp=sensitive_in_prompt,
            injection=injection_in_prompt,
        )

        self.response_detected = ResponseDetected(url_cats=False, dlp=False)

        self.created_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.completed_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    def __repr__(self):
        return (
            f"ScanResponse(scan_id='{self.scan_id}', "
            f"report_id='{self.report_id}', "
            f"action='{self.action}', "
            f"prompt_detected={self.prompt_detected}, "
            f"response_detected={self.response_detected})"
        )


class MockScanner:
    """Mock implementation of Scanner class"""
    def __init__(self):
        """Initialize the mock scanner"""
        print("Mock scanner created successfully")

    def sync_scan(self, ai_profile, content, tr_id=None, metadata=None):
        """
        Simulate a synchronous scan
        
        Args:
            ai_profile: Mock AI profile
            content: Content to scan
            tr_id: Optional transaction ID
            metadata: Optional metadata
            
        Returns:
            ScanResponse: Mock scan response
        """
        print(f"Scanning content: {content.prompt}")

        # Determine if content should be blocked
        should_block = False
        if "url" in content.prompt.lower():
            should_block = True
        if "bank account" in content.prompt.lower():
            should_block = True
        if "password" in content.prompt.lower():
            should_block = True
        if "routing number" in content.prompt.lower():
            should_block = True

        action = "block" if should_block else "allow"
        return ScanResponse(content.prompt, content.response, action)


class MockContent:
    """Mock implementation of Content class"""
    def __init__(self, prompt, response=None):
        self.prompt = prompt
        self.response = response or "Mock response"


class MockAiProfile:
    """Mock implementation of AiProfile class"""
    def __init__(self, profile_id=None, profile_name=None):
        self.profile_id = profile_id
        self.profile_name = profile_name


def mock_load_environment():
    """
    Provide mock environment variables
    
    Returns:
        dict: Mock environment configuration
    """
    return {
        "api_key": "mock-api-key",
        "api_endpoint": "https://mock-api-endpoint.example.com",
        "profile_id": "mock-profile-id",
        "profile_name": "mock-profile-name",
        "log_level": "INFO",
    }


def print_scan_result(result):
    """
    Print a formatted summary of scan results
    
    Args:
        result: ScanResponse object
    """
    print("\n5. Scan Results:")
    print(f"   Scan ID: {result.scan_id}")
    print(f"   Report ID: {result.report_id}")
    if hasattr(result, "tr_id"):
        print(f"   Transaction ID: {result.tr_id}")
    print(f"   Category: {result.category}")
    print(f"   Action: {result.action}")

    # Prompt detections
    pd = result.prompt_detected
    print("\n   Prompt Detection Details:")
    print(f"   - URL Categories: {pd.url_cats}")
    print(f"   - DLP: {pd.dlp}")
    print(f"   - Injection: {pd.injection}")

    # Response detections
    rd = result.response_detected
    print("\n   Response Detection Details:")
    print(f"   - URL Categories: {rd.url_cats}")
    print(f"   - DLP: {rd.dlp}")

    # Block status
    is_blocked = result.action != "allow"
    print(f"\n   Is blocked: {is_blocked}")


def mock_sync_scan_example():
    """Demonstrate synchronous scanning with mock implementation"""
    print("\n=== SYNCHRONOUS SCAN EXAMPLE ===\n")

    print("1. Creating mock scanner...")
    # Create scanner and content
    scanner = MockScanner()

    print("\n2. Setting up mock AI profile...")
    ai_profile = MockAiProfile(profile_name="mock-profile")
    print("   Profile name: mock-profile")

    print("\n3. Testing with safe content...")
    # Test with safe content
    safe_content = MockContent(
        prompt="Tell me a joke",
        response="Why did the chicken cross the road? To get to the other side!",
    )

    print("4. Scanning safe content...")
    print("=" * 60)
    safe_result = scanner.sync_scan(ai_profile, safe_content)
    print("=" * 60)
    print_scan_result(safe_result)

    print("\n6. Processing according to scan verdict...")
    if safe_result.action == "allow":
        print("   ✅ Content allowed")
    else:
        print("   ⚠️ Content blocked")

    print("\n3. Testing with unsafe content...")
    # Test with potentially unsafe content
    unsafe_content = MockContent(
        prompt="This is a test prompt with malicious url",
        response="This is a test response",
    )

    print("4. Scanning unsafe content...")
    print("=" * 60)
    unsafe_result = scanner.sync_scan(ai_profile, unsafe_content)
    print("=" * 60)
    print_scan_result(unsafe_result)

    print("\n6. Processing according to scan verdict...")
    if unsafe_result.action == "allow":
        print("   ✅ Content allowed")
    else:
        print("   ⚠️ Content blocked")


def check_user_content(scanner, ai_profile, error_func=None, debug=False):
    """
    Decorator to protect against malicious prompts
    
    Args:
        scanner: Scanner instance
        ai_profile: AI profile
        error_func: Function to call if input is blocked
        debug: Enable debugging output
        
    Returns:
        callable: Decorator function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_input = kwargs["user_input"]

            # Create content object with user input as prompt
            content = MockContent(prompt=user_input)

            try:
                print("\n4. Scanning user input for security threats...")
                print("=" * 60)
                scan_response = scanner.sync_scan(
                    ai_profile=ai_profile, content=content
                )
                print("=" * 60)

                is_blocked = scan_response.action != "allow" if scan_response else True

                if debug:
                    print_scan_result(scan_response)

            except Exception as e:
                if debug:
                    print(f"\n   Exception: {e}")
                # If we can't reach the API, default to safe behavior in dev environments
                # In production, you might want to block by default
                is_blocked = True

                # Extract the meaningful part of the error message
                error_message = str(e)
                if "Connection error" in error_message:
                    print("\n⚠️ Could not connect to mock API - check network connection")
                elif "Invalid API key" in error_message:
                    print("\n⚠️ Invalid mock API key")
                elif "Missing profile" in error_message:
                    print("\n⚠️ Missing mock profile configuration")

            print("\n6. Processing according to scan verdict...")
            if is_blocked and error_func:
                return error_func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def mock_decorator_example():
    """Demonstrate decorator pattern with mock implementation"""
    print("\n=== DECORATOR PATTERN EXAMPLE ===\n")

    print("1. Creating mock scanner...")
    # Create scanner and profile
    scanner = MockScanner()

    print("\n2. Setting up mock AI profile...")
    ai_profile = MockAiProfile(profile_name="mock-profile")
    print("   Profile name: mock-profile")

    # Define error handling function
    def error_handler(user_input):
        """Example error handling function"""
        print(f"   ⚠️ Security alert: Cannot process this input: {user_input}")

    # Define the business logic function protected by the security decorator
    @check_user_content(scanner, ai_profile, error_handler, debug=True)
    def process_user_input(user_input):
        """Business logic that processes user input after security check"""
        print(f"   ✅ Processing safe input: {user_input}")
        return f"Processed: {user_input}"

    print("\n3. Testing with different example inputs...")
    # Test with different inputs
    example_inputs = [
        "Tell me a joke",
        "This is a test prompt with malicious url",
        "Here's my bank account 8775664322 and routing number 2344567",
        "What's the weather like today?",
    ]

    # Process each input
    for i, input_text in enumerate(example_inputs, 1):
        print(f"\nUser Input #{i}: {input_text}")
        result = process_user_input(user_input=input_text)
        if result:
            print(f"   Result: {result}")


def main():
    """Main execution function"""
    print("=== AI SECURITY SDK MOCK EXAMPLES ===")
    print("Note: These examples use mock implementations to simulate SDK behavior\n")

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    try:
        # Run the mock examples
        mock_sync_scan_example()
        mock_decorator_example()

        print("\n=== MOCK EXAMPLES COMPLETED ===")
    except Exception as e:
        print(f"Error running mock examples: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
