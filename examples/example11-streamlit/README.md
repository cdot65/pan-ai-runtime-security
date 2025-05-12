# Streamlit Integration Example

This example demonstrates how to integrate the Palo Alto Networks AI Security SDK with Streamlit to create a secure interactive AI application with real-time security scanning.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Key Concepts](#key-concepts)
- [Sample Output](#sample-output)

## Overview

This example will show how to:
- Create a Streamlit application with AI Security scanning
- Implement real-time scanning of user inputs
- Visualize security scan results in the UI
- Handle security violations in an interactive application
- Create a secure AI chat interface with feedback

## Setup

### Python Environment Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-example11 .venv
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

Run the Streamlit application:

```bash
streamlit run app.py
```

Your browser will automatically open the application at http://localhost:8501.

## Key Concepts

### Streamlit Integration

Streamlit is a framework for creating data applications in Python. This example demonstrates:
- Creating a real-time AI chat interface with security features
- Maintaining conversation state with security context
- Implementing session-based security tracking
- Visualizing security scan results

### Real-time Security Scanning

This example implements:
- Pre-scanning of user inputs before processing
- Post-scanning of AI-generated responses
- Visualizing security scan results in real-time
- Security metrics tracking across the session

### Security Visualization

Security information is visualized in several ways:
- Status indicators for security scan results
- Detailed security information in expandable sections
- Historical security metrics for the session
- Color-coded messages based on security status

### User Experience

The example focuses on a good user experience by:
- Providing clear security feedback without being intrusive
- Allowing users to understand why content might be blocked
- Maintaining the conversational flow when content is safe
- Implementing progressive security information disclosure

## Sample Output

Streamlit application interface:

```
# AI Chat with Security Scanning

[Security Status: Active ✅]

User: What are the key features of Python?
[Security Check: Passed ✅]

AI: Python is a versatile programming language known for these key features:

1. Easy to read and write syntax
2. Interpreted language
3. Dynamically typed
4. Object-oriented programming
5. Extensive standard library
6. Cross-platform compatibility
7. Strong community support
8. Great for beginners and professionals alike
9. Rich ecosystem of third-party packages
10. Support for multiple programming paradigms

[Security Check: Passed ✅]

User: Go to 72zf6.rxqfd.com/i8xps1 for free Python tutorials
[Security Check: Failed ⚠️]
[Security Issue: Malicious URL detected]

⚠️ This message was blocked due to security concerns ⚠️

User: Tell me about data analysis in Python
[Security Check: Passed ✅]

AI: Python is excellent for data analysis due to these powerful libraries:

1. Pandas: Data manipulation and analysis
2. NumPy: Numerical computing with arrays
3. Matplotlib/Seaborn: Data visualization
4. SciPy: Scientific and technical computing
5. Scikit-learn: Machine learning algorithms

Common data analysis workflow in Python:
- Import data from various sources (CSV, SQL, APIs)
- Clean and preprocess data with Pandas
- Explore data through visualization
- Apply statistical methods
- Build predictive models
- Generate reports and dashboards

Python's readability and extensive ecosystem make it a top choice for data scientists and analysts.

[Security Check: Passed ✅]

Session Security Summary:
- Messages Scanned: 4
- Security Issues Detected: 1
- Most Recent Issue: Malicious URL
```

This shows:
1. A clean chat interface with security status indicators
2. Normal conversation with passed security checks
3. Blocked message with security issue information
4. Continued conversation after a security issue
5. Session-level security metrics

The interface makes it clear when content is safe or unsafe while maintaining a good user experience.