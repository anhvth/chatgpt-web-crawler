from dataclasses import dataclass


@dataclass
class Config:
    # Path to the ChromeDriver executable
    CHROME_DRIVER_PATH: str = (
        "binary/chromedriver-mac-arm64/chromedriver-mac-arm64/chromedriver"
    )

    # Default wait time for WebDriver (in seconds)
    DEFAULT_WAIT_TIME: int = 10

    # Timeout for waiting for a response (in seconds)
    RESPONSE_WAIT_TIMEOUT: int = 30

    # XPath for the message input field
    MESSAGE_INPUT_XPATH: str = '//*[@id="prompt-textarea"]'

    # CSS Selector for the assistant's response
    RESPONSE_CSS_SELECTOR: str = (
        'div[data-message-author-role="assistant"] div.markdown'
    )

    # XPath for the submit button
    SUBMIT_BUTTON_XPATH: str = '//button[@data-testid="send-button"]'

    # Directory for storing logs
    LOG_DIR: str = "data/logs"

    # Debug port for Chrome (optional)
    DEBUG_PORT: int = 9223
