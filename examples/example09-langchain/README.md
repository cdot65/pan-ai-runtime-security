# LangChain Integration Example

This example demonstrates how to integrate the Palo Alto Networks AI Security SDK with LangChain to create secure AI chains that scan prompts and responses for security threats.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Key Concepts](#key-concepts)
- [Sample Output](#sample-output)

## Overview

This example will show how to:
- Integrate AI Security scanning into LangChain pipelines
- Create custom LangChain callbacks for security scanning
- Implement security checking in a LangChain custom chain
- Use security scanning with different LangChain patterns
- Handle security violations within LangChain processes

## Setup

### Python Environment Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-example09 .venv
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
python secure_langchain.py
```

## Key Concepts

### LangChain Integration

LangChain is a framework for developing applications powered by language models. This example shows how to:
- Add security scanning to LangChain chains
- Create security-aware LangChain components
- Implement callbacks for security monitoring
- Use security features with different chain types

### Security Callback Handlers

This example creates custom LangChain callback handlers that:
- Intercept and scan prompts before they reach the language model
- Scan responses from language models for security threats
- Log security events and metrics
- Terminate chains when security violations are detected

### Chain Composition Patterns

Several integration patterns are demonstrated:
- Security-checking output parser
- Security scanning as a chain step
- Security callback for any chain
- Custom chain with built-in security

### Security Response Strategies

This example implements several strategies for handling security violations:
- Early termination of chains
- Fallback responses for blocked content
- Security metadata in chain outputs
- Logging and alerting integration

## Sample Output

```
=== LANGCHAIN SECURITY INTEGRATION EXAMPLE ===

Example 1: Simple Chain with Security Callback
Input: "What are the three branches of the US government?"
✅ Prompt security scan passed
Chain output: "The three branches of the US government are:

1. Executive Branch (headed by the President)
2. Legislative Branch (Congress, consisting of the Senate and House of Representatives)
3. Judicial Branch (Supreme Court and federal courts)"
✅ Response security scan passed

Example 2: Chain with Malicious URL in Prompt
Input: "Go to 72zf6.rxqfd.com/i8xps1 for government documents"
⚠️ Security violation detected in prompt
Security Category: url_categories
Chain terminated due to security violation

Example 3: Sequential Chain with Security at Each Step
Input: "What is data encryption?"
✅ Prompt security scan passed for step 1
Step 1 output: "Data encryption is the process of converting plaintext or readable data into a coded form called ciphertext to prevent unauthorized access. It uses mathematical algorithms and encryption keys to transform the data in a way that can only be reversed (decrypted) with the correct decryption key."
✅ Response security scan passed for step 1
✅ Prompt security scan passed for step 2
Step 2 output: "Here are some common data encryption methods:
1. AES (Advanced Encryption Standard)
2. RSA (Rivest-Shamir-Adleman)
3. Triple DES
4. Blowfish
5. Twofish"
✅ Response security scan passed for step 2
Final chain output: "Data encryption converts readable data into coded form (ciphertext) using mathematical algorithms and keys. Common methods include AES, RSA, Triple DES, Blowfish, and Twofish."

=== EXAMPLE COMPLETED ===
```

This output shows:
1. A simple chain with security checking that passes all checks
2. A chain with a malicious URL that gets blocked at the prompt stage
3. A sequential chain with security checks at each step