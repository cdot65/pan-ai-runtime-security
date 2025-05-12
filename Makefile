.PHONY: setup clean lint format type-check test all help

# Colors for terminal output
GREEN = \033[0;32m
YELLOW = \033[0;33m
RED = \033[0;31m
NC = \033[0m # No Color

# Default target executed when no arguments are given to make.
default: help

# Help target
help:
	@echo "$(GREEN)Pan AI Runtime Security Example Scripts$(NC)"
	@echo "$(YELLOW)Available targets:$(NC)"
	@echo "  $(GREEN)setup$(NC)        Setup poetry virtual environment and install dependencies"
	@echo "  $(GREEN)install-dev$(NC)  Install development dependencies"
	@echo "  $(GREEN)clean$(NC)        Remove build artifacts and cache directories"
	@echo "  $(GREEN)lint$(NC)         Run linting checks with flake8 and ruff"
	@echo "  $(GREEN)format$(NC)       Format code with ruff"
	@echo "  $(GREEN)type-check$(NC)   Run mypy for type checking"
	@echo "  $(GREEN)test$(NC)         Run tests with pytest"
	@echo "  $(GREEN)all$(NC)          Run lint, type-check, and test"

# Setup python environment and install dependencies
setup:
	@echo "$(YELLOW)Setting up poetry environment...$(NC)"
	poetry env use python3.9 || poetry env use python3.10 || poetry env use python3
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	poetry install
	@echo "$(GREEN)Setup complete!$(NC)"
	@echo "$(YELLOW)Activate environment with:$(NC) poetry shell"

# Install development dependencies
install-dev:
	@echo "$(YELLOW)Installing development dependencies...$(NC)"
	poetry install --with dev
	@echo "$(GREEN)Development dependencies installed!$(NC)"

# Clean up build artifacts and cache directories
clean:
	@echo "$(YELLOW)Removing build artifacts and cache directories...$(NC)"
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf */*/__pycache__
	rm -rf */*/*/__pycache__
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	@echo "$(GREEN)Clean complete!$(NC)"

# Run linting
lint:
	@echo "$(YELLOW)Running flake8...$(NC)"
	poetry run flake8 examples
	@echo "$(YELLOW)Running ruff lint...$(NC)"
	poetry run ruff check examples
	@echo "$(GREEN)Linting complete!$(NC)"

# Format code
format:
	@echo "$(YELLOW)Formatting code with ruff...$(NC)"
	poetry run ruff format examples
	@echo "$(GREEN)Formatting complete!$(NC)"

# Type checking
type-check:
	@echo "$(YELLOW)Running mypy for type checking...$(NC)"
	poetry run mypy examples
	@echo "$(GREEN)Type checking complete!$(NC)"

# Run tests
test:
	@echo "$(YELLOW)Running tests...$(NC)"
	poetry run pytest examples/shared/tests
	@echo "$(GREEN)Tests complete!$(NC)"

# Run all checks
all: lint type-check test
	@echo "$(GREEN)All checks passed!$(NC)"