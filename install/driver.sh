# Step 1: look for the chromedriver version at  https://googlechromelabs.github.io/chrome-for-testing/#stable
set -e
url=https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.95/mac-arm64/chromedriver-mac-arm64.zip
target_binary=binary/chromedriver-mac-arm64/chromedriver
rm -rf binary/chromedriver-mac-arm64
mkdir -p binary/chromedriver-mac-arm64
# Step 2: download the chromedriver binary if it does not exist or is outdated
if [ ! -f "$target_binary" ] || ! cmp --silent <(curl -s $url) <(curl -s $target_binary); then
    echo "Downloading ChromeDriver..."
    mkdir -p $(dirname $target_binary)
    curl -L $url -o binary/chromedriver-mac-arm64.zip
    unzip -o binary/chromedriver-mac-arm64.zip -d binary/chromedriver-mac-arm64
fi
# Step 3: make the chromedriver executable
target_pattern=**/*/chromedriver
target_binary=$(find binary -type f -name chromedriver)
chmod +x $target_binary
echo "ChromeDriver is up to date.\n"
binary/chromedriver-mac-arm64/chromedriver-mac-arm64/chromedriver --version

echo "File is at: $target_binary"