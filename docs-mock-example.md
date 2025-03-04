# AI Security SDK - Mock Implementation Documentation

## Overview

The `mock_example.py` script demonstrates a mock implementation of the AI Security SDK, allowing developers to test their applications without requiring actual API credentials or making real API calls. This approach is useful for testing, development, and demonstration purposes.

## Script Purpose

This script illustrates:

1. How to create mock classes that mimic the behavior of the actual SDK
2. Implementing simulated security checks for AI content
3. Demonstrating synchronous scanning with mock responses
4. Showing how to implement a decorator pattern with the mock scanner
5. Processing and interpreting mock scan results

## Key Components

### Mock Classes

The script creates mock classes that replicate the structure of the actual SDK:

#### PromptDetected Class

```python
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
```

#### ResponseDetected Class

```python
class ResponseDetected:
    def __init__(self, url_cats=False, dlp=False):
        self.url_cats = url_cats
        self.dlp = dlp

    def __repr__(self):
        return f"ResponseDetected(url_cats={self.url_cats}, dlp={self.dlp})"
```

#### ScanResponse Class

```python
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
```

#### MockScanner Class

```python
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
```

### Mock Environment

The script includes functions to simulate environment loading:

```python
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
```

### Mock Content Classes

```python
class MockContent:
    def __init__(self, prompt, response=None):
        self.prompt = prompt
        self.response = response


class MockAiProfile:
    def __init__(self, profile_id=None, profile_name=None):
        self.profile_id = profile_id
        self.profile_name = profile_name
```

### Synchronous Scan Example

The script demonstrates a mock synchronous scan:

```python
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
```

### Decorator Pattern Example

The script demonstrates using the mock implementation with a decorator pattern:

```python
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
```

### Result Processing

The script includes a utility function to format and display scan results:

```python
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
```

## Execution Example

When executed, the script produces output similar to:

```
=== AI SECURITY SDK MOCK EXAMPLES ===
Note: These examples use mock implementations to simulate SDK behavior


=== SYNCHRONOUS SCAN EXAMPLE ===

Mock scanner created successfully
Testing with safe content...
Scanning content: Tell me a joke
  Scan ID: 439b0f48-d9e2-495a-8f9f-0545d589a330
  Report ID: 40b33dbf-5d91-468d-9fbf-8102a69ffcd7
  Action: allow
  No issues detected in prompt
  ✅ Content allowed

Testing with unsafe content...
Scanning content: This is a test prompt with malicious url
  Scan ID: 91f668b9-2059-4980-ace8-f23689e172c3
  Report ID: 499fe54c-4865-45e3-8f7a-1d00e8bfaf37
  Action: block
  Prompt detected issues: URL categories
  ⚠️ Content blocked

=== DECORATOR PATTERN EXAMPLE ===

Mock scanner created successfully

User Input #1: Tell me a joke
Scanning content: Tell me a joke
✅ Processing safe input: Tell me a joke

User Input #2: This is a test prompt with malicious url
Scanning content: This is a test prompt with malicious url
⚠️ Security alert: Cannot process this input: This is a test prompt with malicious url

User Input #3: Here's my bank account 8775664322 and routing number 2344567
Scanning content: Here's my bank account 8775664322 and routing number 2344567
⚠️ Security alert: Cannot process this input: Here's my bank account 8775664322 and routing number 2344567

User Input #4: What's the weather like today?
Scanning content: What's the weather like today?
✅ Processing safe input: What's the weather like today?

Mock examples completed successfully
```

## Response Explanation

The mock implementation simulates the behavior of the actual SDK:

### Detection Logic

The mock scanner detects potential security issues based on simple patterns:
- URLs: Detected when "url" appears in the prompt
- Sensitive Data: Detected when "bank account" or "password" appears in the prompt
- Injection: Detected when "ignore" appears in the prompt (simulating prompt injection)

### Actions

The mock scanner determines the action based on detections:
- "allow": When no security issues are detected
- "block": When security issues are detected (URLs, sensitive data, etc.)

### Decorator Pattern

The decorator pattern example shows how to integrate the mock scanner into an application's security workflow:
1. Incoming content is first checked for security issues
2. Based on the scan result, the application decides whether to process the content
3. This pattern can be applied to any application that needs to filter AI content

## Usage Instructions

To run the script:

```bash
python mock_example.py
```

## Benefits of Mock Implementation

Using a mock implementation of the AI Security SDK offers several advantages:

1. **Development Without Credentials**: Develop and test without needing actual API credentials
2. **Offline Testing**: Test your application without requiring an internet connection
3. **Consistent Test Environment**: Ensure tests run consistently without API variability
4. **Faster Testing**: Mock implementations typically run faster than actual API calls
5. **Development Cost Reduction**: Reduce API usage during development and testing

## Integration into Applications

The mock implementation can be integrated into applications using conditional imports:

```python
try:
    # Try to import the real SDK
    from aisecurity.scan.sync.scanner import Scanner
except ImportError:
    # Fall back to mock implementation if real SDK is not available
    from mock_aisecurity import MockScanner as Scanner
```

This approach allows applications to seamlessly use either the real SDK in production or the mock implementation during development and testing.