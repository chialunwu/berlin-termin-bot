VENV_DIR = venv
REQS_FILE = requirements.txt
BUILD_DIR = build
DIST_DIR = dist
DOWNLOAD_DIR_MACOS_INTEL = downloads/macos/intelchip
DOWNLOAD_DIR_MACOS_APPLE = downloads/macos/applechip
DOWNLOAD_DIR_WINDOWS = downloads/windows
SRC_FILE = berlin-termin-bot.py
OUTPUT_FILE = berlin-termin-bot
PYINSTALLER = pyinstaller
ZIP_CMD = zip -r
ZIP_OUTPUT_MACOS_APPLE = ../$(DOWNLOAD_DIR_MACOS_APPLE)/$(OUTPUT_FILE).zip
ZIP_OUTPUT_MACOS_INTEL = ../$(DOWNLOAD_DIR_MACOS_INTEL)/$(OUTPUT_FILE).zip
ZIP_OUTPUT_WINDOWS = ../$(DOWNLOAD_DIR_WINDOWS)/$(OUTPUT_FILE).zip
ADD_DATA = "*.mp3:."
PYTHON_SITE_PACKAGES = $(VENV_DIR)/lib/python3.11/site-packages/

all: help

help:
	@echo "Available make targets:"
	@echo "  install                - Set up Python virtual environment and install dependencies."
	@echo "  build_macos-applechip  - Build application for macOS Apple chip and create ZIP package."
	@echo "  build_macos-intelchip  - Build application for macOS Intel chip and create ZIP package."
	@echo "  build_windows          - Build application for Windows and create ZIP package."

install:
	python3 -m venv $(VENV_DIR)
	source $(VENV_DIR)/bin/activate && pip3 install -r $(REQS_FILE)
	@echo "Installation complete. Virtual environment and dependencies set up."

build: install
	rm -rf $(DIST_DIR) $(BUILD_DIR)
	$(PYINSTALLER) --paths $(PYTHON_SITE_PACKAGES) --onefile --add-data=$(ADD_DATA) $(SRC_FILE)

build_macos-applechip: build
	rm -f $(DOWNLOAD_DIR_MACOS_APPLE)/*
	cd $(DIST_DIR) && $(ZIP_CMD) $(ZIP_OUTPUT_MACOS_APPLE) $(OUTPUT_FILE)
	@echo "Build and packaging complete for macOS Apple chip. ZIP file created at $(ZIP_OUTPUT_MACOS_APPLE)."

build_macos-intelchip: build
	rm -f $(DOWNLOAD_DIR_MACOS_INTEL)/*
	cd $(DIST_DIR) && $(ZIP_CMD) $(ZIP_OUTPUT_MACOS_INTEL) $(OUTPUT_FILE)
	@echo "Build and packaging complete for macOS Intel chip. ZIP file created at $(ZIP_OUTPUT_MACOS_INTEL)."

build_windows: build
	rm -f $(DOWNLOAD_DIR_WINDOWS)/*
	cd $(DIST_DIR) && $(ZIP_CMD) $(ZIP_OUTPUT_WINDOWS) $(OUTPUT_FILE)
	@echo "Build and packaging complete for windows. ZIP file created at $(ZIP_OUTPUT_WINDOWS)."
