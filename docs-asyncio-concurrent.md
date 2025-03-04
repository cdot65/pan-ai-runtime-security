# AI Security SDK - Asyncio Concurrent Scan Documentation

## Overview

The `asyncio_concurrent.py` script demonstrates how to leverage Python's asyncio library to perform concurrent scan operations with the AI Security SDK. This approach maximizes throughput and efficiency by allowing multiple scan operations to run concurrently within the same application.

## Script Purpose

This script illustrates:

1. Loading environment variables for SDK configuration
2. Initializing the AI Security SDK with proper credentials
3. Using the asyncio-enabled Scanner from `aisecurity.scan.asyncio.scanner`
4. Preparing multiple content objects for scanning
5. Executing synchronous and asynchronous scans concurrently using asyncio
6. Querying scan results asynchronously
7. Processing and interpreting the results of concurrent operations

## Key Components

### Environment Configuration

The script begins by loading environment variables from a .env file:

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
```

### API Credentials

Required credentials are retrieved from environment variables:

```python
# Get credentials from environment variables with fallbacks
api_key = os.environ.get("PANW_AI_SEC_API_KEY", None)
api_endpoint = os.environ.get("PANW_AI_SEC_API_ENDPOINT", None)
profile_name = os.environ.get("PANW_AI_PROFILE_NAME", None)
```

### Asyncio Scanner Import

The script imports the asyncio-enabled scanner, which is different from the standard synchronous scanner:

```python
from aisecurity.scan.asyncio.scanner import Scanner  # Note the asyncio.scanner import
```

### Asynchronous Function Definition

The main functionality is encapsulated in an async function:

```python
async def run_concurrent_scans(env):
    """
    Run multiple scan operations concurrently

    Args:
        env (dict): Environment configuration including API credentials
    """
    # Function implementation...
```

### SDK Initialization

The SDK is initialized with the API key and endpoint:

```python
aisecurity.init(api_key=env["api_key"], api_endpoint=env["api_endpoint"])
```

### Asyncio Scanner Creation

An asyncio-enabled scanner instance is created:

```python
ai_security_scanner = Scanner()
```

### AI Profile Configuration

An AI profile is created from environment variables:

```python
ai_profile = AiProfile(profile_name=env["profile_name"])
```

### Content Preparation

Content objects and AsyncScanObjects are prepared for scanning:

```python
# Create content object
content1 = Content(
    prompt="This is a test prompt with 72zf6.rxqfd.com/i8xps1 url",
    response="This is a test response",
)

# Prepare async scan objects
async_scan_objects = [
    AsyncScanObject(
        req_id=1,
        scan_req=ScanRequest(
            tr_id="tx-001",
            ai_profile=ai_profile,
            contents=[
                ScanRequestContentsInner(
                    prompt=content1.prompt, response=content1.response
                )
            ],
        ),
    ),
    # Second AsyncScanObject...
]
```

### Concurrent Execution

The script executes both synchronous and asynchronous scans concurrently:

```python
# Run sync_scan and async_scan concurrently
print("Executing concurrent operations...")
sync_scan_task = ai_security_scanner.sync_scan(
    ai_profile=ai_profile, content=content1, tr_id=tr_id, metadata=metadata
)
async_scan_task = ai_security_scanner.async_scan(async_scan_objects)

# Wait for both tasks to complete
sync_result, async_result = await asyncio.gather(sync_scan_task, async_scan_task)
```

### Concurrent Result Queries

The script demonstrates querying results concurrently if available:

```python
# Query by scan IDs
scan_by_ids_response, query_by_scan_ids_latency = (
    await ai_security_scanner.query_by_scan_ids(scan_ids=[async_result.scan_id])
)

# Query by report IDs
report_by_ids_response, query_by_report_ids_latency = (
    await ai_security_scanner.query_by_report_ids(
        report_ids=[async_result.report_id]
    )
)
```

### Resource Cleanup

The script ensures proper cleanup of resources:

```python
# Clean up resources
await ai_security_scanner.close()
```

### Running the Async Function

The main function runs the async function using asyncio.run():

```python
def main():
    """Main execution function"""
    # Load environment variables
    env = load_environment()

    try:
        # Run the async function in the asyncio event loop
        asyncio.run(run_concurrent_scans(env))
        print("AI Security concurrent scanning example completed successfully")
    except Exception as e:
        print(f"Error: {e}")
