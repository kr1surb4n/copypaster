.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_TARGET=print

APP_NAME = copypaster

TEST_FOLDERS = tests app copypaster
CODE_FOLDERS = $(APP_NAME) $(TEST_FOLDERS)

CODE_PATHS = $(CODE_FOLDERS)
COVERAGE_PATHS = app,copypaster

REMOTE_GIT_SERVER = git@github.com:kr1surb4n/copypaster.git
ORIGIN = kris
MASTER = main

REQUIREMENTS = requirements.txt
REQUIREMENTS_FREEZE = requirements_freeze.txt
REQUIREMENTS_DEV = requirements_dev.txt

BROWSER = firefox

push:
	git push $(ORIGIN) $(MASTER)

print:
	@echo $(APP_NAME)
	@echo $(CODE_FOLDERS)
	@echo $(CODE_PATHS)
	@echo $(TEST_FOLDERS)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

coverage: ## check code coverage quickly with the default Python
	coverage run --omit=lib,dirtynotes --source=$(COVERAGE_PATHS) -m pytest
	coverage report -m

check_code:
	pycodestyle $(CODE_PATHS)

dist: clean
	rm -rf dist/*
	python setup.py sdist
	python setup.py bdist_wheel

dist-upload:
	twine upload dist/*

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/$(APP_NAME).rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ $(CODE_PATHS)
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

document:
	pycco -spi -d docs/literate $(CODE_PATHS)

fmt:
	black -qS --config black.toml $(CODE_FOLDERS)

install: clean ## install the package to the active Python's site-packages
	python setup.py install

flake: ## check style with flake8
	flake8 $(CODE_FOLDERS)

mypy:
	mypy $(CODE_FOLDERS)

lint: ## check style with flake8
	pylint $(CODE_FOLDERS)

pre-commit: clean fmt remove-imports lint test

requirements:
	.venv/bin/pip freeze --local > $(REQUIREMENTS_FREEZE)

remove-imports:
	autoflake -r --in-place \
		--remove-all-unused-imports \
		--exclude .venv,.git,.pytest_cache,__pycache__ \
		.

run:
	copypaster > last_run.log 2>&1 &

run-debug:
	copypaster --debug > last_run.log 2>&1 &

sec:
	bandit -r .

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .


test: ## run tests quickly with the default Python
	pytest -q --log-level=ERROR tests/test_app.py
	pytest -q --log-level=ERROR tests/test_copypaster.py
	pytest -q --log-level=ERROR tests/app/*.py
	pytest -q --log-level=ERROR tests/copypaster/*.py
	pytest -q --log-level=ERROR tests/behaviors/app/*.py
	pytest -q --log-level=ERROR tests/behaviors/copypaster/*.py
	pytest -q --log-level=ERROR tests/integrations/app/cli.py
	pytest -q --log-level=ERROR tests/integrations/app/main.py
	pytest -q --log-level=ERROR tests/integrations/copypaster/cli.py
	pytest -q --log-level=ERROR tests/integrations/copypaster/main.py
# test:
# 	python -m pytest \
# 		-v \
# 		--cov=simple \
# 		--cov-report=term \
# 		--cov-report=html:coverage-report \
# 		$(TEST_FOLDERS)

test-watcher:
	ptw $(CODE_PATHS) $(TEST_FOLDERS)

test-all: ## run tests on every Python version with tox
	tox

update:
	pip install -r requirements.txt

update-dev:
	pip install -r requirements_dev.txt 


virtualenv:
	virtualenv --prompt '|> $(APP_NAME) <| ' .venv
	.venv/bin/pip install -r $(REQUIREMENTS_DEV)
	.venv/bin/python setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: source .venv/bin/activate"
	@echo