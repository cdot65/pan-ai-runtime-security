# AI Security SDK - Asynchronous Scan Documentation

## Overview

The `async_scan.py` script demonstrates the asynchronous scanning capabilities of the AI Security SDK. This approach enables batch processing of multiple content items and provides methods to query results by scan IDs and report IDs, offering flexibility for applications with higher throughput requirements.

## Script Purpose

This script illustrates:

1. Loading environment variables for SDK configuration
2. Initializing the AI Security SDK with credentials
3. Creating an asynchronous scanner
4. Preparing multiple content items for batch scanning
5. Submitting an asynchronous scan request
6. Querying results using scan IDs and report IDs
7. Processing and interpreting asynchronous scan results

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

### SDK Initialization

The SDK is initialized with the API key and endpoint:

```python
aisecurity.init(api_key=env["api_key"], api_endpoint=env["api_endpoint"])
```

### Scanner Creation

A scanner instance is created to perform asynchronous scan operations:

```python
scanner = Scanner()
```

### AI Profile Configuration

An AI profile is created from environment variables:

```python
ai_profile = AiProfile(profile_name=env["profile_name"])
```

### Content Preparation

Multiple content objects are prepared for scanning:

```python
content1 = Content(
    prompt="This is a test prompt with malicious URL",
    response="This is a test response",
)

content2 = Content(
    prompt="This is another test prompt", response="This is another test response"
)
```

### AsyncScanObjects Configuration

An array of AsyncScanObject instances is created for batch processing:

```python
async_scan_objects = [
    AsyncScanObject(
        req_id=1,  # Request identifier for the first content
        scan_req=ScanRequest(
            tr_id="tx-001",  # Transaction ID
            ai_profile=ai_profile,
            contents=[
                ScanRequestContentsInner(
                    prompt=content1.prompt, response=content1.response
                )
            ],
        ),
    ),
    AsyncScanObject(
        req_id=2,  # Request identifier for the second content
        scan_req=ScanRequest(
            tr_id="tx-002",  # Transaction ID
            ai_profile=ai_profile,
            contents=[
                ScanRequestContentsInner(
                    prompt=content2.prompt, response=content2.response
                )
            ],
        ),
    ),
]
```

### Asynchronous Scan Execution

The asynchronous scan is executed with the prepared AsyncScanObjects:

```python
scan_async_response = scanner.async_scan(async_scan_objects)
```

### Querying Results by IDs

The script demonstrates querying results by scan IDs and report IDs:

```python
# Query scan results by scan ID
scan_by_ids_response = scanner.query_by_scan_ids(
    scan_ids=[scan_async_response.scan_id]
)

# Query scan results by report ID
report_by_ids_response = scanner.query_by_report_ids(
    report_ids=[scan_async_response.report_id]
)
```

## Execution Example

When executed, the script produces output similar to:

```
Creating scanner...
==============================================================
Submitting asynchronous scan request...
==============================================================
"Async scan response: report_id='R8a5e67d2-8f3b-45c9-a31c-734f2dfd9bf8' scan_id='8a5e67d2-8f3b-45c9-a31c-734f2dfd9bf8'"
Scan ID: 8a5e67d2-8f3b-45c9-a31c-734f2dfd9bf8
Report ID: R8a5e67d2-8f3b-45c9-a31c-734f2dfd9bf8
==============================================================
Querying results by scan ID...
==============================================================
"Scan by IDs response: [ScanObjectWithSummary(scan_id='8a5e67d2-8f3b-45c9-a31c-734f2dfd9bf8', report_id='R8a5e67d2-8f3b-45c9-a31c-734f2dfd9bf8', req_id=1, tr_id='tx-001', profile_id='f3947659-ff4e-4355-b45b-ad6e20d02138', profile_name='test123', category='malicious', action='block', prompt_detected=PromptDetected(url_cats=True, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False), created_at=None, completed_at=None), ScanObjectWithSummary(scan_id='8a5e67d2-8f3b-45c9-a31c-734f2dfd9bf8', report_id='R8a5e67d2-8f3b-45c9-a31c-734f2dfd9bf8', req_id=2, tr_id='tx-002', profile_id='f3947659-ff4e-4355-b45b-ad6e20d02138', profile_name='test123', category='safe', action='allow', prompt_detected=PromptDetected(url_cats=False, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False), created_at=None, completed_at=None)]"
==============================================================
Querying results by report ID...
==============================================================
"Report by IDs response: [ScanObjectWithSummary(scan_id='8a5e67d2-8f3b-45c9-a31c-734f2dfd9bf8', report_id='R8a5e67d2-8f3b-45c9-a31c-734f2dfd9bf8', req_id=1, tr_id='tx-001', profile_id='f3947659-ff4e-4355-b45b-ad6e20d02138', profile_name='test123', category='malicious', action='block', prompt_detected=PromptDetected(url_cats=True, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False), created_at=None, completed_at=None), ScanObjectWithSummary(scan_id='8a5e67d2-8f3b-45c9-a31c-734f2dfd9bf8', report_id='R8a5e67d2-8f3b-45c9-a31c-734f2dfd9bf8', req_id=2, tr_id='tx-002', profile_id='f3947659-ff4e-4355-b45b-ad6e20d02138', profile_name='test123', category='safe', action='allow', prompt_detected=PromptDetected(url_cats=False, dlp=False, injection=False), response_detected=ResponseDetected(url_cats=False, dlp=False), created_at=None, completed_at=None)]"
==============================================================
```

## Response Explanation

The asynchronous scan response returns IDs that can be used to query detailed results:

- **report_id**: Unique identifier for the scan report
- **scan_id**: Unique identifier for the scan operation

When querying by these IDs, each content item's detailed scan results are returned:

- **req_id**: The request identifier provided in the AsyncScanObject
- **tr_id**: Transaction ID for correlation
- **profile_id/profile_name**: Identifies the AI security profile used
- **category**: Classification of the content (e.g., "malicious" or "safe")
- **action**: Recommended action ("block" or "allow")
- **prompt_detected**: Details about security issues found in the prompt:
  - **url_cats**: Whether URLs were detected
  - **dlp**: Whether Data Loss Prevention issues were detected
  - **injection**: Whether prompt injection was detected
- **response_detected**: Details about security issues in the response

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
   python async_scan.py
   ```

3. Review the scan results to understand the security evaluation of your content.

## Use Cases and Benefits

The asynchronous scanning approach is ideal for:

1. **Batch Processing**: Submit multiple content items in a single request
2. **High-Volume Applications**: Scale to handle large numbers of scan requests
3. **Non-Blocking Operations**: Continue application flow while scans are processed
4. **Flexible Result Retrieval**: Query results when needed using scan or report IDs

This pattern is especially useful for applications that process a high volume of AI content and need to optimize for throughput rather than lowest latency.