#!/usr/bin/env python3
"""
Mock Implementation of AI Security SDK for Testing
This script demonstrates how the examples would work with mocked responses.
"""
import sys
import uuid
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv


# Mock classes to simulate the SDK behavior
class PromptDetected:
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
    def __init__(self, url_cats=False, dlp=False):
        self.url_cats = url_cats
        self.dlp = dlp

    def __repr__(self):
        return f"ResponseDetected(url_cats={self.url_cats}, dlp={self.dlp})"


class ScanResponse:
    def __init__(self, prompt, response, action="allow"):
        self.scan_id = str(uuid.uuid4())
        self.report_id = str(uuid.uuid4())
        self.tr_id = "mock-transaction-id"
        self.profile_id = "mock-profile-id"
        self.profile_name = "mock-profile-name"
        self.category = "security"
        self.action = action  # "allow" or "block"

        # Detect "malicious" content based on simple patterns
        url_in_prompt = "url" in prompt.lower()
        sensitive_in_prompt = (
            "bank account" in prompt.lower()
            or "password" in prompt.lower()
        )
        injection_in_prompt = "ignore" in prompt.lower()

        self.prompt_detected = PromptDetected(
            url_cats=url_in_prompt,
            dlp=sensitive_in_prompt,
            injection=injection_in_prompt,
        )

        self.response_detected = ResponseDetected(url_cats=False, dlp=False)

        self.created_at = datetime.now()
        self.completed_at = datetime.now()

    def __repr__(self):
        return (
            f"ScanResponse(scan_id='{self.scan_id}', "
            f"report_id='{self.report_id}', "
            f"action='{self.action}', "
            f"prompt_detected={self.prompt_detected}, "
            f"response_detected={self.response_detected})"
        )


class MockScanner:
    def __init__(self):
        print("Mock scanner created successfully")

    def sync_scan(self, ai_profile, content, tr_id=None, metadata=None):
        """Simulate a synchronous scan"""
        print(f"Scanning content: {content.prompt}")

        # Determine if content should be blocked
        should_block = False
        if "url" in content.prompt.lower():
            should_block = True
        if "bank account" in content.prompt.lower():
            should_block = True
        if "password" in content.prompt.lower():
            should_block = True

        action = "block" if should_block else "allow"
        return ScanResponse(content.prompt, content.response, action)


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

    return {
        "api_key": "mock-api-key",
        "api_endpoint": "https://mock-api-endpoint.example.com",
        "profile_id": "mock-profile-id",
        "profile_name": "mock-profile-name",
    }


class MockContent:
    def __init__(self, prompt, response=None):
        self.prompt = prompt
        self.response = response


class MockAiProfile:
    def __init__(self, profile_id=None, profile_name=None):
        self.profile_id = profile_id
        self.profile_name = profile_name


def mock_sync_scan_example():
    """Demonstrate synchronous scanning with mock implementation"""
    print("\n=== SYNCHRONOUS SCAN EXAMPLE ===\n")

    # Create scanner and content
    scanner = MockScanner()
    ai_profile = MockAiProfile(profile_name="test-profile")

    # Test with safe content
    safe_content = MockContent(
        prompt="Tell me a joke",
        response="Why did the chicken cross the road? To get to the other side!",
    )

    print("Testing with safe content...")
    safe_result = scanner.sync_scan(ai_profile, safe_content)
    print_scan_result(safe_result)

    # Test with potentially unsafe content
    unsafe_content = MockContent(
        prompt="This is a test prompt with malicious url",
        response="This is a test response",
    )

    print("\nTesting with unsafe content...")
    unsafe_result = scanner.sync_scan(ai_profile, unsafe_content)
    print_scan_result(unsafe_result)


def mock_decorator_example():
    """Demonstrate decorator pattern with mock implementation"""
    print("\n=== DECORATOR PATTERN EXAMPLE ===\n")

    # Create scanner and profile
    scanner = MockScanner()
    ai_profile = MockAiProfile(profile_name="test-profile")

    # Mock implementation of the decorator
    def check_content(prompt):
        content = MockContent(prompt=prompt)
        scan_result = scanner.sync_scan(ai_profile, content)
        return scan_result.action == "allow"

    # Business logic function
    def process_user_input(prompt):
        is_safe = check_content(prompt)
        if is_safe:
            print(f"✅ Processing safe input: {prompt}")
        else:
            print(f"⚠️ Security alert: Cannot process this input: {prompt}")

    # Test with different inputs
    example_inputs = [
        "Tell me a joke",
        "This is a test prompt with malicious url",
        "Here's my bank account 8775664322 and routing number 2344567",
        "What's the weather like today?",
    ]

    for i, input_text in enumerate(example_inputs, 1):
        print(f"\nUser Input #{i}: {input_text}")
        process_user_input(input_text)


def print_scan_result(result):
    """Print a formatted summary of scan results"""
    print(f"  Scan ID: {result.scan_id}")
    print(f"  Report ID: {result.report_id}")
    print(f"  Action: {result.action}")

    # Prompt detections
    prompt_issues = []
    if result.prompt_detected.url_cats:
        prompt_issues.append("URL categories")
    if result.prompt_detected.dlp:
        prompt_issues.append("DLP")
    if result.prompt_detected.injection:
        prompt_issues.append("Injection")

    if prompt_issues:
        print(f"  Prompt detected issues: {', '.join(prompt_issues)}")
    else:
        print("  No issues detected in prompt")

    # Action summary
    if result.action == "allow":
        print("  ✅ Content allowed")
    else:
        print("  ⚠️ Content blocked")


def main():
    """Main execution function"""
    print("=== AI SECURITY SDK MOCK EXAMPLES ===")
    print("Note: These examples use mock implementations to simulate SDK behavior\n")

    # Run the mock examples
    mock_sync_scan_example()
    mock_decorator_example()

    print("\nMock examples completed successfully")


if __name__ == "__main__":
    main()
