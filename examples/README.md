# AI Security SDK Examples

This directory contains examples demonstrating how to use the Palo Alto Networks AI Security SDK (`pan-aisecurity`). Each example is contained in its own directory with a dedicated README and requirements file.

## Examples Directory Structure

- **example01-basic**: Basic SDK initialization and synchronous scanning
- **example02-sync-scan**: Detailed synchronous scanning examples
- **example03-async-scan**: Batch processing with asynchronous scanning
- **example04-concurrent**: Concurrent operations with asyncio
- **example05-decorator**: Using a decorator pattern for scanning
- **example06-mock**: Testing with mock implementations
- **example07-fastapi**: Integration with FastAPI
- **example08-openai**: Integration with OpenAI's Python SDK
- **example09-langchain**: Integration with LangChain
- **example10-flask**: Integration with Flask
- **example11-streamlit**: Integration with Streamlit
- **shared**: Shared utilities and functions used across examples

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Poetry (recommended) or pip
- AI Security API Key from Palo Alto Networks
- AI Security Profile Name or ID

### Installation with Poetry

To set up all examples at once using Poetry:

```bash
# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Using the Makefile

This project includes a Makefile to simplify development tasks:

```bash
# Set up virtual environment and install dependencies
make setup

# Install development dependencies
make install-dev

# Run linting checks
make lint

# Format code
make format

# Run type checks
make type-check

# Run tests
make test

# Run all checks (lint, type-check, test)
make all
```

## Running Individual Examples

Each example directory contains its own README with specific instructions, but generally:

1. Navigate to the example directory
2. Create a `.env` file based on the provided `.env.example`
3. Run the example script:

```bash
# For example
cd example01-basic
cp .env.example .env  # Then edit .env with your credentials
python main.py
```

## Shared Utilities

The `shared` directory contains common utilities used across examples:

- **utils.py**: Environment loading, utility functions, and result formatting
- **tests/**: Unit tests for shared utilities

## Development and Contributions

When contributing to these examples:

- Ensure your code follows the project's style guidelines (use `make format` and `make lint`)
- Add appropriate type hints (check with `make type-check`)
- Write tests for new functionality
- Follow the established directory structure
- Keep dependencies consistent with the project requirements