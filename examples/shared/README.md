# Shared Utilities for AI Security SDK Examples

This directory contains shared utilities and common functionality used across the Palo Alto Networks AI Security SDK examples.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Utilities](#utilities)
- [Testing](#testing)

## Overview

The shared utilities provide common functionality such as:
- Environment variable loading
- SDK initialization
- Common security scanning functions
- Helper functions for formatting outputs
- Testing utilities for the examples

By centralizing these utilities, the examples maintain consistent behavior and reduce code duplication.

## Setup

### Python Environment Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv --prompt aisec-shared .venv
   source .venv/bin/activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Utilities

### Environment Management

The shared module provides consistent environment loading across examples:
- Loading from `.env` files
- Validating required credentials
- Providing fallback values
- Handling missing configurations

### Security Utilities

Common security functions include:
- Standard scanning configuration
- Result formatting and pretty printing
- Detection handling for different threat types
- Security logging and metrics

### Example Helper Functions

Helpers for the examples include:
- Sample content generation
- Result formatting for console output
- Security response interpretation
- Common configuration patterns

## Testing

The `tests` directory contains:
- Unit tests for shared utilities
- Mock implementations for testing without API credentials
- Test fixtures for examples
- Common test utilities

Run the tests with:

```bash
pytest tests/
```

## Usage in Examples

Import shared utilities in your examples:

```python
# Import from shared utilities
from shared.utils import load_environment, print_scan_result_summary

# Get environment configuration
env = load_environment()

# Use shared utility functions
print_scan_result_summary(scan_response)
```

This ensures consistent behavior across all examples while minimizing code duplication.