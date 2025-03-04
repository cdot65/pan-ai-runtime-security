# AI Security SDK - Main Script Documentation

## Overview

The `main.py` script serves as the primary entry point for the AI Security SDK. It demonstrates the basic functionality of the SDK by initializing it, creating a scanner, and performing a synchronous scan operation to evaluate AI content against security policies.

## Script Details

The main script demonstrates:

1. How to initialize the AI Security SDK with proper API credentials
2. Creating a scanner instance to perform security evaluations
3. Creating an AI profile and content objects
4. Executing a synchronous scan operation
5. Processing and interpreting the scan results

## Key Components

### Environment Setup

The script loads environment variables from a .env file, searching in both the current and script directories:

```python
# Load default profile name from environment variable
load_dotenv()
```

### SDK Initialization

The SDK is initialized with the API endpoint (either from environment variables or a default):

```python
api_endpoint = os.environ.get(
    "PANW_AI_SEC_API_ENDPOINT",
    "https://service.api.aisecurity.paloaltonetworks.com"
)
aisecurity.init(api_endpoint=api_endpoint)
```

### Scanner Creation

A scanner instance is created to perform security evaluations:

```python
ai_security_example = Scanner()
```

### AI Profile & Content Setup

An AI profile and content objects are created for scanning:

```python
profile_name = os.environ.get("PANW_AI_PROFILE_NAME", None)
ai_profile = AiProfile(profile_name=profile_name)
content1 = Content(
    prompt="This is a tests prompt with 72zf6.rxqfd.com/i8xps1 url",
    response="This is a tests response",
)
```

### Metadata Configuration

Optional metadata is provided to enhance scan context:

```python
tr_id = "1234"  # Optionally Provide unique identifier for correlating transactions.
metadata = Metadata(
    app_name="concurrent_sdk", app_user="user", ai_model="sample_model"
)
```

### Executing the Scan

The sync_scan method is called to perform the security evaluation:

```python
scan_response = ai_security_example.sync_scan(
    ai_profile=ai_profile, content=content1, tr_id=tr_id, metadata=metadata
)
```

### Environment Variable Validation

The script validates that required environment variables are present:

```python
if not all([pan_api_key]):
    missing = []
    if not pan_api_key:
        missing.append("PANW_AI_SEC_API_KEY")

    print(f"Missing required credentials: {', '.join(missing)}")
else:
    print("All required credentials found")
```

## Execution Example

When executed, the script produces output similar to:

```
'Create a new scanner'
'=============================================================='
'Invoke sync scan call'
'=============================================================='
("sync scan response: report_id='Rc9585ec6-3a47-4d9a-81f6-df795cf4a50e' "
 "scan_id='c9585ec6-3a47-4d9a-81f6-df795cf4a50e' tr_id='1234' "
 "profile_id='f3947659-ff4e-4355-b45b-ad6e20d02138' profile_name='test123' "
 "category='malicious' action='block' "
 'prompt_detected=PromptDetected(url_cats=True, dlp=False, injection=False) '
 'response_detected=ResponseDetected(url_cats=False, dlp=False) '
 'created_at=None completed_at=None\n')
All required credentials found
'ai_security Example is completed'
```

## Response Explanation

The scan response contains detailed information:

- **report_id**: Unique identifier for the scan report
- **scan_id**: Unique identifier for the scan operation
- **tr_id**: Transaction ID used for correlation
- **profile_id/profile_name**: Identifies the AI security profile used
- **category**: Classification of the content (e.g., "malicious")
- **action**: Recommended action ("block" or "allow")
- **prompt_detected**: Details about security issues found in the prompt:
  - **url_cats**: Whether URLs were detected (True)
  - **dlp**: Whether Data Loss Prevention issues were detected (False)
  - **injection**: Whether prompt injection was detected (False)
- **response_detected**: Details about security issues in the response

## Usage

To run the script:

1. Create a `.env` file with your API credentials:
   ```
   PANW_AI_SEC_API_KEY=your_api_key_here
   PANW_AI_PROFILE_NAME=your_profile_name
   PANW_AI_SEC_API_ENDPOINT=your_endpoint_or_leave_for_default
   ```

2. Execute the script:
   ```bash
   python main.py
   ```

3. Review the scan results to determine if the content is safe or requires attention.