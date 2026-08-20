.PHONY: install test compare control-benchmark chaos-benchmark preflight

install:
	python -m pip install -e ".[dev]"

test:
	python -m pytest -q

compare:
	python -m pcc_cross_game.cli \
		--poker-root sources/pcc-poker-v0.8.0 \
		--liars-root sources/pcc-liars-dice-v0.4.0 \
		--rps-root sources/pcc-rps-v0.2.0 \
		--output-dir validation

control-benchmark:
	python -m pcc_cross_game.cli \
		--poker-root sources/pcc-poker-v0.8.0 \
		--liars-root sources/pcc-liars-dice-v0.4.0 \
		--rps-root sources/pcc-rps-v0.2.0 \
		--output-dir validation \
		--control-benchmark

chaos-benchmark:
	python -m pcc_cross_game.cli \
		--poker-root sources/pcc-poker-v0.8.0 \
		--liars-root sources/pcc-liars-dice-v0.4.0 \
		--rps-root sources/pcc-rps-v0.2.0 \
		--output-dir validation \
		--chaos-benchmark

preflight: test control-benchmark chaos-benchmark
	@echo "Cross-game preflight passed."
