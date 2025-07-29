# Build - JavaScript

A collection of useful [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) make command.

## Prerequisites

- [ECMAScript 2015](https://www.w3schools.com/Js/js_versions.asp).

### Install

Create your `Makefile`. An example of a minimal configuration is:

```makefile
# ====================================================================================
# Setup Project
ROOT := $(shell pwd)/
PROJECT_FOLDER := $(ROOT)/src
TECHNOLOGY := javascript

include $(BUILD_TOOLS_FOLDER)/common.mk
include $(BUILD_TOOLS_FOLDER)/common_linters.mk
include $(BUILD_TOOLS_FOLDER)/$(TECHNOLOGY)/$(TECHNOLOGY).mk

# ====================================================================================
# Actions

.PHONY: all
all: fmt

.PHONY: init
init: javascript.init

.PHONY: update
update: javascript.update

.PHONY: fmt
fmt: javascript.fmt

.PHONY: lint
lint: lint.checkmake lint.superlinter

.PHONY: clean
clean: lint.clean

.PHONY: test
test: ; @:
```

Then you can initialize the project by executing the following command:

```shell
    make init
```
