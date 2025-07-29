ANDROID_LANGUAGE := kotlin
PLATFORMS := android
TEMPLATE := app
PROJECT_NAME := $(shell echo $(PROJECT_NAME) | tr '[:upper:]' '[:lower:]' | sed 's/ /_/g' | sed 's/-/_/g')
ORGANIZATION ?= com.giglium.$(PROJECT_NAME)
APP_NAME ?= $(PROJECT_NAME)

.PHONY: flutter.clean
flutter.clean: ## Cleans the project
	-@rm -rf $(PROJECT_FOLDER)pubspec.lock
	-@rm -rf $(PROJECT_FOLDER)ios/PodFile.lock
	@flutter clean

.PHONY: flutter.lint
flutter.lint: ## Lints the code
	@flutter analyze .

.PHONY: flutter.build.android
flutter.build.android: ##   Building the application for Android
	@flutter pub get
	@flutter pub run flutter_launcher_icons -f $(PROJECT_FOLDER)/flutter_launcher_icons.yaml
	@flutter pub run rename_app:main android="${APP_NAME}"
	@flutter build apk

.PHONY: flutter.test
flutter.test: ## Run all the unit test on the codebase.
	@flutter test

.PHONY: flutter.init
flutter.init: ## Initialize the Flutter project. For now, only Android is supported.
	@flutter create -e -a $(ANDROID_LANGUAGE) --platforms $(PLATFORMS) --template $(TEMPLATE) --project-name $(PROJECT_NAME) --org $(ORGANIZATION)  $(PROJECT_FOLDER)
	@mkdir -p $(PROJECT_FOLDER)/assets/images
	@touch $(PROJECT_FOLDER)/assets/images/logo.png
	@flutter pub add flutter_launcher_icons:0.13.1 --dev
	@flutter pub add rename_app:1.3.2 --dev
	@cp -r $(BUILD_TOOLS_FOLDER)/$(TECHNOLOGY)/.github/ $(PROJECT_FOLDER)/.github/
	@cp $(BUILD_TOOLS_FOLDER)/$(TECHNOLOGY)/flutter_launcher_icons.yaml $(PROJECT_FOLDER)/flutter_launcher_icons.yaml
