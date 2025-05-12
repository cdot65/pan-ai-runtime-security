# TODO: Pan-AISecurity Python SDK Example Upgrade Plan

This document outlines the prioritized tasks for upgrading our example repository to work with the latest version of the pan-aisecurity Python SDK.

## Phase 1: Infrastructure and Foundation

- [ ] **Restructure repository to use dedicated folders**
  - [ ] Create folder structure: `examples/example01-basic`, `examples/example02-sync-scan`, etc.
  - [ ] Move example code to appropriate folders
  - [ ] Update documentation references
  - [ ] Add README.md to each example folder

- [ ] **Set up development environment**
  - [ ] Create Python virtual environment requirements
  - [ ] Configure linting (pylint/flake8) and formatting (black)
  - [ ] Configure type checking (mypy)
  - [ ] Set up basic CI for code quality checks

- [ ] **Update SDK installation instructions**
  - [ ] Verify correct pip installation command for latest SDK
  - [ ] Document minimum Python version requirements
  - [ ] Update .env.example with current environment variables
  - [ ] Create standardized environment loading utility

## Phase 2: Core Example Refactoring (Priority Order)

1. [ ] **Create shared utility module (examples/shared/utils.py)**
   - [ ] Update environment loading to support latest SDK
   - [ ] Update common utility functions for SDK compatibility
   - [ ] Add type hints to all functions
   - [ ] Improve error handling for SDK errors
   - [ ] Create comprehensive documentation
   - [ ] Add unit tests

2. [ ] **Create example01-basic (examples/example01-basic/)**
   - [ ] Refactor main.py to new folder structure
   - [ ] Update basic SDK initialization
   - [ ] Update synchronous scanning example
   - [ ] Add proper error handling with new SDK error types
   - [ ] Create README.md with usage instructions
   - [ ] Add sample output

3. [ ] **Create example02-sync-scan (examples/example02-sync-scan/)**
   - [ ] Refactor sync_scan.py to new folder structure
   - [ ] Update synchronous scanning implementation
   - [ ] Ensure compatibility with latest SDK API
   - [ ] Add comprehensive error handling
   - [ ] Create README.md with usage instructions
   - [ ] Add sample output

4. [ ] **Create example03-async-scan (examples/example03-async-scan/)**
   - [ ] Refactor async_scan.py to new folder structure
   - [ ] Update asynchronous scanning implementation
   - [ ] Test batch processing with latest SDK
   - [ ] Optimize for current best practices
   - [ ] Create README.md with usage instructions
   - [ ] Add sample output

5. [ ] **Create example04-concurrent (examples/example04-concurrent/)**
   - [ ] Refactor asyncio_concurrent.py to new folder structure
   - [ ] Update concurrent operations
   - [ ] Optimize asyncio patterns for latest Python best practices
   - [ ] Test with latest SDK version
   - [ ] Create README.md with usage instructions
   - [ ] Add sample output

6. [ ] **Create example05-decorator (examples/example05-decorator/)**
   - [ ] Refactor decorator_example.py to new folder structure
   - [ ] Update decorator pattern implementation
   - [ ] Ensure compatibility with latest SDK
   - [ ] Add type hints and improve error handling
   - [ ] Create README.md with usage instructions
   - [ ] Add sample output

7. [ ] **Create example06-mock (examples/example06-mock/)**
   - [ ] Refactor mock_example.py to new folder structure
   - [ ] Update mock implementation for testing
   - [ ] Ensure compatibility with latest SDK interfaces
   - [ ] Add type hints and improve error handling
   - [ ] Create README.md with usage instructions
   - [ ] Add sample output

## Phase 3: Testing and Validation

- [ ] **Create comprehensive tests**
  - [ ] Add pytest fixtures for SDK testing
  - [ ] Create unit tests for each example
  - [ ] Add integration tests for key workflows
  - [ ] Create mock tests for offline development

- [ ] **Performance testing**
  - [ ] Benchmark each example
  - [ ] Identify and address performance bottlenecks
  - [ ] Document performance considerations

## Phase 4: Documentation Updates

- [ ] **Update README.md**
  - [ ] Update installation instructions
  - [ ] Update usage examples
  - [ ] Add troubleshooting section
  - [ ] Add section on SDK version compatibility

- [ ] **Create SDK Feature Matrix**
  - [ ] Document all SDK features
  - [ ] Map features to example implementations
  - [ ] Identify missing examples for key features

- [ ] **Create migration guide**
  - [ ] Document changes between SDK versions
  - [ ] Provide upgrade path for existing implementations
  - [ ] Highlight breaking changes

## Phase 5: New Examples Development

- [ ] **Create example07-fastapi (examples/example07-fastapi/)**
  - [ ] Create basic FastAPI app with SDK integration
  - [ ] Demonstrate middleware pattern
  - [ ] Document best practices in README.md
  - [ ] Include requirements.txt specific to this example
  - [ ] Add sample output

- [ ] **Create example08-openai (examples/example08-openai/)**
  - [ ] Create example showing SDK integration with OpenAI Python SDK
  - [ ] Show security scanning of prompts and completions
  - [ ] Document best practices in README.md
  - [ ] Include requirements.txt specific to this example
  - [ ] Add sample output

- [ ] **Create example09-langchain (examples/example09-langchain/)**
  - [ ] Create example showing SDK integration with LangChain
  - [ ] Show security scanning within chain execution
  - [ ] Document best practices in README.md
  - [ ] Include requirements.txt specific to this example
  - [ ] Add sample output

- [ ] **Create example10-flask (examples/example10-flask/)**
  - [ ] Create example showing SDK integration with Flask
  - [ ] Show security scanning in Flask routes
  - [ ] Document best practices in README.md
  - [ ] Include requirements.txt specific to this example
  - [ ] Add sample output

- [ ] **Create example11-streamlit (examples/example11-streamlit/)**
  - [ ] Create example showing SDK integration with Streamlit
  - [ ] Show security scanning in interactive Streamlit app
  - [ ] Document best practices in README.md
  - [ ] Include requirements.txt specific to this example
  - [ ] Add sample output

## Phase 6: Continuous Improvement

- [ ] **Set up automated testing for SDK updates**
  - [ ] Create version compatibility test suite
  - [ ] Configure automation for new SDK releases

- [ ] **Create contribution guidelines**
  - [ ] Document PR process
  - [ ] Define code quality requirements
  - [ ] Create example templates

## Notes

- Focus on one example at a time, completing it fully before moving to the next
- Each example folder should have:
  - README.md with clear usage instructions and explanations
  - requirements.txt with specific dependencies
  - Working code compatible with latest SDK
  - Comprehensive error handling
  - Type hints
  - Sample output or screenshots
  - Basic tests
- Follow a consistent folder structure:
  ```
  examples/
  ├── example01-basic/
  │   ├── README.md
  │   ├── requirements.txt
  │   ├── main.py
  │   └── sample_output.txt
  ├── example02-sync-scan/
  │   ├── README.md
  │   ├── requirements.txt
  │   ├── sync_scan.py
  │   └── sample_output.txt
  ├── ...
  └── shared/
      ├── utils.py
      └── tests/
  ```
- Prioritize core functionality over advanced features
- Document any breaking changes encountered during the upgrade process
- Ensure each example can be run independently with minimal setup