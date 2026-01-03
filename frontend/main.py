from frontend.ui import ui

import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, 
    # time in a human-readable format, the severity of the message, and the message content
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(), # display the logs in the console
        logging.FileHandler("frontend.log") # saves the logs into a file
    ]
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting the Multimodal Search UI...")
    ui().launch()


if __name__ == "__main__":
    main()