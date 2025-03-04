# AI Security SDK Documentation

This repository contains example scripts and documentation for working with the AI Security SDK, which helps secure AI applications by scanning prompts and responses for potential security issues.

## Documentation Files

This project contains detailed documentation for each script:

- [Main Script](docs-main.md) - Basic SDK functionality and synchronous scanning
- [Synchronous Scan](docs-sync-scan.md) - Detailed examples of synchronous content scanning
- [Asynchronous Scan](docs-async-scan.md) - Batch processing with asynchronous scanning
- [Asyncio Concurrent](docs-asyncio-concurrent.md) - Using asyncio for concurrent operations
- [Decorator Pattern](docs-decorator-example.md) - Implementing security scanning as decorators
- [Mock Implementation](docs-mock-example.md) - Testing with mock implementations
- [Utilities](docs-utils.md) - Helper functions and utilities

## Scripts Overview

| Script | Description |
|--------|-------------|
| `main.py` | Basic example showing how to initialize the SDK and perform a scan |
| `sync_scan.py` | Demonstrates synchronous scanning of content |
| `async_scan.py` | Shows how to use asynchronous scanning for batch processing |
| `asyncio_concurrent.py` | Uses asyncio for concurrent operations with the SDK |
| `decorator_example.py` | Implements a decorator pattern for adding scanning to existing functions |
| `mock_example.py` | Provides a mock implementation for testing without API credentials |
| `utils.py` | Utility functions for working with the SDK |

## Prerequisites

* AI Runtime Security API Key
* AI Runtime Security API AI Profile Name or AI Profile ID
* CPython >= 3.9 (>= 3.10 recommended)
* AI Runtime Security API Endpoint (optional)

## Installation

1. Create a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-api-sdk-${USER} .venv && source .venv/bin/activate
   ```

2. Install the package:
   ```bash
   python3 -m pip install "aisecurity >= 1.0, < 2.0"
   ```

3. Create a `.env` file with your credentials:
   ```
   PANW_AI_SEC_API_KEY=your_api_key_here
   PANW_AI_PROFILE_NAME=your_profile_name
   PANW_AI_SEC_API_ENDPOINT=your_endpoint_or_leave_for_default
   ```

## Running Examples

Run any of the example scripts to see them in action:

```bash
python main.py
python sync_scan.py
python async_scan.py
python asyncio_concurrent.py
python decorator_example.py
python mock_example.py
```

## Key SDK Features

- **Content Scanning**: Detect security issues in AI prompt-response pairs
- **URL Detection**: Identify potentially malicious URLs in content
- **Data Loss Prevention (DLP)**: Detect sensitive information in content
- **Prompt Injection Detection**: Identify attempts to manipulate AI systems
- **Synchronous & Asynchronous APIs**: Choose the API that fits your workflow
- **Batch Processing**: Process multiple items efficiently

## SDK Configuration

### SDK Initialization

The aisecurity.init() function accepts the following parameters:

```python
api_key (required): Provide your API key through configuration or an environment variable.
api_endpoint (optional): Default value is "https://service.api.aisecurity.paloaltonetworks.com"
num_retries (optional): Default value is 5.
```

### Setting up the API Key

There are two ways to set up your API key:

1. Using an environment variable:
```bash
export PANW_AI_SEC_API_KEY=YOUR_API_KEY_GOES_HERE
```

2. Load the API key through init by passing api_key as a parameter:
```python
aisecurity.init(api_key="YOUR_API_KEY_GOES_HERE")
```

### Customizing the API Endpoint

You can set a custom API endpoint using the api_endpoint parameter:
```python
aisecurity.init(api_endpoint="https://api.example.com")
```

### Profile Configuration

Either the Profile name or Profile ID is sufficient:
```python
# Using profile name (loads latest profile)
ai_profile = AiProfile(profile_name="your_profile_name")

# Or using profile ID (loads specific profile version)
ai_profile = AiProfile(profile_id="your_profile_id")
```

## Usage Patterns

The SDK supports several integration patterns:

1. **Direct Synchronous Integration**: Use `sync_scan.py` as a reference
2. **Batch Asynchronous Processing**: See `async_scan.py` for batch processing
3. **Concurrent Processing**: Use `asyncio_concurrent.py` for concurrent operations
4. **Decorator Pattern**: Apply the decorator in `decorator_example.py` to existing functions
5. **Mock Testing**: Use `mock_example.py` for testing without API credentials

## Error Handling

The SDK defines several error types:
- `AISEC_SERVER_SIDE_ERROR`: Errors returned by the API server
- `AISEC_CLIENT_SIDE_ERROR`: Errors that occur on the client side
- `AISEC_USER_REQUEST_PAYLOAD_ERROR`: Errors related to the user's request payload
- `AISEC_MISSING_VARIABLE`: Errors related to missing variables
- `AISEC_SDK_ERROR`: Other generic errors that occur in the SDK

## Retry Configuration

The SDK supports configurable retries:

```python
import aisecurity
aisecurity.init(num_retries=5)
```

Note that retries are only performed for query operations (query_by_scan_ids and query_by_report_ids), not for sync_scan and async_scan operations as they are POST requests.

For detailed examples and more information, refer to the documentation files linked above.# pan-ai-runtime-security
