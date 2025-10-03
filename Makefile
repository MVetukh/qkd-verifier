# Makefile for qkd-verifier Coq project

# ---- Coq ----
COQDIR       := coq
COQPROJECT   := $(COQDIR)/_CoqProject
COQ_MAKEFILE := coq_makefile
COQC         := coqc
COQTOP       := coqtop
GENERATED_DIR:= $(COQDIR)/Generated

# ---- Python / venv ----
PYTHON      := python3
VENV_DIR    := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python3
VENV_PIP    := $(VENV_DIR)/bin/pip

# ---- Pipeline inputs ----
CONFIG ?= configs/instances/B92_protocol.toml
GEN_MODULE := src.runner.generate_instance
GEN_ENTRY  := $(VENV_PYTHON) -m $(GEN_MODULE)

# ---- Coq VFILES discovery ----
VCORE  := $(shell find $(COQDIR)/Theories -type f -name '*.v' 2>/dev/null)
VGEN   := $(shell find $(GENERATED_DIR)     -type f -name '*.v' 2>/dev/null)
VFILES := $(VCORE) $(VGEN)

.PHONY: all coq clean gen cert generated check-env rebuild setup venv pipeline coq-quick verify dev test-py format lint help

# Default target
all: pipeline

# ---- Environment & setup ----
check-env:
	@echo "Checking Coq tools..."
	@command -v $(COQC)       >/dev/null 2>&1 || (echo "coqc not found in PATH" && false)
	@command -v $(COQTOP)     >/dev/null 2>&1 || (echo "coqtop not found in PATH" && false)
	@command -v $(COQ_MAKEFILE) >/dev/null 2>&1 || echo "warning: coq_makefile not found in PATH (optional)"
	@command -v opam          >/dev/null 2>&1 || echo "note: opam not found (ok if Coq is system-installed)"
	@echo "coqc:   $$(command -v $(COQC))"
	@echo "coqtop: $$(command -v $(COQTOP))"
	@echo "Checking Python..."
	@command -v $(PYTHON)     >/dev/null 2>&1 || (echo "python3 not found in PATH" && false)
	@echo "python3: $$(command -v $(PYTHON))"

venv:
	@echo "Creating Python virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created. Activate with: source $(VENV_DIR)/bin/activate"

install: venv
	@echo "Installing Python dependencies (editable, with dev extras)..."
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -e .[dev]

setup: check-env install
	@echo "Development environment setup complete."

# ---- Generation (Python -> Coq) ----
gen cert:
	@echo "Generating certificate and Coq file from: $(CONFIG)"
	$(GEN_ENTRY) $(CONFIG)
	@echo "Generation done. See: $(GENERATED_DIR)/b92_inst.v"

# ---- Coq build via coq_makefile ----
Makefile.coq: $(COQPROJECT) $(VFILES)
	@echo "Running coq_makefile on $(COQPROJECT) -> Makefile.coq"
	$(COQ_MAKEFILE) -f $(COQPROJECT) $(VFILES) -o Makefile.coq

coq: Makefile.coq
	$(MAKE) -f Makefile.coq

# Build only Generated/ via Makefile.coq (optional, when there are many theories)
generated: Makefile.coq
	@echo "Building generated .v files"
	$(MAKE) -f Makefile.coq $(patsubst %.v,%.vo,$(VGEN))

# Quick one-file build (no Makefile.coq), useful for MVP
coq-quick:
	@echo "Quick compile: $(GENERATED_DIR)/b92_inst.v"
	cd $(COQDIR) && $(COQC) Generated/b92_inst.v

# ---- Pipeline ----
pipeline: gen coq
	@echo "Pipeline done."

# ---- Verify (placeholder hook) ----
verify: coq
	@echo "Running full verification pipeline (placeholder)..."
	@$(VENV_PYTHON) -c "\
from src.runner.coq_runner import run_coq_verification; \
print('Verification result:', 'SUCCESS' if run_coq_verification('Generated/b92_inst.v') else 'FAIL')"

# ---- Dev helpers ----
test-py:
	$(VENV_PYTHON) -m pytest tests/ -v

format:
	$(VENV_PYTHON) -m black src/ tests/

lint:
	@echo "Running code quality checks..."
	$(VENV_PYTHON) -m flake8 src/
	$(VENV_PYTHON) -m mypy src/

# ---- Cleaning ----
clean:
	@if [ -f Makefile.coq ]; then $(MAKE) -f Makefile.coq clean; fi
	@rm -f Makefile.coq
	@find $(COQDIR) -name '*.vo' -delete
	@find $(COQDIR) -name '*.glob' -delete
	@find $(COQDIR) -name '*~' -delete
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	@rm -rf *.egg-info

rebuild: clean pipeline

help:
	@echo "Available targets:"
	@echo "  setup      - Create venv and install dependencies"
	@echo "  gen|cert   - Run Python generator (CONFIG=... overrides input)"
	@echo "  coq        - Build all Coq files via coq_makefile"
	@echo "  coq-quick  - Quick compile of Generated/b92_inst.v without Makefile.coq"
	@echo "  pipeline   - gen + coq"
	@echo "  verify     - Placeholder: run coq_runner check"
	@echo "  clean      - Clean build artifacts"
	@echo "  rebuild    - Clean and rebuild pipeline"
	@echo "  test-py    - Run Python tests"
	@echo "  format     - Format Python code"
	@echo "  lint       - Lint Python code"
