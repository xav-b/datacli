# Makefile
# vim:ft=make

.PHONY: container.build
container.build: ## build, start and initialize containers cluster
	@docker-compose up -d
	@sleep 10
	@./tools/init.sh

.PHONY: container.drill.run
container.drill.run: ## shortcut to start drill container
	@./tools/drill/manage.sh run

.PHONY: container.drill.build
container.drill.build: ## shortcut to build drill container
	@./tools/drill/manage.sh build
