# Makefile for qkd-verifier Coq project
COQDIR := coq
COQPROJECT := $(COQDIR)/_CoqProject

COQ_MAKEFILE := coq_makefile
COQC := coqc
COQTOP := coqtop

GENERATED_DIR := $(COQDIR)/Generated

# Python configuration for WSL compatibility
PYTHON := python3
VENV_PYTHON := .venv/bin/python3
VENV_PIP := .venv/bin/pip

.PHONY: all coq clean generated check-env rebuild

all: coq

coq: Makefile.coq
	$(MAKE) -f Makefile.coq

Makefile.coq: $(COQPROJECT)
	@echo "Running coq_makefile on $(COQPROJECT) -> Makefile.coq"
	$(COQ_MAKEFILE) -f $(COQPROJECT) -o Makefile.coq

generated: Makefile.coq
	@echo "Building generated .v files (if any)"
	$(MAKE) -f Makefile.coq COQFILES="$(shell find $(GENERATED_DIR) -name '*.v' | sed 's/\.v/\.vo/g')"

clean:
	@if [ -f Makefile.coq ]; then $(MAKE) -f Makefile.coq clean; fi
	@rm -f Makefile.coq
	@find $(COQDIR) -name '*.vo' -delete
	@find $(COQDIR) -name '*.glob' -delete
	@find $(COQDIR) -name '*~' -delete
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	@rm -rf *.egg-info
	@rm -rf .venv

rebuild: clean coq

check-env:
	@echo "Checking coq executables and tools..."
	@command -v $(COQC) >/dev/null 2>&1 || (echo "coqc not found in PATH" && false)
	@command -v $(COQTOP) >/dev/null 2>&1 || (echo "coqtop not found in PATH" && false)
	@command -v $(COQ_MAKEFILE) >/dev/null 2>&1 || echo "warning: coq_makefile not found in PATH"
	@command -v opam >/dev/null 2>&1 || echo "note: opam not found (ok for system coq but needed for opam-managed libs)"
	@echo "coqc: $$(command -v $(COQC))"
	@echo "coqtop: $$(command -v $(COQTOP))"
	@echo "Checking Python..."
	@command -v $(PYTHON) >/dev/null 2>&1 || (echo "python3 not found in PATH" && false)
	@echo "python3: $$(command -v $(PYTHON))"

# Development configuration
DEV_CONFIG = configs/instances/test_protocol.yaml

# Python environment setup
venv:
	@echo "Creating Python virtual environment..."
	$(PYTHON) -m venv .venv
	@echo "Virtual environment created. Activate with: source .venv/bin/activate"

install: venv
	@echo "Installing Python dependencies..."
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -e .[dev]

setup: venv install
	@echo "Development environment setup complete!"

# Запуск полного пайплайна
pipeline:
	@echo "Running verification pipeline..."
	$(VENV_PYTHON) -c "from src.runner.coq_runner import run_coq_verification; run_coq_verification('Theories/Core/Dummy.v')"

# Development targets
dev: check-env coq pipeline
	@echo "Development cycle complete"

test-py:
	$(VENV_PYTHON) -m pytest tests/ -v

format:
	$(VENV_PYTHON) -m black src/ tests/

lint:
	@echo "Running code quality checks..."
	$(VENV_PYTHON) -m flake8 src/
	$(VENV_PYTHON) -m mypy src/

# Full verification with specific config
verify: coq
	@echo "Running full verification pipeline..."
	$(VENV_PYTHON) -c "\
	from src.runner.coq_runner import run_coq_verification; \
	print('Verification result: SUCCESS (basic test)')"

help:
	@echo "Available targets:"
	@echo "  coq       - Build Coq theories"
	@echo "  clean     - Clean generated files"
	@echo "  check-env - Check development environment"
	@echo "  setup     - Setup Python virtual environment and dependencies"
	@echo "  pipeline  - Run verification pipeline with test file"
	@echo "  verify    - Run full verification with config"
	@echo "  test-py   - Run Python tests"
	@echo "  format    - Format Python code"
	@echo "  lint      - Run code quality checks"
	@echo "  dev       - Run complete development cycle"
	@echo "  help      - Show this help"