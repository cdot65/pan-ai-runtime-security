# Mock Implementation Example

This example demonstrates a mock implementation of the Palo Alto Networks AI Security SDK for testing and development without requiring actual API credentials.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Key Concepts](#key-concepts)
- [Sample Output](#sample-output)

## Overview

This example shows how to:
- Create a mock implementation of the AI Security SDK
- Simulate security scanning responses for testing
- Implement different detection patterns for testing various scenarios
- Test decorator patterns with mock implementations
- Develop and test without requiring valid API credentials

## Setup

### Python Environment Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-example06 .venv
   source .venv/bin/activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. No valid API credentials are required for this example, as it uses a mock implementation.

## Usage

Run the example script:

```bash
python main.py
```

## Key Concepts

### Mock Implementation

A mock implementation:
- Simulates the behavior of a real system
- Works without external dependencies
- Provides predictable responses for testing
- Allows development without valid credentials

### Mock Classes

This example implements mock versions of:
- `PromptDetected` and `ResponseDetected` classes
- `ScanResponse` class with realistic detection logic
- `MockScanner` that simulates the scanning process
- `MockContent` and `MockAiProfile` classes

### Detection Simulation

The mock implementation includes simple detection logic:
- URL detection based on the presence of "url" in the prompt
- Sensitive information detection for "bank account" or "password"
- Injection detection for "ignore" in the prompt
- Realistic UUIDs and timestamps in responses

### Testing Patterns

Two main testing patterns are demonstrated:
- Direct API usage pattern with the mock scanner
- Decorator pattern using the mock implementation

## Sample Output

```
=== AI SECURITY SDK MOCK EXAMPLES ===
Note: These examples use mock implementations to simulate SDK behavior

=== SYNCHRONOUS SCAN EXAMPLE ===

Mock scanner created successfully
Testing with safe content...
Scanning content: Tell me a joke
  Scan ID: 550e8400-e29b-41d4-a716-446655440000
  Report ID: 6ba7b810-9dad-11d1-80b4-00c04fd430c8
  Action: allow
  No issues detected in prompt
  ✅ Content allowed

Testing with unsafe content...
Scanning content: This is a test prompt with malicious url
  Scan ID: 6ba7b810-9dad-11d1-80b4-00c04fd430c8
  Report ID: 6ba7b811-9dad-11d1-80b4-00c04fd430c8
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

This output shows:
1. A mock scanner being created without real API credentials
2. Testing with safe content that passes security checks
3. Testing with unsafe content that gets blocked
4. A decorator pattern implementation using the mock scanner
5. Various inputs being tested with the mock implementation