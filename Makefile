# Makefile
# vim:ft=make

include ./tools/Common.mk
include ./tools/Python.mk

.PHONY: container.build
container.build: ## build, start and initialize containers cluster
	@docker-compose up -d
	@sleep 3
	@./tools/init.sh

.PHONY: container.run.drill
container.drill.run: ## shortcut to start drill container
	@./tools/drill/manage.sh run
