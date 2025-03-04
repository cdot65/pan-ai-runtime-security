# AI Security SDK - Utilities Documentation

## Overview

The `utils.py` file provides utility functions for working with the AI Security SDK. These utilities offer common helper functions that make it easier to use the SDK in applications, including environment loading, credential management, and error handling.

## Script Purpose

This utility module provides:

1. Environment variable loading and configuration management
2. Credential validation and handling
3. Helper functions for SDK initialization
4. Error handling utilities
5. Common patterns for working with the SDK
6. Development and debugging tools

## Key Components

### Environment Loading

The module provides functions to load environment variables from different sources:

```python
def load_environment_from_file(env_file=".env"):
    """Load environment variables from a file"""
    # First try to load from specified path
    if os.path.exists(env_file):
        load_dotenv(dotenv_path=env_file)
        return True
    
    # If not found, try the current directory
    env_path = Path(".") / env_file
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        return True
    
    # If not found, try the script's directory
    script_dir = Path(__file__).parent.absolute()
    env_path = script_dir / env_file
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        return True
    
    return False
```

### Credential Management

Functions for handling and validating API credentials:

```python
def get_credentials():
    """Get credentials from environment variables with validation"""
    # Load environment if not already loaded
    if os.environ.get("PANW_AI_SEC_API_KEY") is None:
        load_environment_from_file()
    
    # Get required credentials
    api_key = os.environ.get("PANW_AI_SEC_API_KEY")
    api_endpoint = os.environ.get(
        "PANW_AI_SEC_API_ENDPOINT",
        "https://service.api.aisecurity.paloaltonetworks.com"
    )
    profile_name = os.environ.get("PANW_AI_PROFILE_NAME")
    
    # Validate required credentials
    if not api_key:
        raise ValueError("Missing required PANW_AI_SEC_API_KEY environment variable")
    
    if not profile_name:
        print("Warning: PANW_AI_PROFILE_NAME not set, using default profile")
    
    return {
        "api_key": api_key,
        "api_endpoint": api_endpoint,
        "profile_name": profile_name,
    }
```

### SDK Initialization

Helper functions for initializing the SDK with proper credentials:

```python
def initialize_sdk():
    """Initialize the AI Security SDK with proper credentials"""
    credentials = get_credentials()
    
    # Initialize the SDK
    aisecurity.init(
        api_key=credentials["api_key"],
        api_endpoint=credentials["api_endpoint"]
    )
    
    return credentials
```

### Content Validation

Utilities for validating content before scanning:

```python
def validate_content(prompt, response=None):
    """
    Validate content before creating a Content object
    
    Args:
        prompt (str): The prompt to validate
        response (str, optional): The response to validate
        
    Returns:
        bool: True if content is valid, False otherwise
    """
    if not prompt or not isinstance(prompt, str):
        print("Error: Prompt must be a non-empty string")
        return False
    
    if response is not None and not isinstance(response, str):
        print("Error: Response must be a string if provided")
        return False
    
    return True
```

### Error Handling

Error handling utilities for working with the SDK:

```python
def safe_scan(scanner, ai_profile, content, tr_id=None, metadata=None):
    """
    Perform a scan with error handling
    
    Args:
        scanner: Scanner instance
        ai_profile: AiProfile instance
        content: Content instance
        tr_id (str, optional): Transaction ID
        metadata (Metadata, optional): Metadata
        
    Returns:
        ScanResponse or None: The scan response or None if an error occurred
    """
    try:
        scan_response = scanner.sync_scan(
            ai_profile=ai_profile,
            content=content,
            tr_id=tr_id,
            metadata=metadata
        )
        return scan_response
    except Exception as e:
        print(f"Error during scan: {e}")
        return None
```

### Development Tools

Utilities for development and debugging:

```python
def print_scan_details(scan_response):
    """Print detailed information about a scan response"""
    if not scan_response:
        print("No scan response available")
        return
    
    print(f"Scan ID: {scan_response.scan_id}")
    print(f"Report ID: {scan_response.report_id}")
    print(f"Transaction ID: {scan_response.tr_id}")
    print(f"Profile: {scan_response.profile_name} ({scan_response.profile_id})")
    print(f"Category: {scan_response.category}")
    print(f"Action: {scan_response.action}")
    
    print("Prompt Detection:")
    print(f"  - URLs: {scan_response.prompt_detected.url_cats}")
    print(f"  - DLP: {scan_response.prompt_detected.dlp}")
    print(f"  - Injection: {scan_response.prompt_detected.injection}")
    
    print("Response Detection:")
    print(f"  - URLs: {scan_response.response_detected.url_cats}")
    print(f"  - DLP: {scan_response.response_detected.dlp}")
```

## Usage Examples

### Basic SDK Initialization

```python
# Import the utilities
from utils import initialize_sdk, get_credentials

# Initialize the SDK
credentials = initialize_sdk()
print(f"SDK initialized with profile: {credentials['profile_name']}")
```

### Using Safe Scan

```python
from utils import initialize_sdk, safe_scan
from aisecurity.generated_openapi_client.models.ai_profile import AiProfile
from aisecurity.scan.models.content import Content
from aisecurity.scan.sync.scanner import Scanner

# Initialize SDK
credentials = initialize_sdk()

# Create scanner and profile
scanner = Scanner()
ai_profile = AiProfile(profile_name=credentials["profile_name"])

# Create content
content = Content(
    prompt="This is a test prompt",
    response="This is a test response"
)

# Perform safe scan
scan_response = safe_scan(scanner, ai_profile, content)
if scan_response:
    print(f"Scan completed: {scan_response.action}")
else:
    print("Scan failed")
```

### Environment Loading

```python
from utils import load_environment_from_file

# Try to load from a specific file
success = load_environment_from_file("config/.env.dev")
if success:
    print("Loaded environment from custom file")
else:
    print("Could not load environment, using defaults")
```

### Content Validation

```python
from utils import validate_content, initialize_sdk
from aisecurity.scan.models.content import Content

# Initialize SDK
initialize_sdk()

# Validate user input
user_prompt = input("Enter a prompt: ")
if validate_content(user_prompt):
    content = Content(prompt=user_prompt)
    print("Content valid, proceeding with scan...")
else:
    print("Invalid content, cannot proceed with scan")
```

## Implementation Details

### Environment Fallback Logic

The environment loading functions prioritize sources in this order:
1. Specified file path
2. Current directory
3. Script directory

This provides flexibility for different deployment environments.

### Error Handling Strategy

The `safe_scan` function demonstrates a robust error handling approach:

```python
try:
    scan_response = scanner.sync_scan(...)
    return scan_response
except Exception as e:
    print(f"Error during scan: {e}")
    return None
```

This pattern allows calling code to easily check for errors without needing to handle exceptions directly.

## Usage Instructions

To use the utilities in your own scripts:

1. Import the required utility functions:
   ```python
   from utils import initialize_sdk, safe_scan, print_scan_details
   ```

2. Use them in your application:
   ```python
   # Initialize SDK
   credentials = initialize_sdk()
   
   # Create scanner, profile, content...
   
   # Perform safe scan
   result = safe_scan(scanner, profile, content)
   
   # Print detailed results
   print_scan_details(result)
   ```

## Benefits of the Utilities Module

1. **Code Reuse**: Common patterns are abstracted into reusable functions
2. **Error Handling**: Consistent error handling across your application
3. **Configuration Management**: Centralized environment and credential management
4. **Development Support**: Helper functions for debugging and development
5. **Reduced Boilerplate**: Less repetitive code in your application

These utilities can significantly simplify working with the AI Security SDK by providing consistent patterns for common tasks.