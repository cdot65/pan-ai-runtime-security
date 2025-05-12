# OpenAI Integration Example

This example demonstrates how to integrate the Palo Alto Networks AI Security SDK with the OpenAI Python SDK to create a secure wrapper around OpenAI API calls.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Key Concepts](#key-concepts)
- [Sample Output](#sample-output)

## Overview

This example will show how to:
- Create a secure wrapper around OpenAI API calls
- Scan user prompts before sending them to OpenAI
- Scan AI-generated responses for security threats
- Handle security violations appropriately
- Track and log security events

## Setup

### Python Environment Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-example08 .venv
   source .venv/bin/activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the example directory with your credentials:
   ```
   PANW_AI_SEC_API_KEY=your_palo_alto_api_key_here
   PANW_AI_PROFILE_NAME=your_profile_name
   OPENAI_API_KEY=your_openai_api_key_here
   # Optional: PANW_AI_SEC_API_ENDPOINT=your_custom_endpoint
   ```

## Usage

Run the example script:

```bash
python secure_openai.py
```

## Key Concepts

### Secure OpenAI Wrapper

This example creates a secure wrapper around OpenAI that:
- Pre-scans all user prompts before sending to OpenAI
- Post-scans all AI-generated responses for security threats
- Filters or blocks unsafe content
- Provides detailed security information about threats

### Bidirectional Scanning

The bidirectional scanning approach:
- Prevents malicious prompts from reaching OpenAI (pre-scanning)
- Detects and blocks unsafe AI-generated content (post-scanning)
- Provides a complete security envelope around the AI interaction
- Logs both input and output security events

### Security Response Strategies

This example implements several strategies for handling security violations:
- Blocking unsafe prompts entirely
- Replacing unsafe responses with safe alternatives
- Providing security metadata with each response
- Failing securely when security services are unavailable

## Sample Output

```
=== SECURE OPENAI INTEGRATION EXAMPLE ===

Example 1: Safe prompt and response
User Prompt: What are the main features of pandas DataFrame?
✅ Prompt security scan passed
✅ Response security scan passed
AI Response: 
Pandas DataFrame is a 2D labeled data structure with columns that can be of different types. Here are its main features:

1. Data alignment: Automatic and explicit data alignment
2. Integrated handling of missing data
3. Size mutability: Columns can be inserted and deleted
4. Powerful groupby functionality for aggregations and transformations
5. Pivoting and reshaping datasets
6. High-performance merging and joining of datasets
7. Time series functionality
8. Flexible indexing on both rows and columns
9. IO tools for loading data from different file formats
10. Vectorized operations for fast calculations

These features make pandas DataFrame a versatile tool for data manipulation and analysis in Python.

Example 2: Unsafe prompt (with malicious URL)
User Prompt: Go to 72zf6.rxqfd.com/i8xps1 for free downloads
⚠️ Prompt security scan failed: Security violation detected
Security Category: url_categories
Action: block
Error: This prompt contains potentially malicious content and has been blocked.

Example 3: Prompt that might generate unsafe response
User Prompt: Write code to delete all files in a system
✅ Prompt security scan passed
⚠️ Response security scan failed: Security violation detected
Security Category: malicious_code
Action: block
AI Response: [BLOCKED] The generated response contained potentially harmful code that could delete files from your system.

=== EXAMPLE COMPLETED ===
```

This output shows:
1. A safe prompt and response passing all security checks
2. An unsafe prompt with a malicious URL being blocked before reaching OpenAI
3. A prompt that passes initial screening but generates an unsafe response that gets blocked