# set the project folder if not defined
ifeq ($(origin REPOSITORY), undefined)
REPOSITORY := $(shell jq -r '.repository.url' package.json | sed 's/.git$$//g')
endif


.PHONY: userscript.init
userscript.init: ## Initialize a new userscript project
	@npm install --save-dev mini-css-extract-plugin css-loader sass-loader webpack webpack-monkey sass webpack-cli webpack-dev-server

.PHONY: userscript.build
userscript.build: ## build the user script

	@find . -name "meta.json" -exec sh -c ' \
		file_path=$$(echo $$1 | sed "s/^\.\//\//g" | sed "s/src/dist/g"); \
		script_name=$$(echo $$1 | sed "s|./src/\(.*\)/meta\.json|\1|");  \
		if [ -n "$(UPDATE_URL)" ]; then \
			update_url="$(UPDATE_URL)/$${script_name}.meta.js"; \
			download_url="$(UPDATE_URL)/$${script_name}.user.js"; \
		else \
			update_url="$(REPOSITORY)/raw/refs/heads/main/dist/$${file_path}"; \
			download_url="$(REPOSITORY)/raw/refs/heads/main/dist/$${script_name}.user.js"; \
		fi;  \
		jq --arg version "$(VERSION)" \
			--arg update_url "$$update_url" \
			--arg download_url "$$download_url" \
			".updateURL = \$$update_url | .downloadURL = \$$download_url" "$$1" > temp.json && mv temp.json "$$1" \
	' _ {} \;

	@find . -name "meta.json" -exec sh -c ' \
		jq --arg version "$(VERSION)" \
		".version = \$$version" "$$1" > temp.json && mv temp.json "$$1" \
		' _ {} \;
	@./node_modules/.bin/webpack --mode production


.PHONY: userscript.dev
userscript.dev: ## build the development user script
	@./node_modules/.bin/webpack serve --mode development
