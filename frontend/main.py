from frontend.ui import ui
from dotenv import load_dotenv
import os
import logging

load_dotenv()

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
    ui().launch(server_name=os.getenv("FRONTEND_HOST"), server_port=int(os.getenv("FRONTEND_PORT")))


if __name__ == "__main__":
    main()