import argparse
from chatgpt_selenium.chatgpt_automation import ChatGPTAutomation
import config
from loguru import logger
import pandas as pd


parser = argparse.ArgumentParser(description="ChatGPT automation script")
parser.add_argument(
    "--collect-data",
    action="store_true",
    help="Collect data from ChatGPT conversations",
)
parser.add_argument(
    "--csv-file",
    type=str,
    default="data/messages.csv",
    help="Path to the CSV file with messages",
)
args = parser.parse_args()

def main():
    """Main execution flow."""
    logger.info("Starting ChatGPT automation")

    try:
        # Initialize automation with debug port from config
        bot = ChatGPTAutomation(debug_port=config.DEBUG_PORT)

        # Process conversations and export data
        conversation_data = bot.send_messages(
            base_url=config.PROJECT_URL, messages=config.MESSAGE_LIST
        )

        # Save results with metadata
        df = pd.DataFrame(conversation_data)
        df.to_csv(
            config.OUTPUT_FILE,
            index=False,
            encoding="utf-8-sig",
            date_format="%Y-%m-%d %H:%M:%S",
        )
        logger.success(f"Successfully processed {len(conversation_data)} conversations")
    except Exception as e:
        import traceback

        traceback.print_exc()
        logger.critical(f"Fatal error in main execution: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
