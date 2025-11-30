.PHONY: setup test run clean lint

setup:
	python -m venv .venv
	@echo "Activate virtual environment with: source .venv/bin/activate (Linux/Mac) or .venv\\Scripts\\activate (Windows)"
	@echo "Then run: pip install -r requirements.txt"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

run:
	python src/run.py "Analyze ROAS drop in last 7 days"

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf src/__pycache__
	rm -rf src/agents/__pycache__
	rm -rf src/orchestrator/__pycache__
	rm -rf src/utils/__pycache__
	rm -rf tests/__pycache__
