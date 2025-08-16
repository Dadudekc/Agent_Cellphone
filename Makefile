.PHONY: overnight-run overnight-digest setup
setup:
	python -m pip install -U pip ruff pyright pytest coverage pyyaml requests

overnight-run:
	python orchestrators/overnight_runner.py

overnight-digest:
	python scripts/post_digest.py
