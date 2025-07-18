# external imports
import logging
import sys
from os import getenv

# internal imports

def setup_logger():
    logger_created = logging.getLogger('hunter')

    # Avoid handlers duplication
    if not logger_created.handlers:
        # Set looger level with environment
        logger_created.setLevel(getenv("LOG_LEVEL", "INFO"))

        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s'
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        logger_created.addHandler(console_handler)

    return logger_created

# Crear logger global
logger = setup_logger()
