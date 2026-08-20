.PHONY: install test compare preflight

install:
	python -m pip install -e ".[dev]"

test:
	python -m pytest -q

compare:
	pcc-cross-game --poker-root sources/pcc-poker-v0.8.0 --liars-root sources/pcc-liars-dice-v0.3.0 --output-dir validation

preflight: test compare
	@echo "Cross-game preflight passed."
