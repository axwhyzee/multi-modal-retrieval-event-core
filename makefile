clean-develop:
	@if [ -d env ]; then rm -rf env; fi
	python3.8 -m venv env
	./env/bin/pip install black isort mypy pytest

format:
	./env/bin/isort . --profile black --skip env
	./env/bin/black . --line-length 79

test:
	mypy .
	pytest
