# Asynchronous Scan Example

This example demonstrates how to use the asynchronous scan functionality in the Palo Alto Networks AI Security SDK to submit multiple content items for scanning and retrieve results.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Key Concepts](#key-concepts)
- [Sample Output](#sample-output)

## Overview

This example shows how to:
- Initialize the SDK with environment variables
- Submit multiple content items in a single batch for asynchronous scanning
- Query scan results by scan ID
- Query scan results by report ID
- Process and interpret asynchronous scan results

## Setup

### Python Environment Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-example03 .venv
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

### Asynchronous Scanning

Asynchronous scanning involves:
1. Submitting content for background processing
2. Getting a scan ID and report ID
3. Querying results using those IDs when processing is complete

This is ideal for:
- Batch processing multiple content items
- Processing large volumes of content
- Non-blocking workflows

### AsyncScanObject

The `AsyncScanObject` is a container for batch requests with:
- `req_id`: A client-assigned identifier for the request
- `scan_req`: A `ScanRequest` object containing:
  - `tr_id`: Transaction ID for tracking
  - `ai_profile`: The security profile to apply
  - `contents`: Array of content items to scan

### Query Methods

Two methods are available to retrieve results:
- `query_by_scan_ids`: Get details about scan operations
- `query_by_report_ids`: Get comprehensive security reports

## Sample Output

```
=== ASYNCHRONOUS SCAN AI SECURITY SDK EXAMPLE ===

1. Initializing SDK...
   SDK initialized with endpoint: https://service.api.aisecurity.paloaltonetworks.com

2. Creating scanner...
   Scanner created successfully

3. Setting up AI profile...
   Using profile name: default_profile

4. Creating content for batch scanning...
   Created 2 content items for batch processing

5. Preparing async scan objects...
   Prepared 2 async scan objects with unique request IDs

6. Submitting asynchronous scan request...
============================================================
============================================================

7. Async scan submission results:
   Scan ID: 73a481bf-f2e1-4c29-8f24-e56d8c7a66b5
   Report ID: 89c750ab-cf71-4e45-942a-b75e1f23d1c6
   ✅ Async scan request submitted successfully

8. Querying results by scan ID...
============================================================
============================================================

   Scan Status Details:
   - Scan ID: 73a481bf-f2e1-4c29-8f24-e56d8c7a66b5
   - Status: COMPLETED
   - Created: 2023-05-15T14:32:17Z
   - Completed: 2023-05-15T14:32:19Z

9. Querying results by report ID...
============================================================
============================================================

   Report Details:
   - Report ID: 89c750ab-cf71-4e45-942a-b75e1f23d1c6
   - Profile: default_profile
   - Status: READY

   Individual Scan Results:
   Request ID: 1, Transaction ID: async-tx-001
   Category: security, Action: block
   Prompt URL Detection: True
   Prompt DLP Detection: False
   Prompt Injection Detection: False
   Response URL Detection: False
   Response DLP Detection: False
   ⚠️ Content blocked
   ----------------------------------------
   Request ID: 2, Transaction ID: async-tx-002
   Category: none, Action: allow
   Prompt URL Detection: False
   Prompt DLP Detection: False
   Prompt Injection Detection: False
   Response URL Detection: False
   Response DLP Detection: False
   ✅ Content allowed
   ----------------------------------------

=== EXAMPLE COMPLETED ===
```

In this example output:
1. Two content items are submitted for asynchronous scanning:
   - First item contains a malicious URL for testing detection
   - Second item contains safe content
2. The scan and report IDs are received after submission
3. Results are queried by scan ID to check processing status
4. Detailed results are obtained by querying the report ID
5. The first content item was blocked due to the malicious URL
6. The second content item was allowed as it contained no security issues