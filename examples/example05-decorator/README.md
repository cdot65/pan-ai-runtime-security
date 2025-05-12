# Decorator Pattern Example

This example demonstrates how to use the decorator pattern to automatically scan user inputs for security threats before processing them using the Palo Alto Networks AI Security SDK.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Key Concepts](#key-concepts)
- [Sample Output](#sample-output)

## Overview

This example shows how to:
- Create a Python decorator for automatic security scanning
- Protect functions that process user input
- Implement custom error handling for blocked content
- Configure security scanning with different profiles
- Handle exceptions gracefully in production environments

## Setup

### Python Environment Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-example05 .venv
   source .venv/bin/activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the example directory with your credentials:
   ```
   PANW_AI_SEC_API_KEY=your_api_key_here
   # Use either profile name or ID
   DEMO_AI_PROFILE_NAME=your_profile_name
   # Optional: DEMO_AI_PROFILE_ID=your_profile_id
   # Optional: PANW_AI_SEC_API_ENDPOINT=your_custom_endpoint
   ```

## Usage

Run the example script:

```bash
python main.py
```

## Key Concepts

### Decorator Pattern

The decorator pattern is a structural design pattern that:
- Allows behavior to be added to individual objects dynamically
- Wraps functions with additional functionality
- Follows the principle of open for extension, closed for modification

### Security Decorator Implementation

This example implements:
- A `check_user_content` decorator that scans inputs before processing
- Configuration via an AI runtime profile
- Custom error handling with a fallback function
- Debug mode for troubleshooting

### Error Handling

The decorator includes robust error handling:
- Graceful degradation when the API is unavailable
- User-friendly error messages for different failure modes
- Descriptive feedback for common configuration issues
- Optional debug output for troubleshooting

## Sample Output

```
User Input #1: Tell me a joke
Scan response: ScanResponse(scan_id='abc123', report_id='xyz789', tr_id='auto-gen', profile_id='profile123', profile_name='demo_profile', category='none', action='allow', prompt_detected=PromptDetected(url_cats=False, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False))
Action: allow
Is blocked: False
✅ Processing safe input: Tell me a joke

User Input #2: This is a test prompt with 72zf6.rxqfd.com/i8xps1 url
Scan response: ScanResponse(scan_id='def456', report_id='uvw321', tr_id='auto-gen', profile_id='profile123', profile_name='demo_profile', category='security', action='block', prompt_detected=PromptDetected(url_cats=True, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False))
Action: block
Is blocked: True
⚠️ Security alert: Cannot process this input: This is a test prompt with 72zf6.rxqfd.com/i8xps1 url

User Input #3: Here's my bank account 8775664322 and routing number 2344567
Scan response: ScanResponse(scan_id='ghi789', report_id='rst654', tr_id='auto-gen', profile_id='profile123', profile_name='demo_profile', category='dlp', action='block', prompt_detected=PromptDetected(url_cats=False, dlp=True, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False))
Action: block
Is blocked: True
⚠️ Security alert: Cannot process this input: Here's my bank account 8775664322 and routing number 2344567

User Input #4: What's the weather like today?
Scan response: ScanResponse(scan_id='jkl012', report_id='opq987', tr_id='auto-gen', profile_id='profile123', profile_name='demo_profile', category='none', action='allow', prompt_detected=PromptDetected(url_cats=False, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False))
Action: allow
Is blocked: False
✅ Processing safe input: What's the weather like today?
```

This output shows:
1. Normal input being processed after passing security checks
2. Input with a URL being blocked
3. Input with sensitive financial information being blocked
4. Another safe input being processed