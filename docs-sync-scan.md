# AI Security SDK - Synchronous Scan Documentation

## Overview

The `sync_scan.py` script demonstrates the synchronous scanning capabilities of the AI Security SDK. This script shows how to create a scanner instance, prepare content for evaluation, and perform a synchronous security scan, which analyzes AI content for potential security concerns in real-time.

## Script Purpose

This script illustrates:

1. Loading environment variables for configuration
2. Initializing the AI Security SDK with proper credentials
3. Creating and configuring an AI security scanner
4. Defining content to be evaluated for security risks
5. Executing a synchronous scan operation
6. Interpreting detailed scan results

## Key Components

### Environment Configuration

The script begins by loading environment variables from a .env file, looking in both the current directory and the script's directory:

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

The script retrieves required API credentials from environment variables:

```python
# Get credentials from environment variables with fallbacks
api_key = os.environ.get("PANW_AI_SEC_API_KEY", None)
api_endpoint = os.environ.get("PANW_AI_SEC_API_ENDPOINT", None)
profile_name = os.environ.get("PANW_AI_PROFILE_NAME", None)
```

### SDK Initialization

The SDK is initialized with the provided API key and endpoint:

```python
aisecurity.init(api_key=env["api_key"], api_endpoint=env["api_endpoint"])
```

### Scanner Creation

A scanner instance is created to perform the security evaluation:

```python
scanner = Scanner()
```

### AI Profile Configuration

An AI profile is created using the profile name from environment variables:

```python
ai_profile = AiProfile(profile_name=env["profile_name"])
```

### Content Preparation

Content to be scanned is prepared, including a test prompt containing a URL:

```python
content = Content(
    prompt="This is a test prompt with 72zf6.rxqfd.com/i8xps1 url",
    response="This is a test response",
)
```

### Scan Execution

The synchronous scan is executed with the prepared AI profile, content, and optional metadata:

```python
scan_response = scanner.sync_scan(
    ai_profile=ai_profile, content=content, tr_id=tr_id, metadata=metadata
)
```

### Result Processing

The script processes and displays the detailed scan results:

```python
print(f"Scan ID: {scan_response.scan_id}")
print(f"Report ID: {scan_response.report_id}")
print(f"Transaction ID: {scan_response.tr_id}")
print(f"Category: {scan_response.category}")
print(f"Action: {scan_response.action}")
print(
    f"Prompt Detection: URL: {scan_response.prompt_detected.url_cats}, "
    f"DLP: {scan_response.prompt_detected.dlp}, "
    f"Injection: {scan_response.prompt_detected.injection}"
)
print(
    f"Response Detection: URL: {scan_response.response_detected.url_cats}, "
    f"DLP: {scan_response.response_detected.dlp}"
)
```

## Execution Example

When executed, the script produces output similar to:

```
Creating scanner...
==============================================================
Invoking synchronous scan...
==============================================================
("Synchronous scan response: report_id='R288f8177-5de7-45b6-8d68-83f78a80db98' "
 "scan_id='288f8177-5de7-45b6-8d68-83f78a80db98' tr_id='1234' "
 "profile_id='f3947659-ff4e-4355-b45b-ad6e20d02138' profile_name='test123' "
 "category='malicious' action='block' "
 'prompt_detected=PromptDetected(url_cats=True, dlp=False, injection=False) '
 'response_detected=ResponseDetected(url_cats=False, dlp=False) '
 'created_at=None completed_at=None')
==============================================================
Scan ID: 288f8177-5de7-45b6-8d68-83f78a80db98
Report ID: R288f8177-5de7-45b6-8d68-83f78a80db98
Transaction ID: 1234
Category: malicious
Action: block
Prompt Detection: URL: True, DLP: False, Injection: False
Response Detection: URL: False, DLP: False
```

## Response Explanation

The synchronous scan response contains detailed information:

- **report_id**: Unique identifier for the scan report
- **scan_id**: Unique identifier for the scan operation
- **tr_id**: Transaction ID used for correlation (provided as "1234" in this example)
- **profile_id/profile_name**: Identifies the AI security profile used (from environment)
- **category**: Classification of the content ("malicious" in this example)
- **action**: Recommended action ("block" in this example)
- **prompt_detected**: Details about security issues found in the prompt:
  - **url_cats**: Whether URLs were detected (True in this example)
  - **dlp**: Whether Data Loss Prevention issues were detected (False)
  - **injection**: Whether prompt injection was detected (False)
- **response_detected**: Details about security issues in the response (none detected)

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
   python sync_scan.py
   ```

3. Review the scan results to understand if the AI content is secure or requires attention.

## Security Implications

The synchronous scanning approach is ideal when:

1. You need immediate feedback on AI content before proceeding
2. You want to block potentially harmful content in real-time
3. The scanning latency is acceptable for your application's user experience

The script demonstrates detecting URLs in prompts, which could be malicious links or attempts to bypass security measures.