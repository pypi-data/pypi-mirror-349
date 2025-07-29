# Build - Flutter

A collection of useful [Dart](https://dart.dev/)/[Flutter](https://flutter.dev/) make command. For now, mostly design for [Flutter](https://flutter.dev/) and supports only the [Android](https://www.android.com/) device.

Optionally, you can also set up [Firebase](https://firebase.google.com/).

## Prerequisites

- [Dart 3.5.4](https://dart.dev/);
- (Optional) [Flutter 3.24.4](https://flutter.dev/);
- (Optional) [Firebase](https://firebase.google.com/);

### Install

Create your `Makefile`. An example of a minimal configuration is:

```makefile
# ====================================================================================
# Setup Project
ROOT := $(shell pwd)/
BUILD_TOOLS_FOLDER := $(ROOT)/build-tools
TECHNOLOGY := dart

include $(BUILD_TOOLS_FOLDER)/common.mk
include $(BUILD_TOOLS_FOLDER)/$(TECHNOLOGY)/*.mk

# ====================================================================================
# Actions

.PHONY: all
all: fmt lint test build

.PHONY: build
build: flutter.build.android

.PHONY: init
init: flutter.init

.PHONY: test
test: flutter.test

.PHONY: fmt
fmt: dart.fmt

.PHONY: lint
lint: lint.checkmake flutter.lint

.PHONY: clean
clean: flutter.lint lint.clean
```

Then you can initialize the project by executing the following command:

```shell
    make init
```
