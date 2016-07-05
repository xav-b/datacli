# Common.mk
# vim:ft=make
#
#  Python configuration  ######################################################

.PHONY: install
py-install: ## standard python setup
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
test: warn_missing_linters ## run test suite
	py.test --verbose --cov=$(PROJECT) tests/

.PHONY: warn_missing_linters
present_pylint=$(shell which pylint)
present_pytest=$(shell which test)
present_piprot=$(shell which piprot)
warn_missing_linters:
	@test -n "$(present_pylint)" || echo "WARNING: pylint not installed."
	@test -n "$(present_pytest)" || echo "WARNING: test not installed."
	@test -n "$(present_piprot)" || echo "WARNING: piprot not installed."

.PHONY: clean
clean: ## remove buid artifacts and temporary files
	rm -rf *.egg-info dist build
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
