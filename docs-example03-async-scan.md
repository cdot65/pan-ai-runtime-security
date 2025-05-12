# AI Security SDK - Asynchronous Scan Documentation

## Overview

The asynchronous scan example demonstrates how to use the Palo Alto Networks AI Security SDK to submit multiple content items for scanning and retrieve results. This example is located in `examples/example03-async-scan/` and contains the necessary files to run a standalone asynchronous scan demonstration.

## Example Purpose

This example illustrates:

1. Loading environment variables for configuration
2. Initializing the AI Security SDK with proper credentials
3. Creating and configuring an AI security scanner
4. Preparing multiple content items for batch scanning
5. Submitting an asynchronous scan request
6. Querying scan status by scan ID
7. Retrieving detailed scan results by report ID
8. Processing and interpreting batch scan results

## Key Components

### Environment Configuration

The example loads environment variables from a .env file, looking in both the current directory and the script's directory:

```python
def load_environment() -> dict[str, str | None]:
    """
    Load environment variables from .env file

    Returns:
        dict: Environment configuration including API credentials
    """
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
            print("Please copy .env.example to .env and add your credentials")
            sys.exit(1)
```

### SDK Initialization

The SDK is initialized with the provided API key and endpoint:

```python
# Initialize the SDK with the API key and endpoint
aisecurity.init(api_key=env["api_key"], api_endpoint=env["api_endpoint"])
```

### Logging Configuration

Logging is configured based on the environment variable:

```python
# Configure logging based on environment variable
logging.basicConfig(level=getattr(logging, env["log_level"]))
```

### Scanner Creation

A scanner instance is created to perform the security evaluation:

```python
# Create the scanner instance
scanner = Scanner()
```

### AI Profile Configuration

An AI profile is created using either the profile ID or profile name from environment variables:

```python
# Create an AI profile with environment variables
if env["profile_id"]:
    ai_profile = AiProfile(profile_id=env["profile_id"])
else:
    ai_profile = AiProfile(profile_name=env["profile_name"])
```

### Content Preparation

Multiple content items are prepared for batch scanning:

```python
# Create sample content objects
content1 = Content(
    prompt="This is a test prompt with 72zf6.rxqfd.com/i8xps1 URL that should be detected",
    response="This is a test response for the first item",
)

content2 = Content(
    prompt="This is another test prompt without any malicious content",
    response="This is another test response for the second item"
)
```

### AsyncScanObject Creation

Async scan objects are created to hold the batch requests:

```python
# Prepare async scan objects for batch processing
async_scan_objects = [
    AsyncScanObject(
        req_id=1,  # Request identifier for the first content
        scan_req=ScanRequest(
            tr_id="async-tx-001",  # Transaction ID
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
            tr_id="async-tx-002",  # Transaction ID
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

### Asynchronous Scan Submission

The batch of content items is submitted for asynchronous scanning:

```python
# Submit the asynchronous scan request
scan_async_response = scanner.async_scan(async_scan_objects)
```

### Querying Scan Status

The scan status is queried using the scan ID, with a retry mechanism to handle cases where the scan might not be completed immediately:

```python
# Initialize retry variables
max_retries = 3
retry_count = 0
retry_wait = 10  # seconds
scan_completed = False
scan_by_ids_response = None

while retry_count < max_retries and not scan_completed:
    if retry_count > 0:
        print(f"Waiting {retry_wait} seconds before retry {retry_count}/{max_retries-1}...")
        time.sleep(retry_wait)
        print("Retrying query for scan status...")

    # Query scan results by scan ID
    scan_by_ids_response = scanner.query_by_scan_ids(
        scan_ids=[scan_async_response.scan_id]
    )

    # Check if any scan is completed
    for scan in scan_by_ids_response:
        if hasattr(scan, 'scan_status') and scan.scan_status == "COMPLETED":
            scan_completed = True
            break

    retry_count += 1
```

### Retrieving Scan Results

Detailed scan results are retrieved using the report ID, with a retry mechanism to handle cases where results might not be immediately available:

```python
# Initialize retry variables
max_retries = 3
retry_count = 0
retry_wait = 10  # seconds
has_results = False
report_by_ids_response = None

while retry_count < max_retries and not has_results:
    if retry_count > 0:
        print(f"Waiting {retry_wait} seconds before retry {retry_count}/{max_retries-1}...")
        time.sleep(retry_wait)
        print("Retrying query for report results...")

    # Query scan results by report ID
    report_by_ids_response = scanner.query_by_report_ids(
        report_ids=[scan_async_response.report_id]
    )

    # Check if any report has results
    reports = report_by_ids_response.reports if hasattr(report_by_ids_response, 'reports') else report_by_ids_response
    for report in reports:
        if hasattr(report, 'results') and report.results:
            has_results = True
            break

    retry_count += 1
