# Makefile
# vim:ft=make

include ./tools/Common.mk
include ./tools/Python.mk

.PHONY: container.build
container.build: ## build, start and initialize containers cluster
	@docker-compose up -d
	@sleep 3
	@./tools/init.sh

.PHONY: container.drill.run
container.drill.run: ## shortcut to start drill container
	@./tools/drill/manage.sh run

.PHONY: container.drill.build
container.drill.build: ## shortcut to build drill container
	@./tools/drill/manage.sh build

# TODO TEST flag instead
release.test: ## simulate package upload on pypi
	python setup.py sdist upload -r pypitest
	make clean

release: ## release new package version
	@python setup.py sdist upload -r pypi

