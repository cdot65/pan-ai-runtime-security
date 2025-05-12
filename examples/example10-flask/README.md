# Flask Integration Example

This example demonstrates how to integrate the Palo Alto Networks AI Security SDK with Flask to create a secure web application that scans inputs and responses for security threats.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Key Concepts](#key-concepts)
- [Sample Output](#sample-output)

## Overview

This example will show how to:
- Create a Flask application with AI Security scanning
- Implement custom Flask middleware for security scanning
- Create web routes with built-in security features
- Handle security scan results in a web application context
- Provide appropriate user feedback based on security results

## Setup

### Python Environment Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-example10 .venv
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
   # Optional: PANW_AI_SEC_API_ENDPOINT=your_custom_endpoint
   ```

## Usage

Run the Flask application:

```bash
python app.py
```

You can then access the web application at http://127.0.0.1:5000.

## Key Concepts

### Flask Integration

Flask is a lightweight web framework for Python. This example demonstrates:
- Setting up the AI Security SDK in a Flask application
- Creating request hooks for security scanning
- Implementing custom middleware for automatic scanning
- Using route decorators for security features

### Middleware Approach

The middleware approach for Flask:
- Uses Flask's `before_request` and `after_request` hooks
- Can be configured to scan specific routes or all routes
- Accesses form data and JSON payloads for scanning
- Modifies responses based on security scan results

### Security Response Handling

This example implements several strategies for handling security violations:
- Redirecting to an error page for blocked content
- Displaying user-friendly error messages
- Adding security headers to responses
- Providing admin-level security information for investigation

### Template Integration

The example also shows how to:
- Safely display user input in templates
- Show security information in the UI when appropriate
- Create user-friendly security error pages
- Log security issues for monitoring

## Sample Output

Web application logs:
```
 * Running on http://127.0.0.1:5000
INFO:werkzeug:127.0.0.1 - - [01/Jan/2023 12:00:00] "GET / HTTP/1.1" 200 -
INFO:app:Security scan passed for request from 127.0.0.1
INFO:werkzeug:127.0.0.1 - - [01/Jan/2023 12:00:05] "POST /submit HTTP/1.1" 200 -
INFO:app:Security scan passed for request from 127.0.0.1
INFO:werkzeug:127.0.0.1 - - [01/Jan/2023 12:00:10] "POST /submit HTTP/1.1" 403 -
WARNING:app:Security violation detected: URL categories. Request from 127.0.0.1
INFO:werkzeug:127.0.0.1 - - [01/Jan/2023 12:00:15] "POST /submit HTTP/1.1" 403 -
WARNING:app:Security violation detected: DLP. Request from 127.0.0.1
```

User interaction:
1. User visits homepage and sees a form
2. User submits safe input and gets a normal response
3. User submits input with a malicious URL and sees an error page
4. User submits input with sensitive information and sees a different error

Example response HTML for a security violation:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Security Alert</title>
    <style>
        .error-container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            background-color: #f8d7da;
            color: #721c24;
        }
        .error-icon {
            font-size: 48px;
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">⚠️</div>
        <h1>Security Alert</h1>
        <p>Your request could not be processed due to security concerns.</p>
        <p>Our system detected potentially malicious content in your submission.</p>
        <p><a href="/">Return to Home</a></p>
    </div>
</body>
</html>
```

This shows how the application:
1. Successfully processes safe requests
2. Detects and blocks unsafe requests
3. Provides appropriate user feedback
4. Logs security events for monitoring