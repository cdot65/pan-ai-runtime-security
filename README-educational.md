# Introduction to AI Security SDK

This guide introduces the AI Security SDK, a tool for securing AI applications by detecting and mitigating potential security risks in AI interactions.

## What is AI Security?

AI Security helps protect AI applications from various threats:

1. **Malicious URLs**: Detecting potentially harmful links in prompts or responses
2. **Data Loss Prevention (DLP)**: Identifying sensitive information that shouldn't be shared
3. **Prompt Injection**: Detecting attempts to manipulate AI systems through carefully crafted inputs

## How the SDK Works

The AI Security SDK follows this workflow:

1. **Content Submission**: Your application submits prompt-response pairs to the security service
2. **Security Analysis**: The service analyzes the content for security threats
3. **Response**: The service returns a verdict ("allow" or "block") with details about detected issues
4. **Action**: Your application can take appropriate action based on the verdict

## Getting Started

### Installation

Install the AI Security SDK using pip:

```bash
# Create a virtual environment (recommended)
python3 -m venv --prompt aisec-venv .venv
source .venv/bin/activate

# Install the package
pip install "aisecurity >= 1.0, < 2.0"
```

### Configuration

Create a `.env` file with your credentials:

```
PANW_AI_SEC_API_KEY=your_api_key_here
PANW_AI_PROFILE_NAME=your_profile_name
```

### Basic Usage

Here's a simple example of how to use the SDK:

```python
import os
import aisecurity
from aisecurity.generated_openapi_client.models.ai_profile import AiProfile
from aisecurity.scan.models.content import Content
from aisecurity.scan.sync.scanner import Scanner
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the SDK
aisecurity.init()

# Create a scanner
scanner = Scanner()

# Configure the AI profile
profile_name = os.environ.get("PANW_AI_PROFILE_NAME")
ai_profile = AiProfile(profile_name=profile_name)

# Create content to scan
content = Content(
    prompt="What is the capital of France?",
    response="The capital of France is Paris."
)

# Perform a security scan
scan_response = scanner.sync_scan(ai_profile=ai_profile, content=content)

# Check the result
if scan_response.action == "allow":
    print("✅ Content is safe")
    print(f"Processing: {content.prompt}")
    print(f"Response: {content.response}")
else:
    print("⚠️ Security issues detected!")
    print(f"Category: {scan_response.category}")
    print(f"Action: {scan_response.action}")
    
    # Show details about detected issues
    if scan_response.prompt_detected.url_cats:
        print("- Contains potentially malicious URLs")
    if scan_response.prompt_detected.dlp:
        print("- Contains sensitive information")
    if scan_response.prompt_detected.injection:
        print("- Contains potential prompt injection")
```

## Key Concepts

### 1. SDK Initialization

Initialize the SDK with your credentials:

```python
# Using environment variables (recommended)
aisecurity.init()

# Or provide credentials directly
aisecurity.init(
    api_key="YOUR_API_KEY",
    api_endpoint="https://service.api.aisecurity.paloaltonetworks.com"
)
```

### 2. AI Profiles

AI Profiles define security policies:

```python
# Using profile name (loads the latest version)
ai_profile = AiProfile(profile_name="your_profile_name")

# Or using profile ID (loads a specific version)
ai_profile = AiProfile(profile_id="your_profile_id")
```

### 3. Content Objects

Content objects represent the text to scan:

```python
# Scan both prompt and response
content = Content(
    prompt="User input here",
    response="AI response here"
)

# Or scan just the prompt
content = Content(prompt="User input here")

# Or scan just the response
content = Content(response="AI response here")
```

### 4. Scan Methods

The SDK offers different scanning methods:

#### Synchronous Scanning

Best for real-time applications where you need immediate results:

```python
scan_response = scanner.sync_scan(ai_profile=ai_profile, content=content)
```

#### Asynchronous Scanning

Best for batch processing multiple content items:

```python
# Create async scan objects
async_scan_objects = [
    AsyncScanObject(
        req_id=1,  # Your identifier for this request
        scan_req=ScanRequest(
            tr_id="tx-001",  # Transaction ID
            ai_profile=ai_profile,
            contents=[
                ScanRequestContentsInner(
                    prompt="First prompt",
                    response="First response"
                )
            ],
        ),
    ),
    # Add more items as needed
]

# Submit for scanning
async_response = scanner.async_scan(async_scan_objects)

# Later, query results using the scan ID
scan_results = scanner.query_by_scan_ids(
    scan_ids=[async_response.scan_id]
)
```

## Common Integration Patterns

### 1. Pre-Processing Filter

Scan user inputs before processing them:

