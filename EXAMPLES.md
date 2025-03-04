# AI Security SDK Examples

This directory contains example scripts demonstrating different methods of using the Palo Alto Networks AI Security Runtime SDK.

## Setup Instructions

1. Create a virtual environment and activate it:
   ```bash
   python3 -m venv --prompt aisec-api-sdk-${USER} .venv 
   source .venv/bin/activate
   ```

2. Set your pip configuration (for internal Palo Alto Networks users):
   ```bash
   python3 -m pip config --user set global.index-url "https://art.code.pan.run/artifactory/api/pypi/pypi.org/simple"
   python3 -m pip config set --site global.extra-index-url "https://art.code.pan.run/artifactory/api/pypi/aisec-api-pypi/simple"
   ```

3. Install the aisecurity package:
   ```bash
   python3 -m pip install "aisecurity >= 1.0, < 2.0"
   ```

4. Copy `.env.example` to `.env` and add your API key and other configuration:
   ```bash
   cp .env.example .env
   # Edit .env with your editor to add credentials
   ```

   **IMPORTANT**: You must add a valid API key to the .env file for these examples to work!
   ```
   PANW_AI_SEC_API_KEY=your_actual_api_key_here
   ```

## Available Examples

### 1. Synchronous Scan (`sync_scan.py`)

Demonstrates how to use the synchronous scan functionality to perform immediate content evaluation.

```bash
python3 sync_scan.py
```

This script:
- Initializes the SDK with your API credentials
- Creates content with test data
- Performs a synchronous scan
- Displays the scan results

### 2. Decorator Pattern (`decorator_example.py`) 

Shows how to use the decorator pattern to automatically scan user inputs before processing them.

```bash
python3 decorator_example.py
```

This script:
- Demonstrates how to create a security decorator
- Tests it with various input examples
- Shows how to handle blocked content

### 3. Asynchronous Scan (`async_scan.py`)

Illustrates how to submit content for asynchronous scanning and retrieve results.

```bash
python3 async_scan.py
```

This script:
- Submits multiple content items for scanning
- Gets scan and report IDs
- Shows how to query results using scan IDs and report IDs

### 4. Asyncio Concurrent Scanning (`asyncio_concurrent.py`)

Shows how to use Python's asyncio for concurrent scanning operations.

```bash
python3 asyncio_concurrent.py
```

This script:
- Uses the asyncio version of the Scanner
- Executes multiple scan operations concurrently
- Measures performance metrics

### 5. Mock Implementation (`mock_example.py`)

Provides a mock implementation to demonstrate how the SDK would work without requiring valid API credentials.

```bash
python3 mock_example.py
```

This script:
- Simulates the behavior of the real SDK
- Shows examples of both synchronous scanning and the decorator pattern
- Can be run without a valid API key

## Environment Variables

All examples use the following environment variables from the `.env` file:

- `PANW_AI_SEC_API_KEY` (required): Your API key
- `PANW_AI_SEC_API_ENDPOINT` (optional): API endpoint URL
- `DEMO_AI_PROFILE_ID` (optional): Profile ID for testing
- `DEMO_AI_PROFILE_NAME` (optional): Profile name for testing

## Troubleshooting

If you encounter "Invalid API Key" errors:
1. Make sure you have set a valid API key in the `.env` file
2. Verify that the key has the proper permissions
3. Check if your API key has expired or been revoked
4. Try the mock implementation to understand the SDK's expected behavior

## Notes

- Either `DEMO_AI_PROFILE_ID` or `DEMO_AI_PROFILE_NAME` should be provided
- Set proper error handling in production environments
- Configure appropriate retry strategies for production use