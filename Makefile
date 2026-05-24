# Helix dev ergonomics. Run `make help` for available targets.

.PHONY: help test verify-bundles verify-all check-source-values clean

PY := python3
GATES := 13-argument-graph 14-counter-thesis 17-liquidity 18-disclosure-footprint 19-audit-trail 20-constitution

help:
	@echo "Helix dev targets:"
	@echo "  make test            Run all gate unit tests"
	@echo "  make verify-bundles  Run each gate against every committed example bundle"
	@echo "  make verify-all      test + verify-bundles"
	@echo "  make check-source-values  Lint source_values.json against transformations.yaml"
	@echo "  make clean           Remove __pycache__ directories"

test:
	@set -e; for g in $(GATES); do \
	    echo "==> gate $$g tests"; \
	    $(PY) helix/gates/$$g/test_check.py; \
	done

verify-bundles:
	@set -e; \
	for f in helix/gates/13-argument-graph/example_graph.json examples/*/argument_graph.json; do \
	    echo "==> Gate 13: $$f"; \
	    $(PY) helix/gates/13-argument-graph/check.py "$$f" > /dev/null; \
	done; \
	for d in examples/*/; do \
	    if [ -f "$$d/counter_attempt.md" ]; then \
	        echo "==> Gate 14: $$d"; \
	        $(PY) helix/gates/14-counter-thesis/check.py "$$d/counter_attempt.md" > /dev/null; \
	    fi; \
	    if [ -f "$$d/paper.md" ] && [ -f "$$d/appendix.md" ]; then \
	        echo "==> Gate 18: $$d"; \
	        $(PY) helix/gates/18-disclosure-footprint/check.py "$$d/paper.md" "$$d/appendix.md" > /dev/null; \
	    fi; \
	    if [ -f "$$d/transformations.yaml" ] && [ -f "$$d/source_values.json" ]; then \
	        echo "==> Gate 19: $$d"; \
	        $(PY) helix/gates/19-audit-trail/check.py "$$d/transformations.yaml" "$$d/source_values.json" > /dev/null; \
	    fi; \
	done

verify-all: test verify-bundles
	@echo ""
	@echo "All gates green."

check-source-values:
	@set -e; for d in examples/*/; do \
	    t="$$d/transformations.yaml"; s="$$d/source_values.json"; \
	    if [ -f "$$t" ] && [ -f "$$s" ]; then \
	        echo "==> $$d"; \
	        $(PY) tools/check_source_values.py "$$t" "$$s"; \
	    fi; \
	done

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "cleaned __pycache__"
