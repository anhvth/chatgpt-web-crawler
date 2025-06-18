#!/bin/bash
#
# This script automatically detects the OS, architecture, and installed Chrome version
# to download and set up the latest stable ChromeDriver.
#
# Prerequisites: curl, unzip, jq, and Google Chrome must be installed.
#

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Prerequisite Check ---
# Check if jq is installed, as it's required for parsing JSON from the API.
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install it to continue."
    echo "On macOS: brew install jq"
    echo "On Debian/Ubuntu: sudo apt-get install jq"
    exit 1
fi
# Check for other necessary tools.
if ! command -v curl &> /dev/null || ! command -v unzip &> /dev/null; then
    echo "Error: curl or unzip is not installed. Please ensure they are available in your PATH."
    exit 1
fi

echo "--- Step 1: Detect System & Get Installed Chrome Version ---"

# Detect Operating System and CPU Architecture
OS=$(uname -s)
ARCH=$(uname -m)
CHROME_PLATFORM=""

if [[ "$OS" == "Linux" && "$ARCH" == "x86_64" ]]; then
    CHROME_PLATFORM="linux64"
    # Find the Google Chrome executable on Linux
    CHROME_CMD=$(which google-chrome-stable || which google-chrome || echo "")
    if [[ -z "$CHROME_CMD" ]]; then
        echo "Error: Google Chrome is not installed or not in your PATH on Linux."
        exit 1
    fi
    # Get version from command
    CHROME_VERSION_FULL=$($CHROME_CMD --version)

elif [[ "$OS" == "Darwin" ]]; then
    # Find the Google Chrome application on macOS
    CHROME_APP_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if ! [ -f "$CHROME_APP_PATH" ]; then
        echo "Error: Google Chrome not found at '$CHROME_APP_PATH'."
        exit 1
    fi
    # Determine platform based on architecture
    if [[ "$ARCH" == "arm64" ]]; then
        CHROME_PLATFORM="mac-arm64"
    elif [[ "$ARCH" == "x86_64" ]]; then
        CHROME_PLATFORM="mac-x64"
    else
        echo "Error: Unsupported macOS architecture '$ARCH'."
        exit 1
    fi
    # Get version from the application binary
    CHROME_VERSION_FULL=$("$CHROME_APP_PATH" --version)
else
    echo "Error: Unsupported operating system '$OS'."
    exit 1
fi

# Extract just the version number (e.g., "126.0.6478.127" from "Google Chrome 126.0.6478.127")
INSTALLED_VERSION=$(echo "$CHROME_VERSION_FULL" | awk '{print $3}')
echo "Detected Platform: $CHROME_PLATFORM"
echo "Installed Chrome Version: $INSTALLED_VERSION"


echo -e "\n--- Step 2: Fetch Download URL for Latest Stable ChromeDriver ---"

# Fetch the official JSON data for the latest versions
JSON_DATA=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json)

# Use jq to parse the JSON and get the download URL and version for the Stable channel and our platform
DRIVER_VERSION=$(echo "$JSON_DATA" | jq -r ".channels.Stable.version")
DOWNLOAD_URL=$(echo "$JSON_DATA" | jq -r ".channels.Stable.downloads.chromedriver[] | select(.platform==\"$CHROME_PLATFORM\").url")

if [[ -z "$DRIVER_VERSION" || "$DOWNLOAD_URL" == "null" || -z "$DOWNLOAD_URL" ]]; then
    echo "Error: Could not find a stable ChromeDriver for platform '$CHROME_PLATFORM'."
    echo "Please visit 'https://googlechromelabs.github.io/chrome-for-testing/' to check for available versions."
    exit 1
fi

echo "Latest Stable ChromeDriver available: $DRIVER_VERSION"


echo -e "\n--- Step 3: Download and Set Up ChromeDriver ---"

# Define target directory and binary path. The unzipped folder name matches the zip file name without the extension.
ZIP_FILENAME=$(basename "$DOWNLOAD_URL")
UNZIP_DIR_NAME=${ZIP_FILENAME%.zip}
TARGET_DIR="binary/$UNZIP_DIR_NAME"
TARGET_BINARY="$TARGET_DIR/chromedriver"

# Check if the correct version is already installed to avoid unnecessary downloads
NEEDS_DOWNLOAD=true
if [ -f "$TARGET_BINARY" ]; then
    EXISTING_VERSION=$($TARGET_BINARY --version | awk '{print $2}')
    echo "Found existing ChromeDriver version: $EXISTING_VERSION"
    if [[ "$EXISTING_VERSION" == "$DRIVER_VERSION" ]]; then
        echo "ChromeDriver is already up to date."
        NEEDS_DOWNLOAD=false
    else
        echo "ChromeDriver version mismatch (found $EXISTING_VERSION, need $DRIVER_VERSION). Re-downloading."
    fi
else
    echo "ChromeDriver not found. Downloading..."
fi

# Download and unzip if needed
if [ "$NEEDS_DOWNLOAD" = true ]; then
    DOWNLOAD_ZIP_PATH="binary/$ZIP_FILENAME"

    # Clean up old directory and create new parent directory
    rm -rf "$TARGET_DIR"
    mkdir -p "binary"

    echo "Downloading from: $DOWNLOAD_URL"
    curl --progress-bar -L "$DOWNLOAD_URL" -o "$DOWNLOAD_ZIP_PATH"
    
    echo "Unzipping '$DOWNLOAD_ZIP_PATH'..."
    # Unzip and overwrite, placing contents into the 'binary' directory.
    # The zip file from Google contains a top-level directory (e.g., chromedriver-mac-arm64/).
    unzip -o "$DOWNLOAD_ZIP_PATH" -d "binary" > /dev/null
    
    # Make the final binary executable
    chmod +x "$TARGET_BINARY"
    
    # Clean up the downloaded zip file
    rm "$DOWNLOAD_ZIP_PATH"
    echo "Download and setup complete."
fi


echo -e "\n--- Step 4: Verification ---"
echo "ChromeDriver is ready to use."
echo "Executable path: $TARGET_BINARY"
"$TARGET_BINARY" --version