```

## Execution Example

When executed, the script produces output similar to:

```
Executing concurrent operations...
==============================================================
Sync scan response:
report_id='R3fe5ca9c-decd-46e0-96df-d4cb2c1ed94c' scan_id='3fe5ca9c-decd-46e0-96df-d4cb2c1ed94c' tr_id='1234' profile_id='f3947659-ff4e-4355-b45b-ad6e20d02138' profile_name='test123' category='malicious' action='block' prompt_detected=PromptDetected(url_cats=True, dlp=False, injection=False) response_detected=ResponseDetected(url_cats=False, dlp=False) created_at=None completed_at=None
==============================================================
Async scan response:
report_id='R1bd81b10-f2ae-4ce2-94a0-ddfa6fd11968' scan_id='1bd81b10-f2ae-4ce2-94a0-ddfa6fd11968'
==============================================================
Scan by IDs response [latency 245 ms]:
[ScanObjectWithSummary(scan_id='1bd81b10-f2ae-4ce2-94a0-ddfa6fd11968', report_id='R1bd81b10-f2ae-4ce2-94a0-ddfa6fd11968', req_id=1, tr_id='tx-001', profile_id='f3947659-ff4e-4355-b45b-ad6e20d02138', profile_name='test123', category='malicious', action='block', prompt_detected=PromptDetected(url_cats=True, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False), created_at=None, completed_at=None), ScanObjectWithSummary(scan_id='1bd81b10-f2ae-4ce2-94a0-ddfa6fd11968', report_id='R1bd81b10-f2ae-4ce2-94a0-ddfa6fd11968', req_id=2, tr_id='tx-002', profile_id='f3947659-ff4e-4355-b45b-ad6e20d02138', profile_name='test123', category='safe', action='allow', prompt_detected=PromptDetected(url_cats=False, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False), created_at=None, completed_at=None)]
==============================================================
Report by IDs response [latency 202 ms]:
[ScanObjectWithSummary(scan_id='1bd81b10-f2ae-4ce2-94a0-ddfa6fd11968', report_id='R1bd81b10-f2ae-4ce2-94a0-ddfa6fd11968', req_id=1, tr_id='tx-001', profile_id='f3947659-ff4e-4355-b45b-ad6e20d02138', profile_name='test123', category='malicious', action='block', prompt_detected=PromptDetected(url_cats=True, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False), created_at=None, completed_at=None), ScanObjectWithSummary(scan_id='1bd81b10-f2ae-4ce2-94a0-ddfa6fd11968', report_id='R1bd81b10-f2ae-4ce2-94a0-ddfa6fd11968', req_id=2, tr_id='tx-002', profile_id='f3947659-ff4e-4355-b45b-ad6e20d02138', profile_name='test123', category='safe', action='allow', prompt_detected=PromptDetected(url_cats=False, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False), created_at=None, completed_at=None)]
==============================================================
AI Security concurrent scanning example completed successfully
```

## Response Explanation

The script demonstrates concurrent execution with both sync and async results:

### Sync Scan Result
- **report_id/scan_id**: Unique identifiers for the scan operation
- **tr_id**: Transaction ID used for correlation
- **profile_id/profile_name**: AI security profile used
- **category**: Classification of the content ("malicious")
- **action**: Recommended action ("block")
- **prompt_detected**: Security issues in the prompt (URL detected)
- **response_detected**: Security issues in the response (none detected)

### Async Scan Result
- Initial response contains just the IDs
- When queried, detailed results for both content items are returned
- First content item (req_id=1) contains a URL and is classified as "malicious"
- Second content item (req_id=2) is classified as "safe"

### Query Performance
The script includes latency measurements for the queries:
- Scan IDs query: 245 ms
- Report IDs query: 202 ms

## Usage Instructions

To run the script:

1. Create a `.env` file with your API credentials:
   ```
   PANW_AI_SEC_API_KEY=your_api_key_here
   PANW_AI_PROFILE_NAME=your_profile_name
   PANW_AI_SEC_API_ENDPOINT=your_endpoint_or_leave_for_default
   ```

2. Execute the script:
   ```bash
   python asyncio_concurrent.py
   ```

3. Review the concurrent operation results to understand the security evaluation.

## Performance Benefits

The asyncio concurrent approach offers several advantages:

1. **Improved Throughput**: Multiple operations run simultaneously
2. **Reduced Latency**: Overall processing time is reduced compared to sequential execution
3. **Efficient Resource Usage**: I/O-bound operations don't block the entire application
4. **Scalability**: Can handle many concurrent operations with controlled resource usage

This pattern is ideal for applications that need to perform multiple scan operations and want to optimize for overall throughput and responsiveness.