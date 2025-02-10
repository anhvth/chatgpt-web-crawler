import pandas as pd

# Path to the ChromeDriver executable
CHROME_DRIVER_PATH = "binary/chromedriver-mac-arm64/chromedriver-mac-arm64/chromedriver"

# Default wait time for WebDriver (in seconds)
DEFAULT_WAIT_TIME = 10

# Timeout for waiting for a response (in seconds)
RESPONSE_WAIT_TIMEOUT = 30

# XPath for the message input field
MESSAGE_INPUT_XPATH = '//*[@id="prompt-textarea"]'

# CSS Selector for the assistant's response
RESPONSE_CSS_SELECTOR = 'div[data-message-author-role="assistant"] div.markdown'

# XPath for the submit button
SUBMIT_BUTTON_XPATH = '//button[@data-testid="send-button"]'

# Directory for storing logs
LOG_DIR = "data/logs"

# Debug port for Chrome (optional, set to None if not using debug mode)
DEBUG_PORT = 9223

# Base URL for ChatGPT
PROJECT_URL = "https://chatgpt.com/g/g-p-67aa1a793a808191b64765ff50fc6e83-label-qa-type/project"

# List of messages to send to ChatGPT
MESSAGE_LIST = pd.read_csv("/tmp/batch_msgs.csv")["messages"].tolist()
OUTPUT_FILE = "/tmp/batch_msgs_step1.csv"
