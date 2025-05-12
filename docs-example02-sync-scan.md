# AI Security SDK - Synchronous Scan Documentation

## Overview

The synchronous scan example demonstrates how to use the Palo Alto Networks AI Security SDK to evaluate content against security policies in a synchronous (request-response) manner. This example is located in `examples/example02-sync-scan/` and contains the necessary files to run a standalone synchronous scan demonstration.

## Example Purpose

This example illustrates:

1. Loading environment variables for configuration
2. Initializing the AI Security SDK with proper credentials
3. Creating and configuring an AI security scanner
4. Defining content to be evaluated for security risks
5. Executing a synchronous scan operation
6. Interpreting detailed scan results

## Key Components

### Environment Configuration

The example loads environment variables from a .env file, looking in both the current directory and the script's directory:

```python
def load_environment() -> Dict[str, Optional[str]]:
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

### API Credentials

The example retrieves required API credentials from environment variables:

```python
# Get credentials from environment variables with fallbacks
api_key = os.environ.get("PANW_AI_SEC_API_KEY", None)
api_endpoint = os.environ.get(
    "PANW_AI_SEC_API_ENDPOINT", 
    "https://service.api.aisecurity.paloaltonetworks.com"
)
profile_name = os.environ.get("PANW_AI_PROFILE_NAME", None)
profile_id = os.environ.get("PANW_AI_PROFILE_ID", None)
log_level = os.environ.get("LOG_LEVEL", "INFO")
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

Content to be scanned is prepared, including a test prompt containing a malicious URL:

```python
# Create a content object with test data containing a malicious URL
content = Content(
    prompt="This is a test prompt with 72zf6.rxqfd.com/i8xps1 URL that should be detected",
    response="This is a test response without any malicious content",
)
```

### Metadata Configuration

Optional metadata is configured to provide context for the scan:

```python
# Optional parameters for the scan API
tr_id = "sync-scan-example-001"  # Transaction ID for correlation
metadata = Metadata(
    app_name="ai_security_sync_example", 
    app_user="example_user", 
    ai_model="example_model"
)
```

### Scan Execution

The synchronous scan is executed with the prepared AI profile, content, and optional metadata:

```python
# Perform the synchronous scan with all parameters
scan_response = scanner.sync_scan(
    ai_profile=ai_profile, 
    content=content, 
    tr_id=tr_id, 
    metadata=metadata
)
```

### Result Processing

The example processes and displays the detailed scan results:

```python
# Print detailed scan results
print_detailed_scan_result(scan_response)
```

The `print_detailed_scan_result` function provides a comprehensive view of the scan results:

```python
def print_detailed_scan_result(scan_response: Any) -> None:
    """
    Print a detailed summary of scan results

    Args:
        scan_response: The response from a security scan
    """
    try:
        print(f"Scan ID: {scan_response.scan_id}")
        print(f"Report ID: {scan_response.report_id}")
        print(f"Transaction ID: {scan_response.tr_id}")
        print(f"Category: {scan_response.category}")
        print(f"Action: {scan_response.action}")

        # Detailed detection information
        if hasattr(scan_response, "prompt_detected"):
            if hasattr(scan_response.prompt_detected, "url_cats"):
                print(f"Prompt URL Detection: {scan_response.prompt_detected.url_cats}")
            if hasattr(scan_response.prompt_detected, "dlp"):
                print(f"Prompt DLP Detection: {scan_response.prompt_detected.dlp}")
            if hasattr(scan_response.prompt_detected, "injection"):
                print(f"Prompt Injection Detection: {scan_response.prompt_detected.injection}")

        if hasattr(scan_response, "response_detected"):
            if hasattr(scan_response.response_detected, "url_cats"):
                print(f"Response URL Detection: {scan_response.response_detected.url_cats}")
            if hasattr(scan_response.response_detected, "dlp"):
                print(f"Response DLP Detection: {scan_response.response_detected.dlp}")

        # Print action summary
        if scan_response.action == "allow":
            print("✅ Content allowed")
        else:
            print("⚠️ Content blocked")
            
    except AttributeError as e:
        print(f"Error accessing scan response attribute: {e}")
    except Exception as e:
        print(f"Error printing scan result: {e}")
```

## Execution Example

When executed, the example produces output similar to:

```
=== SYNCHRONOUS SCAN AI SECURITY SDK EXAMPLE ===

1. Initializing SDK...
   SDK initialized with endpoint: https://service.api.aisecurity.paloaltonetworks.com

2. Creating scanner...
   Scanner created successfully

3. Setting up AI profile...
   Using profile name: default_profile

4. Creating content for scanning...
   Content created with test data (including malicious URL)

5. Setting up optional metadata...
   Metadata configured

6. Performing synchronous scan...
============================================================
============================================================

7. Detailed scan results:
Scan ID: ad781bcf-a5f3-4c09-9f14-e46d8c7a99b1
Report ID: 93c850ab-cf71-4e45-942a-b75e1f23d1c6
Transaction ID: sync-scan-example-001
Category: security
Action: block
Prompt URL Detection: True
Prompt DLP Detection: False
Prompt Injection Detection: False
Response URL Detection: False
Response DLP Detection: False
⚠️ Content blocked

=== EXAMPLE COMPLETED ===
```

## Response Explanation

The synchronous scan response contains detailed information:

- **scan_id**: Unique identifier for the scan operation
- **report_id**: Unique identifier for the scan report
- **tr_id**: Transaction ID used for correlation
- **category**: Classification of the detected issue (e.g., "security")
- **action**: Recommended action ("block" or "allow")
- **prompt_detected**: Details about security issues found in the prompt:
  - **url_cats**: Whether malicious URLs were detected
  - **dlp**: Whether Data Loss Prevention issues were detected
  - **injection**: Whether prompt injection was detected
- **response_detected**: Details about security issues in the response

## Usage Instructions

To run the example:

1. Navigate to the example directory:
   ```bash
   cd examples/example02-sync-scan
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-example02 .venv
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

6. Review the scan results to understand if the AI content is secure or requires attention.

## Security Implications

The synchronous scanning approach is ideal when:

1. You need immediate feedback on AI content before proceeding
2. You want to block potentially harmful content in real-time
3. The scanning latency is acceptable for your application's user experience

The example demonstrates detecting URLs in prompts, which could be malicious links or attempts to bypass security measures.

## Key Differences from Other Scan Methods

Synchronous scanning (using `sync_scan`) differs from other scanning methods in the following ways:

1. **Blocking Operation**: It waits for the scan to complete before returning a result
2. **Immediate Response**: Results are available immediately in the response
3. **Single Request/Response**: No need for callbacks or polling
4. **Simple Integration**: Easier to integrate but adds latency to the main execution flow

For use cases that require lower latency, consider the asynchronous scanning examples.