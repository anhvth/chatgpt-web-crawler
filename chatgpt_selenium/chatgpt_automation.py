import time
from dataclasses import dataclass
from os import makedirs
from typing import Dict, List, Optional

import pandas as pd
import pyperclip
from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
# import config
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from speedy_utils import memoize

from chatgpt_selenium.config import Config


def _send_message_clipboard(textarea, formatted_message, timeout=180):

    if textarea.get_attribute("value"):
        print("Text area should be empty")
        textarea.clear()
        time.sleep(3)

    pyperclip.copy(formatted_message)
    textarea.click()
    time.sleep(3)
    textarea.send_keys(Keys.COMMAND, "v")  # paste

    time.sleep(3)
    textarea.send_keys(Keys.ENTER)


class ChatGPTAutomation:
    def __init__(self, debug_port: Optional[int] = 9223):
        logger.info(f"Initializing ChatGPTAutomation with debug_port={debug_port}")
        self.config = self._get_config()
        self._ensure_directories_exist()
        self.driver = self._setup_driver(debug_port)
        self.wait = WebDriverWait(self.driver, self.config["DEFAULT_WAIT_TIME"])
        logger.info("ChatGPTAutomation initialization complete")

    @staticmethod
    def _get_config() -> Dict:
        """Retrieve configuration from config module."""
        logger.info("Loading configuration settings")
        config = Config()
        config_dict = {
            "CHROME_DRIVER_PATH": config.CHROME_DRIVER_PATH,
            "DEFAULT_WAIT_TIME": config.DEFAULT_WAIT_TIME,
            "RESPONSE_WAIT_TIMEOUT": config.RESPONSE_WAIT_TIMEOUT,
            "MESSAGE_INPUT_XPATH": config.MESSAGE_INPUT_XPATH,
            "RESPONSE_SELECTOR": (By.CSS_SELECTOR, config.RESPONSE_CSS_SELECTOR),
            "SUBMIT_BUTTON_XPATH": config.SUBMIT_BUTTON_XPATH,
            "LOG_DIR": config.LOG_DIR,
        }
        logger.debug(f"Configuration loaded: {config_dict}")
        return config_dict

    def _ensure_directories_exist(self):
        """Create necessary directories for logs and data."""
        logger.info(f"Creating directory: {self.config['LOG_DIR']}")
        makedirs(self.config["LOG_DIR"], exist_ok=True)
        logger.info("Creating directory: data")
        makedirs("data", exist_ok=True)
        logger.debug("Directory creation complete")

    def _setup_driver(self, debug_port: Optional[int]) -> webdriver.Chrome:
        """Initialize Chrome WebDriver with specified options."""
        logger.info("Setting up Chrome WebDriver")
        options = webdriver.ChromeOptions()
        if debug_port:
            logger.info(f"Connecting to existing Chrome instance on port {debug_port}")
            options.add_experimental_option(
                "debuggerAddress", f"127.0.0.1:{debug_port}"
            )

        logger.debug(
            f"Creating Chrome service with driver path: {self.config['CHROME_DRIVER_PATH']}"
        )
        service = webdriver.ChromeService(
            executable_path=self.config["CHROME_DRIVER_PATH"],
            log_path=f'{self.config["LOG_DIR"]}/driver.log',
        )

        try:
            driver = webdriver.Chrome(options=options, service=service)
            logger.success("Chrome driver initialized successfully")
            return driver
        except WebDriverException as e:
            logger.critical(f"Driver initialization failed: {e}")
            raise

    def visit_page(self, url: str) -> None:
        """Navigate to specified URL and verify successful load."""
        logger.info(f"Attempting to navigate to URL: {url}")
        try:
            self.driver.get(url)
            logger.debug("Waiting for page to load completely")
            WebDriverWait(self.driver, 3).until(EC.url_to_be(url))
            logger.success(f"Successfully loaded page: {url}")
        except WebDriverException as e:
            logger.error(f"Failed to load {url}: {e}")
            raise

    def send_message(self, message: str) -> str:
        """Send message to ChatGPT and return current URL."""
        logger.info("Preparing to send message")
        try:
            logger.debug("Waiting for input field to be clickable")
            input_field = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, self.config["MESSAGE_INPUT_XPATH"])
                )
            )
            logger.debug("Entering message text")
            # set the text of the input field to the message
            _send_message_clipboard(input_field, message)

            # logger.debug("Waiting for submit button to be clickable")
            # submit_button = self.wait.until(
            #     EC.element_to_be_clickable(
            #         (By.XPATH, self.config["SUBMIT_BUTTON_XPATH"])
            #     )
            # )
            # logger.debug("Clicking submit button")
            current_url = _current_url = self.driver.current_url
            # submit_button.click()
            while current_url == _current_url:
                time.sleep(0.5)
                current_url = self.driver.current_url
            logger.success(f"Message sent successfully. URL: {current_url}")
            return current_url
        except TimeoutException as e:
            logger.error(f"Timeout while sending message: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error sending message: {e}")
            raise

    def _wait_for_response(self) -> Optional[str]:
        """Wait for and retrieve assistant response text."""
        logger.info("Waiting for ChatGPT response")
        try:
            logger.debug("Looking for response element")
            response_element = WebDriverWait(
                self.driver, self.config["RESPONSE_WAIT_TIMEOUT"]
            ).until(EC.presence_of_element_located(self.config["RESPONSE_SELECTOR"]))
            logger.debug("Waiting for response text to populate")

            def wait_for_copy_turn_msg(d):
                logger.debug("Waiting for copy turn message")
                time.sleep(1)
                try:
                    d.find_element(By.CSS_SELECTOR, "button[aria-label='Copy']")
                    return True
                except:
                    return False

            WebDriverWait(self.driver, 60 * 10).until(wait_for_copy_turn_msg)
            logger.success("Response received successfully")
            return response_element.text
        except TimeoutException:
            logger.warning("Response timeout or incomplete response")
            return None

    def send_messages_and_collect_response(
        self, base_url: str, messages: List[str]
    ) -> List[Dict]:
        """Process list of messages through ChatGPT conversations."""
        assert base_url, f"{base_url=} is invalid"
        conversation_data = self.send_messages(base_url, messages)
        logger.info("All messages sent. Collecting responses")
        conversation_data = self.collect_responses(conversation_data)
        return conversation_data

    def send_messages(self, base_url: str, messages: List[str]) -> List[Dict]:
        logger.info(f"Starting conversation processing for {len(messages)} messages")
        conversation_data = []
        # visited = False
        from tqdm import tqdm
        for idx, message in tqdm(enumerate(messages, 1)):
            logger.info(f"{idx}/{len(messages)} Seending message: {message[:100]}")
            try:
                logger.debug("Starting new conversation")
                if not self.driver.current_url == base_url:
                    self.visit_page(base_url)
                    visited = True

                logger.debug("Sending message")

                @memoize
                def f(base_url, message):
                    current_url = self.send_message(message)
                    return current_url
                
                current_url = f(base_url, message)
                # if visited:
                #     continue
                #     time.sleep(5)
                logger.info(f'{idx} Returned {current_url}')
                output = {
                    "user": message,
                    "assistant": None,
                    "link": current_url,
                }

                conversation_data.append(output)
                time.sleep(3)
                
            except Exception as e:
                raise e

        logger.info(
            f"Conversation processing complete. Processed {len(conversation_data)} messages"
        )
        return conversation_data

    def collect_responses(self, conversation_data: List[Dict]) -> List[Dict]:
        """Collect assistant responses for each conversation."""
        logger.info("Collecting assistant responses")
        assert "link" in conversation_data[0]
        for conversation in conversation_data:
            logger.info(f"Processing conversation: {conversation['link']}")
            try:

                @memoize
                def get_response(link):
                    self.visit_page(link)
                    response = self._wait_for_response()
                    return response

                conversation["assistant"] = get_response(conversation["link"])
            except TimeoutException:
                logger.warning("Response timeout or incomplete response")
                continue
            except Exception as e:
                logger.error(f"Error processing conversation: {e}")
                continue

        logger.info("Response collection complete")
        return conversation_data
