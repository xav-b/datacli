# Common.mk
# vim:ft=make
#
#  Python configuration  ######################################################

.PHONY: install
install.std: ## standard python setup
	python setup.py install

.PHONY: install.hack
install.hack: ## locally install library and dev requirements
	pip install -r requirements.txt
	pip install -r dev-requirements.txt
	gitlint install-hook

.PHONY: lint
lint: ## lint library and test codes
	flake8 $(PROJECT)/ tests/

.PHONY: test
test: ## run test suite
	py.test --verbose --cov=$(PROJECT) tests/

.PHONY:
present_flake8=$(shell which flake8)
present_pytest=$(shell which test)
present_piprot=$(shell which piprot)
warn_missing_linters:
	@test -n "$(present_flake8)" || echo "WARNING: flake8 not installed."
	@test -n "$(present_pytest)" || echo "WARNING: test not installed."
	@test -n "$(present_piprot)" || echo "WARNING: piprot not installed."

.PHONY: clean
clean: ## remove buid artifacts and temporary files
	rm -rf *.egg-info dist build
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
