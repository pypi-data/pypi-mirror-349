.PHONY: javascript.fmt
javascript.fmt: ## Formats the code
	@prettier . "!**/$(BUILD_TOOLS_FOLDER_NAME)" --write 

.PHONY: javascript.update
javascript.update: ## Updates the dependencies
	@npm install

javascript.init: ## Initialize the project
	@npm init $(PROJECT_NAME) --init-author-name Giglium --init-author-url https://github.com/Giglium --init-license ISC --init-version $(VERSION) --yes
	@npm install --save-dev eslint @eslint/js prettier