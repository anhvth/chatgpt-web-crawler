import argparse
from chatgpt_selenium.chatgpt_automation import ChatGPTAutomation

# import config
from loguru import logger
import pandas as pd


parser = argparse.ArgumentParser(description="ChatGPT automation script")
parser.add_argument(
    "csv_file",
    type=str,
    default="/tmp/messages.csv",
    help="Path to the CSV file with messages",
)
parser.add_argument(
    "--collect-data",
    "-cl",
    action="store_true",
    help="Collect data from ChatGPT conversations",
)
parser.add_argument(
    "--project-url", "-p", type=str, help="URL of the ChatGPT project", required=True
)
args = parser.parse_args()


def helper():
    print(
        "you must start /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome  --remote-debugging-port=9223 --user-data-dir=.cache/user_example2"
    )
    print("after that you can run this script")


def main():
    """Main execution flow."""
    logger.info("Starting ChatGPT automation")

    # try:
    # Initialize automation with debug port from config
    bot = ChatGPTAutomation()

    # Process conversations and export data
    df = pd.read_csv(args.csv_file)
    assert "messages" in df.columns, "Column 'messages' not found in CSV file"
    MESSAGE_LIST = df["messages"].tolist()
    conversation_data = bot.send_messages(
        base_url=args.project_url, messages=MESSAGE_LIST
    )
    # Save results with metadata
    df = pd.DataFrame(conversation_data)
    outfile = args.csv_file.replace(".csv", "_submited.csv")
    df.to_csv(
        outfile,
        index=False,
        encoding="utf-8-sig",
    )
    logger.success(f"Successfully processed {len(conversation_data)} conversations\n{outfile}")


    return 0


if __name__ == "__main__":
    raise SystemExit(main())
