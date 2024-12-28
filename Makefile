# Makefile for Spotify Playlist Maker (Cross-Platform)

# Detect the operating system
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
else
    DETECTED_OS := $(shell uname -s)
endif

# Set variables based on the OS
ifeq ($(DETECTED_OS),Windows)
    PYTHON := python
    VENV_ACTIVATE := .\venv\Scripts\activate
    RM_RF := rmdir /s /q
else
    PYTHON := python3
    VENV_ACTIVATE := . ./venv/bin/activate
    RM_RF := rm -rf
endif

# Common variables
VENV_NAME := venv
PIP := pip
PROJECT_ROOT := $(shell pwd)
SRC_DIR := $(PROJECT_ROOT)/src
TESTS_DIR := $(PROJECT_ROOT)/tests
PYTHONPATH := $(PROJECT_ROOT)
FLASK_APP := $(SRC_DIR)/app.py

# Test-related variables
PYTEST := pytest
COVERAGE := coverage
TEST_ARGS := -v --color=yes

# Phony targets
.PHONY: all setup run clean test lint test-all test-models test-services test-coverage test-report update-deps

# Default target
all: setup run

# Setup virtual environment and install dependencies
setup:
	@echo "Setting up virtual environment in project root..."
ifeq ($(DETECTED_OS),Windows)
	@if not exist $(VENV_NAME) ( \
		$(PYTHON) -m venv $(VENV_NAME) && \
		call $(VENV_ACTIVATE) && \
		$(PIP) install -r requirements.txt && \
		$(PIP) install pytest pytest-cov pytest-mock pytest-asyncio flake8 \
	) else ( \
		echo Virtual environment already exists in project root. Skipping creation. \
	)
else
	@if [ ! -d "$(VENV_NAME)" ]; then \
		$(PYTHON) -m venv $(VENV_NAME); \
		$(VENV_ACTIVATE) && \
		$(PIP) install -r requirements.txt && \
		$(PIP) install pytest pytest-cov pytest-mock pytest-asyncio flake8; \
	else \
		echo "Virtual environment already exists in project root. Skipping creation."; \
	fi
endif

# Run the Flask application
run:
	@echo "Starting Flask application..."
ifeq ($(DETECTED_OS),Windows)
	@call $(VENV_ACTIVATE) && cd $(SRC_DIR) && $(PYTHON) app.py
else
	@$(VENV_ACTIVATE) && cd $(SRC_DIR) && $(PYTHON) app.py
endif

# Clean up virtual environment and coverage reports
clean:
	@echo "Removing virtual environment and coverage reports..."
	@$(RM_RF) $(VENV_NAME)
	@$(RM_RF) .coverage
	@$(RM_RF) htmlcov
	@$(RM_RF) .pytest_cache

# Run all tests with verbose output
test-all:
	@echo "Running all tests..."
ifeq ($(DETECTED_OS),Windows)
	@call $(VENV_ACTIVATE) && set PYTHONPATH=$(PYTHONPATH) && $(PYTEST) $(TESTS_DIR) $(TEST_ARGS)
else
	@$(VENV_ACTIVATE) && PYTHONPATH=$(PYTHONPATH) $(PYTEST) $(TESTS_DIR) $(TEST_ARGS)
endif

# Run only model tests
test-models:
	@echo "Running model tests..."
ifeq ($(DETECTED_OS),Windows)
	@call $(VENV_ACTIVATE) && set PYTHONPATH=$(PYTHONPATH) && $(PYTEST) $(TESTS_DIR)/test_models $(TEST_ARGS)
else
	@$(VENV_ACTIVATE) && PYTHONPATH=$(PYTHONPATH) $(PYTEST) $(TESTS_DIR)/test_models $(TEST_ARGS)
endif

# Run only service tests
test-services:
	@echo "Running service tests..."
ifeq ($(DETECTED_OS),Windows)
	@call $(VENV_ACTIVATE) && set PYTHONPATH=$(PYTHONPATH) && $(PYTEST) $(TESTS_DIR)/test_services $(TEST_ARGS)
else
	@$(VENV_ACTIVATE) && PYTHONPATH=$(PROJECT_ROOT)/src:$(PYTHONPATH) $(PYTEST) $(TESTS_DIR)/test_services $(TEST_ARGS)
endif

# Run tests with coverage
test-coverage:
	@echo "Running tests with coverage..."
ifeq ($(DETECTED_OS),Windows)
	@call $(VENV_ACTIVATE) && set PYTHONPATH=$(PYTHONPATH) && $(PYTEST) $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=term-missing $(TEST_ARGS)
else
	@$(VENV_ACTIVATE) && PYTHONPATH=$(PYTHONPATH) $(PYTEST) $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=term-missing $(TEST_ARGS)
endif

# Generate HTML coverage report
test-report:
	@echo "Generating HTML coverage report..."
ifeq ($(DETECTED_OS),Windows)
	@call $(VENV_ACTIVATE) && set PYTHONPATH=$(PYTHONPATH) && $(PYTEST) $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=html $(TEST_ARGS)
	@echo "Coverage report generated in htmlcov/index.html"
else
	@$(VENV_ACTIVATE) && PYTHONPATH=$(PYTHONPATH) $(PYTEST) $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=html $(TEST_ARGS)
	@echo "Coverage report generated in htmlcov/index.html"
endif

# Run linter
lint:
	@echo "Running linter..."
ifeq ($(DETECTED_OS),Windows)
	@call $(VENV_ACTIVATE) && flake8 $(SRC_DIR) $(TESTS_DIR)
else
	@$(VENV_ACTIVATE) && flake8 $(SRC_DIR) $(TESTS_DIR)
endif

# Install new dependencies and update requirements.txt
update-deps:
	@echo "Updating dependencies..."
ifeq ($(DETECTED_OS),Windows)
	@call $(VENV_ACTIVATE) && $(PIP) install -U -r requirements.txt && $(PIP) freeze > requirements.txt
else
	@$(VENV_ACTIVATE) && $(PIP) install -U -r requirements.txt && $(PIP) freeze > requirements.txt
endif

# Logging function
log:
	@echo "Current working directory: $(PROJECT_ROOT)"
	@echo "Detected OS: $(DETECTED_OS)"
	@echo "Python executable: $(PYTHON)"
	@echo "Virtual environment: $(VENV_NAME)"
	@echo "Source directory: $(SRC_DIR)"
	@echo "Tests directory: $(TESTS_DIR)"
