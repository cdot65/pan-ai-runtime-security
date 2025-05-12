# Basic AI Security SDK Example

This example demonstrates the basic usage of the Palo Alto Networks AI Security Python SDK, including SDK initialization, setup, and a simple synchronous scan of content for security threats.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
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
   PANW_AI_PROFILE_NAME=your_profile_name
   # Optional: PANW_AI_SEC_API_ENDPOINT=your_custom_endpoint
   ```

## Usage

Run the example script:

```bash
python main.py
```

## Key Concepts

### SDK Initialization

The SDK needs to be initialized with your API key and optionally a custom API endpoint. There are multiple ways to set up the API key:

1. Using an environment variable:
   ```bash
   export PANW_AI_SEC_API_KEY=YOUR_API_KEY_GOES_HERE
   ```

2. Loading dynamically from a secure Secret Store or .env file:
   ```python
   api_key = os.environ.get("PANW_AI_SEC_API_KEY")
   aisecurity.init(api_key=api_key)
   ```

### Content Object

The `Content` object represents the data to be scanned, typically including:
- `prompt`: The user input to an AI system
- `response`: The AI system's response

### Scan Response

The scan response contains detailed information about the security scan:
- `scan_id`: Unique identifier for the scan
- `report_id`: Identifier for the detailed report
- `action`: Whether the content is allowed or blocked
- `prompt_detected`: Security issues detected in the prompt
- `response_detected`: Security issues detected in the response

## Sample Output

```
"Create a new scanner"
"=============================================================="
"Invoke sync scan call"
"=============================================================="
"sync scan response: ScanResponse(scan_id='demo_scan_id', report_id='demo_report_id', tr_id='demo_transaction_id', profile_id='demo_profile_id', profile_name='demo_profile_name', category='demo_category', action='block', prompt_detected=PromptDetected(url_cats=True, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False))"
All required credentials found
"ai_security Example is completed"
```

In the example output, a URL was detected in the prompt, resulting in the content being blocked.