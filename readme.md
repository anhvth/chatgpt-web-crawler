# ChatGPT Selenium Automation

This project provides a Python script using Selenium to automate interactions with ChatGPT, specifically for submitting messages from a CSV file.

## Prerequisites

1.  **Python:** Ensure you have Python 3.x installed.
2.  **Google Chrome:** You need Google Chrome installed.
3.  **ChromeDriver:** Download ChromeDriver that matches your Chrome version and ensure it's in your system's PATH or specify its path.
4.  **Python Packages:** Install required packages:
    ```bash
    pip install selenium pandas loguru ipdb
    ```
5.  **Running Chrome with Remote Debugging:** Before running the script, you **must** start Google Chrome with remote debugging enabled on port 9223 and a specific user data directory.

    *   **macOS:**
        ```bash
        /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9223 --user-data-dir=.cache/user_example2
        ```
    *   **Linux:**
        ```bash
        google-chrome --remote-debugging-port=9223 --user-data-dir=.cache/user_example2
        ```
    *   **Windows:**
        ```bash
        "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9223 --user-data-dir=C:\Users\YourUser\.cache\user_example2
        ```
        *(Adjust the path to your Chrome executable and desired cache directory)*

    **Note:** The script connects to this specific Chrome instance. Ensure you are logged into ChatGPT in this browser session.

## Installation

1.  Clone the repository:
    ```bash
    git clone <your-repository-url>
    cd chatgpt-selenium
    ```
2.  Install dependencies (as mentioned in Prerequisites).

## Usage

The main script is `chatgpt_selenium/scripts/submit_reqs.py`. It reads messages from a CSV file and submits them to a specified ChatGPT project URL.

### Arguments

*   `csv_file`: (Required positional argument) Path to the CSV file containing the messages. The CSV **must** have a column named `messages`.
*   `--project-url` or `-p`: (Required) The base URL of the ChatGPT project/conversation you want to interact with.
*   `--collect-data` or `-cl`: (Optional flag) If provided, enables data collection features (currently seems unused in the provided script snippet but might be intended for future use).

### Example

1.  **Prepare your CSV file** (e.g., `/tmp/messages.csv`):

    ```csv
    id,messages
    1,"Hello ChatGPT, how are you?"
    2,"Explain the theory of relativity."
    3,"Write a short poem about clouds."
    ```

2.  **Start Chrome with remote debugging** (see Prerequisites).

3.  **Run the script:**

    ```bash
    python chatgpt_selenium/scripts/submit_reqs.py /tmp/messages.csv -p "https://chat.openai.com/c/your-conversation-id"
    ```

    Replace `/tmp/messages.csv` with the actual path to your file and `"https://chat.openai.com/c/your-conversation-id"` with the target ChatGPT conversation URL.

### Output

The script will process each message from the CSV file, send it to the specified ChatGPT URL, and collect the responses. The results (including original messages and responses) will be saved to a new CSV file named `<your_input_file>_submited.csv` (e.g., `/tmp/messages_submited.csv`).

The script includes a `ipdb.set_trace()` breakpoint after processing messages, allowing you to inspect the `conversation_data` variable before the script finishes and saves the output file. Type `c` and press Enter in the debugger to continue execution.

## Development

The core automation logic resides in `chatgpt_selenium/chatgpt_automation.py`. The `submit_reqs.py` script acts as a command-line interface for this logic.
