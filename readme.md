# ChatGPT Selenium Automation

This project enables automation of ChatGPT interactions using Selenium WebDriver, specifically designed for ChatGPT Pro with unlimited o1 usage.

## Setup Instructions

### Step 1: Launch Chrome Browser
Macos:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    --remote-debugging-port=9223 \
    --user-data-dir=.cache/user_example2
```
Windows:
Figure out how to launch Chrome with remote debugging port enabled. I don't use Windows.

### Step 2: ChatGPT Setup
1. Log in to your ChatGPT Pro account
2. Create a new chat session
3. Configure settings:
   - Select GPT-4 model
   - Keep your session URL

### Step 3: Run Automation
1. Configure `config.py`:
   ```python
   URL = "your_chatgpt_session_url"
   MESSAGES = ["your", "messages", "here"]
   ```

2. Execute the script:
   ```bash
   python main.py
   ```

Results are saved to `data/*.csv`

## Troubleshooting

If ChatGPT's interface changes, update CSS selectors in `config.py`:
1. Right-click the element
2. Copy element HTML
3. Use ChatGPT to generate the correct CSS selector
# chatgpt-web-crawler


## Known Limitations & Best Practices

### Browser Configuration
- Headless mode is not recommended as it frequently causes compatibility issues with ChatGPT's interface
- Use your default Chrome profile to:
   - Avoid login detection issues
   - Prevent bot detection mechanisms
   - Maintain existing session cookies
