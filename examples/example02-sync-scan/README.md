# Synchronous Scan Example

This example demonstrates how to use the synchronous scan functionality in the Palo Alto Networks AI Security SDK to evaluate content against security policies.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Key Concepts](#key-concepts)
- [Sample Output](#sample-output)

## Overview

This example shows how to:
- Initialize the SDK with environment variables
- Perform synchronous content scanning
- Get detailed information about security scan results
- Interpret detection flags like URL categories, DLP, and injection detection

## Setup

### Python Environment Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-example02 .venv
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
python sync_scan.py
```

## Key Concepts

### Synchronous Scanning

Synchronous scanning is a request-response model where:
1. You submit content for scanning
2. The system immediately processes the content
3. You receive the scan results in the same response

This is ideal for:
- Single content scanning
- Real-time decision making
- Simple integration patterns

### Scan Request Components

Each scan request includes:
- **AI Profile**: Defines the security policies to apply
- **Content**: The prompt and/or response to scan
- **Transaction ID** (optional): For tracking and correlation
- **Metadata** (optional): Additional context like app name and user

### Scan Results Interpretation

The scan response includes:
- **action**: "allow" or "block" indicating whether the content was approved
- **category**: The security category that triggered a block
- **prompt_detected**: Issues found in the prompt (URL categories, DLP, injection)
- **response_detected**: Issues found in the response (URL categories, DLP)

## Sample Output

```
Creating scanner...
==============================================================
Invoking synchronous scan...
==============================================================
Synchronous scan response: ScanResponse(scan_id='abc123', report_id='xyz789', tr_id='1234', profile_id='profile123', profile_name='default_profile', category='security', action='block', prompt_detected=PromptDetected(url_cats=True, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False))
==============================================================
Scan ID: abc123
Report ID: xyz789
Transaction ID: 1234
Category: security
Action: block
Prompt Detection: URL: True, DLP: False, Injection: False
Response Detection: URL: False, DLP: False
```

In this example output, the scan detected a malicious URL in the prompt, resulting in the content being blocked.