```

### Result Processing

The example processes and displays the detailed scan results for each item in the batch:

```python
# Print report query response details
print("\n   Report Details:")
for report in report_by_ids_response.reports:
    print(f"   - Report ID: {report.report_id}")
    print(f"   - Profile: {report.profile_name}")
    print(f"   - Status: {report.report_status}")
    
    # Display results for each request in the batch
    print("\n   Individual Scan Results:")
    for result in report.results:
        print(f"   Request ID: {result.req_id}, Transaction ID: {result.tr_id}")
        print(f"   Category: {result.category}, Action: {result.action}")
        
        # Show detection details
        if hasattr(result, 'prompt_detected'):
            if hasattr(result.prompt_detected, 'url_cats'):
                print(f"   Prompt URL Detection: {result.prompt_detected.url_cats}")
            if hasattr(result.prompt_detected, 'dlp'):
                print(f"   Prompt DLP Detection: {result.prompt_detected.dlp}")
            if hasattr(result.prompt_detected, 'injection'):
                print(f"   Prompt Injection Detection: {result.prompt_detected.injection}")
```

## Execution Example

When executed, the example produces output similar to:

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

## Asynchronous Scan Response Structure

The asynchronous scan workflow involves several response structures:

### 1. Initial Submission Response

The `async_scan` method returns an AsyncScanResponse containing:
- **scan_id**: Unique identifier for the scan operation
- **report_id**: Unique identifier for the report generated from the scan

### 2. Scan Status Query Response

The `query_by_scan_ids` method returns a list of ScanDetail objects, each including:
  - **scan_id**: The scan's unique identifier
  - **scan_status**: Status of the scan (e.g., "COMPLETED", "PENDING", "PROCESSING")
  - **created_at**: Timestamp when the scan was created
  - **completed_at**: Timestamp when the scan completed (if finished)

### 3. Report Query Response

The `query_by_report_ids` method returns a list of ReportDetail objects, each including:
  - **report_id**: The report's unique identifier
  - **profile_id**: The AI security profile ID used
  - **profile_name**: The AI security profile name
  - **report_status**: Status of the report (e.g., "READY")
  - **results**: An array of ScanResult objects, each including:
    - **scan_id**: The scan's unique identifier
    - **tr_id**: Transaction ID for correlation
    - **req_id**: Request ID from the client
    - **category**: Classification of the detected issue (e.g., "security")
    - **action**: Recommended action ("block" or "allow")
    - **prompt_detected**: Details about security issues found in the prompt
    - **response_detected**: Details about security issues found in the response

## Usage Instructions

To run the example:

1. Navigate to the example directory:
   ```bash
   cd examples/example03-async-scan
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-example03 .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API credentials:
   ```
   PANW_AI_SEC_API_KEY=your_api_key_here
   PANW_AI_PROFILE_NAME=your_profile_name
   # Optional: PANW_AI_PROFILE_ID=your_profile_id
   # Optional: PANW_AI_SEC_API_ENDPOINT=your_custom_endpoint
   # Optional: LOG_LEVEL=DEBUG
   ```

5. Execute the example:
   ```bash
   python main.py
   ```

6. Review the scan results to understand how asynchronous batch scanning works.

## Asynchronous Scanning Benefits

The asynchronous scanning approach is ideal when:

1. You need to process multiple content items efficiently
2. You want to avoid blocking your application while scans complete
3. You need to scan a large volume of content
4. You prefer a job submission model with later result retrieval

This example demonstrates using request IDs to correlate results with original content, allowing you to track which items in a batch were flagged for security concerns.

## Key Differences from Synchronous Scanning

Asynchronous scanning (using `async_scan`) differs from synchronous scanning in the following ways:

1. **Non-Blocking Operation**: It returns immediately with IDs rather than waiting for results
2. **Batch Processing**: It can efficiently process multiple items in a single request
3. **Two-Phase Results**: Requires a separate query to retrieve results after submission
4. **Status Checking**: Allows checking processing status before retrieving results
5. **Request Correlation**: Uses request IDs to correlate results with original content
6. **Retry Mechanism**: Requires implementing retries to handle cases where results aren't immediately available

This example implements a retry mechanism with configurable parameters:
- Maximum number of retries (3 by default)
- Wait time between retries (10 seconds by default)
- Condition checks to determine if results are available

For simpler use cases where immediate results are needed for a single content item, consider the synchronous scanning example instead.