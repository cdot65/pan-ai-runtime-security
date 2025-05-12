# Asyncio Concurrent SDK Example

This example demonstrates how to use asyncio for concurrent operations with the Palo Alto Networks AI Security SDK for improved performance.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Key Concepts](#key-concepts)
- [Sample Output](#sample-output)

## Overview

This example shows how to:
- Use Python's asyncio library with the AI Security SDK
- Run multiple security scans concurrently
- Perform both synchronous and asynchronous scans in parallel
- Query scan results asynchronously
- Properly manage resources with async context managers

## Setup

### Python Environment Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-example04 .venv
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
python asyncio_concurrent.py
```

## Key Concepts

### Asyncio Integration

The AI Security SDK provides a dedicated `asyncio.scanner` implementation that supports:
- Asynchronous operations with `async/await` syntax
- Concurrent processing of multiple security scans
- Non-blocking I/O for improved performance

### Concurrent Operations

This example demonstrates:
- Running a sync_scan and async_scan concurrently using `asyncio.gather()`
- Waiting for all operations to complete
- Processing results from multiple concurrent operations
- Measuring latency of asynchronous operations

### Resource Management

Important aspects of resource management include:
- Using the `await scanner.close()` method to clean up resources
- Proper exception handling in async contexts
- Using asyncio's event loop with `asyncio.run()`

## Sample Output

```
Executing concurrent operations...
==============================================================
Sync scan response:
ScanResponse(scan_id='abc123', report_id='xyz789', tr_id='1234', profile_id='profile123', profile_name='demo_profile', category='security', action='block', prompt_detected=PromptDetected(url_cats=True, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False))
==============================================================
Async scan response:
AsyncScanResponse(scan_id='def456', report_id='uvw321')
==============================================================
Scan by IDs response [latency 234 ms]:
QueryByScanIdsResponse(scans=[ScanDetail(scan_id='def456', scan_status='COMPLETED', created_at='2023-01-01T12:00:00Z', completed_at='2023-01-01T12:00:01Z')])
==============================================================
Report by IDs response [latency 156 ms]:
QueryByReportIdsResponse(reports=[ReportDetail(report_id='uvw321', profile_id='profile123', profile_name='demo_profile', report_status='READY', results=[ScanResult(scan_id='def456', tr_id='tx-001', req_id=1, category='security', action='block', prompt_detected=PromptDetected(url_cats=True, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False))])])
==============================================================
AI Security concurrent scanning example completed successfully
```

This output shows:
1. A synchronous scan and asynchronous scan running concurrently
2. Results from both operations
3. Additional queries for scan and report details with latency measurements
4. Successful resource cleanup and completion