```python
def process_user_input(user_prompt):
    # Create content object
    content = Content(prompt=user_prompt)
    
    # Scan the content
    scan_result = scanner.sync_scan(ai_profile=ai_profile, content=content)
    
    if scan_result.action == "allow":
        # Process the content
        return generate_ai_response(user_prompt)
    else:
        # Return an error message
        return "Sorry, your input contains security issues and cannot be processed."
```

### 2. Decorator Pattern

Add scanning capabilities to existing functions:

```python
import functools

def ai_security_scan(func):
    @functools.wraps(func)
    def wrapper(prompt, *args, **kwargs):
        # Create content object
        content = Content(prompt=prompt)
        
        # Scan the content
        scan_result = scanner.sync_scan(ai_profile=ai_profile, content=content)
        
        if scan_result.action == "allow":
            # Call the original function
            return func(prompt, *args, **kwargs)
        else:
            # Return an error message
            return "Sorry, your input cannot be processed due to security concerns."
    
    return wrapper

# Apply the decorator to existing functions
@ai_security_scan
def generate_content(prompt):
    # Your content generation logic here
    return f"Generated content for: {prompt}"
```

### 3. Post-Processing Filter

Scan both prompts and responses:

```python
def secure_ai_interaction(user_prompt):
    # First, scan the prompt
    prompt_content = Content(prompt=user_prompt)
    prompt_scan = scanner.sync_scan(ai_profile=ai_profile, content=prompt_content)
    
    if prompt_scan.action != "allow":
        return "Your input contains security issues."
    
    # Generate AI response
    ai_response = generate_ai_response(user_prompt)
    
    # Scan the complete interaction
    full_content = Content(prompt=user_prompt, response=ai_response)
    full_scan = scanner.sync_scan(ai_profile=ai_profile, content=full_content)
    
    if full_scan.action == "allow":
        return ai_response
    else:
        return "Sorry, I cannot provide that information due to security concerns."
```

## Understanding Scan Results

The scan response contains detailed information:

```python
scan_response = scanner.sync_scan(ai_profile=ai_profile, content=content)

# Unique identifiers
print(f"Scan ID: {scan_response.scan_id}")
print(f"Report ID: {scan_response.report_id}")
print(f"Transaction ID: {scan_response.tr_id}")

# Security verdict
print(f"Category: {scan_response.category}")  # e.g., "safe", "malicious", "sensitive"
print(f"Action: {scan_response.action}")      # "allow" or "block"

# Detailed detection information
print("Prompt issues:")
print(f"- URLs: {scan_response.prompt_detected.url_cats}")
print(f"- DLP: {scan_response.prompt_detected.dlp}")
print(f"- Injection: {scan_response.prompt_detected.injection}")

print("Response issues:")
print(f"- URLs: {scan_response.response_detected.url_cats}")
print(f"- DLP: {scan_response.response_detected.dlp}")
```

## Best Practices

1. **Use Environment Variables**: Store API keys in environment variables, not in code
2. **Error Handling**: Implement proper error handling for API failures
3. **Performance Consideration**: 
   - Use synchronous scanning for real-time interactions
   - Use asynchronous scanning for batch processing
4. **Testing**: Use mock implementations during development to avoid API usage costs

## Error Handling

Implement robust error handling:

```python
try:
    scan_response = scanner.sync_scan(ai_profile=ai_profile, content=content)
    
    if scan_response.action == "allow":
        # Process content
        pass
    else:
        # Handle security issues
        pass
        
except aisecurity.exceptions.AISecSDKException as e:
    # Handle SDK-specific errors
    print(f"SDK Error: {e}")
    
except Exception as e:
    # Handle other errors
    print(f"Unexpected error: {e}")
```

## Common Use Cases

1. **Chatbot Security**: Prevent chatbots from responding to malicious prompts
2. **Content Generation Safety**: Ensure AI-generated content doesn't contain sensitive information
3. **Data Protection**: Prevent accidental data leakage in AI interactions
4. **Prompt Injection Defense**: Protect against attempts to manipulate your AI system

## Next Steps

Explore the detailed examples in this repository to learn more advanced usage patterns:

- [Main Script](docs-main.md) - Basic SDK functionality
- [Synchronous Scan](docs-sync-scan.md) - Real-time scanning
- [Asynchronous Scan](docs-async-scan.md) - Batch processing
- [Asyncio Concurrent](docs-asyncio-concurrent.md) - Parallel operations
- [Decorator Pattern](docs-decorator-example.md) - Elegant integration
- [Mock Implementation](docs-mock-example.md) - Testing without API credentials
- [Utilities](docs-utils.md) - Helper functions

---

By understanding these core concepts, you can effectively integrate AI Security into your applications to protect against various security threats in AI interactions.