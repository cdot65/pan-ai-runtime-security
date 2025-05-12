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
python async_scan.py
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
Creating scanner...
==============================================================
Submitting asynchronous scan request...
==============================================================
Async scan response: AsyncScanResponse(scan_id='abc123', report_id='xyz789')
Scan ID: abc123
Report ID: xyz789
==============================================================
Querying results by scan ID...
==============================================================
Scan by IDs response: QueryByScanIdsResponse(scans=[ScanDetail(scan_id='abc123', scan_status='COMPLETED', created_at='2023-01-01T12:00:00Z', completed_at='2023-01-01T12:00:01Z')])
==============================================================
Querying results by report ID...
==============================================================
Report by IDs response: QueryByReportIdsResponse(reports=[ReportDetail(report_id='xyz789', profile_id='profile123', profile_name='default_profile', report_status='READY', results=[ScanResult(scan_id='abc123', tr_id='tx-001', req_id=1, category='security', action='block', prompt_detected=PromptDetected(url_cats=True, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False))])])
==============================================================
```

In this example output:
1. Two content items are submitted for asynchronous scanning
2. The scan and report IDs are received
3. Results are queried by scan ID to check status
4. Detailed results are obtained by querying the report ID
5. The first content item was blocked due to a malicious URL