# ====================================================================================
# Setup Project
include common.mk
include common_linters.mk
include ./python/python.mk

# ====================================================================================
# Actions

.PHONY: all
all: test clean

.PHONY: test
test: lint

.PHONY: lint
lint: lint.checkmake lint.superlinter

.PHONY: fmt
fmt: py.fmt

.PHONY: clean
clean: lint.clean
