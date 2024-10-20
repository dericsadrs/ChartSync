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
FLASK_APP := $(SRC_DIR)/app.py

# Phony targets
.PHONY: all setup run clean test lint

# Default target
all: setup run

# Setup virtual environment and install dependencies
setup:
	@echo "Setting up virtual environment in project root..."
ifeq ($(DETECTED_OS),Windows)
	@if not exist $(VENV_NAME) ( \
		$(PYTHON) -m venv $(VENV_NAME) && \
		call $(VENV_ACTIVATE) && \
		$(PIP) install -r requirements.txt \
	) else ( \
		echo Virtual environment already exists in project root. Skipping creation. \
	)
else
	@if [ ! -d "$(VENV_NAME)" ]; then \
		$(PYTHON) -m venv $(VENV_NAME); \
		$(VENV_ACTIVATE) && $(PIP) install -r requirements.txt; \
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

# Clean up virtual environment
clean:
	@echo "Removing virtual environment from project root..."
	@$(RM_RF) $(VENV_NAME)

# Run tests
test:
	@echo "Running tests..."
ifeq ($(DETECTED_OS),Windows)
	@call $(VENV_ACTIVATE) && cd $(SRC_DIR) && pytest
else
	@$(VENV_ACTIVATE) && cd $(SRC_DIR) && pytest
endif

# Run linter
lint:
	@echo "Running linter..."
ifeq ($(DETECTED_OS),Windows)
	@call $(VENV_ACTIVATE) && cd $(SRC_DIR) && flake8 .
else
	@$(VENV_ACTIVATE) && cd $(SRC_DIR) && flake8 .
endif

# Install new dependencies and update requirements.txt
update-deps:
	@echo "Updating dependencies..."
ifeq ($(DETECTED_OS),Windows)
	@call $(VENV_ACTIVATE) && $(PIP) install -U -r requirements.txt && $(PIP) freeze > requirements.txt
else
	@$(VENV_ACTIVATE) && $(PIP) install -U -r requirements.txt && $(PIP) freeze > requirements.txt
endif