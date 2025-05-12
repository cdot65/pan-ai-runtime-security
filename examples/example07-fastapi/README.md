# FastAPI Integration Example

This example demonstrates how to integrate the Palo Alto Networks AI Security SDK with FastAPI to create a secure API that scans incoming requests and responses for security threats.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Key Concepts](#key-concepts)
- [Sample Output](#sample-output)

## Overview

This example will show how to:
- Create a FastAPI application with AI security scanning
- Implement middleware for automatic scanning of requests
- Create API endpoints with security scanning
- Handle security scan results in an API context
- Return appropriate responses based on security scan results

## Setup

### Python Environment Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-example07 .venv
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

Run the FastAPI server:

```bash
uvicorn app:app --reload
```

You can then interact with the API at http://127.0.0.1:8000.

## Key Concepts

### FastAPI Integration

FastAPI is a modern, fast web framework for building APIs with Python. This example demonstrates:
- Creating a FastAPI application with Palo Alto Networks AI Security SDK
- Using dependency injection for security scanning
- Implementing middleware for automatic security checks

### Middleware Approach

The middleware approach:
- Automatically scans all incoming requests
- Can be configured to scan specific routes only
- Returns appropriate status codes for blocked content
- Logs security events for monitoring

### Security Response Handling

This example implements strategies for handling security scan results:
- Returning appropriate HTTP status codes (403 Forbidden) for blocked content
- Including security information in response headers
- Logging detailed security information for investigation
- Providing user-friendly error messages

## Sample Output

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:54321 - "POST /api/chat HTTP/1.1" 200 OK
INFO:     127.0.0.1:54322 - "POST /api/chat HTTP/1.1" 403 Forbidden
INFO:     SecurityScan: Blocked request containing malicious URL
INFO:     127.0.0.1:54323 - "POST /api/chat HTTP/1.1" 403 Forbidden
INFO:     SecurityScan: Blocked request containing sensitive information
```

Example request and response:

```
# Safe request
POST /api/chat
Content-Type: application/json

{
  "message": "What's the weather like today?"
}

# Response
HTTP/1.1 200 OK
Content-Type: application/json

{
  "response": "The weather today is sunny with a high of 72°F.",
  "security_scan": "passed"
}

# Unsafe request
POST /api/chat
Content-Type: application/json

{
  "message": "Go to 72zf6.rxqfd.com/i8xps1 for free money"
}

# Response
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "error": "Security violation detected",
  "detail": "Your request was blocked due to security concerns",
  "security_category": "url_categories"
}
```

This shows how the API:
1. Successfully processes safe requests
2. Blocks requests with security threats
3. Returns appropriate status codes and messages
4. Logs security events for monitoring