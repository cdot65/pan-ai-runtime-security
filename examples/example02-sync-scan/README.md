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
python main.py
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
=== SYNCHRONOUS SCAN AI SECURITY SDK EXAMPLE ===

1. Initializing SDK...
   SDK initialized with endpoint: https://service.api.aisecurity.paloaltonetworks.com

2. Creating scanner...
   Scanner created successfully

3. Setting up AI profile...
   Using profile name: default

4. Creating content for scanning...
   Content created with test data (including malicious URL)

5. Setting up optional metadata...
   Metadata configured

6. Performing synchronous scan...
============================================================
============================================================

7. Detailed scan results:
Scan ID: abc123def456
Report ID: xyz789
Transaction ID: sync-scan-example-001
Category: security
Action: block
Prompt URL Detection: True
Prompt DLP Detection: False
Prompt Injection Detection: False
Response URL Detection: False
Response DLP Detection: False
⚠️ Content blocked
```

In this example output, the scan detected a malicious URL in the prompt (the test domain `72zf6.rxqfd.com/i8xps1`), resulting in the content being blocked. The detailed scan results show which security policies triggered the block action.