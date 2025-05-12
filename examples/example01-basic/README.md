# Basic AI Security SDK Example

This example demonstrates the basic usage of the Palo Alto Networks AI Security Python SDK, including SDK initialization, setup, and a simple synchronous scan of content for security threats.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Code Walkthrough](#code-walkthrough)
- [Key Concepts](#key-concepts)
- [Sample Output](#sample-output)

## Overview

This example shows how to:
- Initialize the AI Security SDK with proper credentials
- Create a scanner instance
- Set up an AI profile
- Perform a basic synchronous scan
- Interpret scan results

## Setup

### Python Environment Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-example01 .venv
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
   PANW_AI_PROFILE_NAME=your_profile_name
   # Optional: PANW_AI_PROFILE_ID=your_profile_id
   # Optional: PANW_AI_SEC_API_ENDPOINT=your_custom_endpoint
   ```

## Usage

Run the example script:

```bash
python main.py
```

## Code Walkthrough

The example script demonstrates the following steps:

1. **Environment Setup**: Load API key and other configuration from environment variables
   ```python
   env = load_environment()
   ```

2. **SDK Initialization**: Initialize the SDK with your API key and endpoint
   ```python
   aisecurity.init(
       api_key=env["api_key"],
       api_endpoint=env["api_endpoint"]
   )
   ```

3. **Scanner Creation**: Create a scanner instance
   ```python
   scanner = Scanner()
   ```

4. **AI Profile Setup**: Create an AI profile using name or ID
   ```python
   ai_profile = AiProfile(profile_name=env["profile_name"])
   ```

5. **Content Creation**: Create a content object with test data
   ```python
   content = Content(
       prompt="This is a test prompt with 72zf6.rxqfd.com/i8xps1 URL",
       response="This is a test response",
   )
   ```

6. **Metadata Setup**: Configure optional metadata for the scan
   ```python
   tr_id = "example-tx-001"
   metadata = Metadata(
       app_name="basic_example",
       app_user="example_user",
       ai_model="example_model"
   )
   ```

7. **Perform Scan**: Execute the synchronous scan
   ```python
   scan_response = scanner.sync_scan(
       ai_profile=ai_profile,
       content=content,
       tr_id=tr_id,
       metadata=metadata
   )
   ```

8. **Process Results**: Analyze and display the scan results
   ```python
   print_scan_result_summary(scan_response)
   ```

## Key Concepts

### SDK Initialization

The SDK needs to be initialized with your API key and optionally a custom API endpoint:

```python
aisecurity.init(
    api_key="your_api_key_here",
    api_endpoint="https://service.api.aisecurity.paloaltonetworks.com"
)
```

### AI Profile

The AI Profile defines the security policies to apply during scanning. You can specify either a profile name or ID:

```python
# Using profile name
ai_profile = AiProfile(profile_name="your_profile_name")

# Or using profile ID
ai_profile = AiProfile(profile_id="your_profile_id")
```

### Content Object

The `Content` object represents the data to be scanned, typically including:
- `prompt`: The user input to an AI system
- `response`: The AI system's response

### Metadata

Optional metadata provides context for the scan:
- `app_name`: The name of your application
- `app_user`: The user interacting with your application
- `ai_model`: The AI model being used

### Scan Response

The scan response contains detailed information about the security scan:
- `scan_id`: Unique identifier for the scan
- `report_id`: Identifier for the detailed report
- `action`: Whether the content is allowed or blocked ("allow" or "block")
- `category`: The security category that triggered a block
- `prompt_detected`: Security issues detected in the prompt:
  - `url_cats`: URL categorization issues
  - `dlp`: Data Loss Prevention issues
  - `injection`: Prompt injection attempts
- `response_detected`: Security issues detected in the response:
  - `url_cats`: URL categorization issues
  - `dlp`: Data Loss Prevention issues

## Sample Output

```
=== BASIC AI SECURITY SDK EXAMPLE ===

1. Initializing SDK...
   SDK initialized with endpoint: https://service.api.aisecurity.paloaltonetworks.com

2. Creating scanner...
   Scanner created successfully

3. Setting up AI profile...
   Using profile name: default_profile

4. Creating content for scanning...
   Content created with test data

5. Setting up optional metadata...
   Metadata configured

6. Performing synchronous scan...
============================================================
============================================================

7. Scan result summary:
Scan ID: abc123-def456-ghi789
Report ID: jkl012-mno345-pqr678
Transaction ID: example-tx-001
Category: security
Action: block
Prompt detected issues: URL categories
No issues detected in response
⚠️ Content blocked

=== EXAMPLE COMPLETED ===
```

In this example output, a malicious URL was detected in the prompt, resulting in the content being blocked.