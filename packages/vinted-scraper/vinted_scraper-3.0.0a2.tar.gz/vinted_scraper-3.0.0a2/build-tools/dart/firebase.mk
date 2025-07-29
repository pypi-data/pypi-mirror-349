FIREBASE_PROJECT_NAME ?= $(PROJECT_NAME)
FIREBASE_CLI_VERSION := 11.22.0
FIREBASE_CLI_URL := https://firebase.tools/bin/$(OS)/v$(FIREBASE_CLI_VERSION)
FIREBASE_TMP := $(PROJECT_FOLDER)firebase_tmp
FIREBASE_BIN := $(FIREBASE_TMP)/firebase

firebase.init: ## Initialize the Flutter project with Firebase
	-@rm -rf $(FIREBASE_TMP)
	@mkdir -p $(FIREBASE_TMP)
	@curl -Lo $(FIREBASE_BIN) --progress-bar $(FIREBASE_CLI_URL)
	@chmod +x $(FIREBASE_BIN)
	@echo "Please login with your Firebase account"
	@$(FIREBASE_BIN) login
	-@rm -f $(PROJECT_FOLDER)pubspec.lock
	@flutter pub get
	@dart pub global activate flutterfire_cli 0.2.7
	@PATH="$(FIREBASE_TMP):$$PATH" $(HOME)/.pub-cache/bin/flutterfire configure --yes -p $(FIREBASE_PROJECT_NAME)
	@rm -rf $(FIREBASE_TMP)