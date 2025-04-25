import argparse
from chatgpt_selenium.chatgpt_automation import ChatGPTAutomation
# import config
from loguru import logger
import pandas as pd


parser = argparse.ArgumentParser(description="ChatGPT automation script")
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
        bot = ChatGPTAutomation(debug_port=9223)
        df = pd.read_csv(args.csv_file)
        records = df.to_dict(orient="records")
        response = bot.collect_responses(records)
        output_file = args.csv_file.replace(".csv", "_response.csv")
        df = pd.DataFrame(response)

        df = df[["user", "assistant", "link"]]
        df.to_csv(
            output_file,
            index=False,
        )
        logger.success(f"Successfully processed {len(response)} conversations")
        logger.info(f'Output saved to {output_file}')

    except Exception as e:
        import traceback

        traceback.print_exc()
        logger.critical(f"Fatal error in main execution: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
