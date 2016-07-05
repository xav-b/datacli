# Makefile
# vim:ft=make

include ./tools/Common.mk
include ./tools/Python.mk

.PHONY: container.build
container.build: ## build, start and initialize containers cluster
	@docker-compose up -d
	@./containers/init.sh
