# Build - Userscript

A collection of useful [Userscript](https://www.tampermonkey.net/scripts.php) make command.

## Prerequisites

- [JQ](https://github.com/jqlang/jq).

### Install

Create your `Makefile`. An example of a minimal configuration is:

```makefile
# ====================================================================================
# Setup Project
TECHNOLOGY := javascript
VERSION := $(shell jq -r '.version' package.json)

include ./build-tools/common.mk
include $(BUILD_TOOLS_FOLDER)/common_linters.mk
include $(BUILD_TOOLS_FOLDER)/$(TECHNOLOGY)/$(TECHNOLOGY).mk
include $(BUILD_TOOLS_FOLDER)/$(TECHNOLOGY)/userscript.mk
# ====================================================================================
# Actions

.PHONY: all
all: build

.PHONY: fmt
fmt: javascript.fmt

.PHONY: lint
lint: lint.checkmake lint.superlinter

.PHONY: init
init: javascript.init userscript.init

.PHONY: build
build: userscript.build

.PHONY: dev
dev: userscript.dev

.PHONY: clean
clean: lint.clean

.PHONY: test
test: ; @:
```

Then you can initialize the project by executing the following command:

```shell
    make init
```
