build-dev:
	@rm -f python/finance_core/*.so
	maturin develop

build-prod:
	@rm -f python/finance_core/*.so
	maturin develop --release

clean:
	rm -f python/finance_core/*.so
	rm -rf `find . -name .venv`
	rm -rf `find . -name __pycache__`

venv:
	python -m venv .venv
	. .venv/bin/activate && \
	pip install -r requirements.txt