.PHONY: dart.fmt
dart.fmt: ## Formats the code
	@dart format .

.PHONY: dart.lint
dart.lint: ## Lints the code
	@dart analyze .

.PHONY: dart.test
dart.test: ## Run all the unit test on the codebase.
	@dart test
