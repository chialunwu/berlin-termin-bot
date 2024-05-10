VENV_DIR = venv
REQS_FILE = requirements.txt
BUILD_DIR = build
DIST_DIR = dist
DOWNLOAD_DIR_MACOS_INTEL = download/macos/intelchip
DOWNLOAD_DIR_MACOS_APPLE = download/macos/applechip
DOWNLOAD_DIR_WINDOWS = download\windows
SRC_FILE = berlin-termin-bot.py
OUTPUT_FILE = berlin-termin-bot
INSTRUCTION_FILE = instructions.txt
PYINSTALLER = pyinstaller
ZIP_CMD = zip -r
ZIP_OUTPUT_MACOS_APPLE = $(DOWNLOAD_DIR_MACOS_APPLE)/$(OUTPUT_FILE)_macosapple.zip
ZIP_OUTPUT_MACOS_INTEL = $(DOWNLOAD_DIR_MACOS_INTEL)/$(OUTPUT_FILE)_macosintel.zip
ZIP_OUTPUT_WINDOWS = $(DOWNLOAD_DIR_WINDOWS)\$(OUTPUT_FILE)_windows.zip
ADD_DATA = "*.mp3:."
PYTHON_SITE_PACKAGES = $(VENV_DIR)/lib/python3.*/site-packages/

all: help

help:
	@echo "Available make targets:"
	@echo "  install                - Set up Python virtual environment and install dependencies."
	@echo "  build_macos-applechip  - Build application for macOS Apple chip and create ZIP package."
	@echo "  build_macos-intelchip  - Build application for macOS Intel chip and create ZIP package."
	@echo "  build_windows          - Build application for Windows and create ZIP package."

install:
#	python311 -m venv $(VENV_DIR)
#	$(VENV_DIR)\Scripts\activate && 
	pip311 install -r $(REQS_FILE)
	@echo "Installation complete. Virtual environment and dependencies set up."

build: install
	@if exist "$(DIST_DIR)" rmdir /s /q $(DIST_DIR)
	@if exist "$(BUILD_DIR)" rmdir /s /q $(BUILD_DIR)
	$(PYINSTALLER) --paths $(PYTHON_SITE_PACKAGES) --onefile --add-data=$(ADD_DATA) $(SRC_FILE)
	copy $(DIST_DIR)/$(OUTPUT_FILE) $(OUTPUT_FILE)

build_macos-applechip: build
	mkdir -p $(DOWNLOAD_DIR_MACOS_APPLE)
	rm -f $(DOWNLOAD_DIR_MACOS_APPLE)/*
	$(ZIP_CMD) $(ZIP_OUTPUT_MACOS_APPLE) $(OUTPUT_FILE) $(INSTRUCTION_FILE)
	@echo "Build and packaging complete for macOS Apple chip. ZIP file created at $(ZIP_OUTPUT_MACOS_APPLE)."

build_macos-intelchip: build
	mkdir -p $(DOWNLOAD_DIR_MACOS_INTEL)
	rm -f $(DOWNLOAD_DIR_MACOS_INTEL)/*
	$(ZIP_CMD) $(ZIP_OUTPUT_MACOS_INTEL) $(OUTPUT_FILE) $(INSTRUCTION_FILE)
	@echo "Build and packaging complete for macOS Intel chip. ZIP file created at $(ZIP_OUTPUT_MACOS_INTEL)."

build_windows: build
	@if not exist "$(DOWNLOAD_DIR_WINDOWS)" mkdir $(DOWNLOAD_DIR_WINDOWS)
	del /q $(DOWNLOAD_DIR_WINDOWS)\*
	powershell Compress-Archive -Path $(OUTPUT_FILE) -DestinationPath $(ZIP_OUTPUT_WINDOWS)
	@echo "Build and packaging complete for windows. ZIP file created at $(ZIP_OUTPUT_WINDOWS)."

release:
	gh release delete v1.0.0
	gh release create v1.0.0 --title "v1.0.0" --notes ""
	gh release upload v1.0.0 'download/macos/applechip/berlin-termin-bot_macosapple.zip#macOS (apple chip)'
	gh release upload v1.0.0 'download/macos/intelchip/berlin-termin-bot_macosintel.zip#macOS (intel chip)'
