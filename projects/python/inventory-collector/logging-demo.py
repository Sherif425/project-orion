import logging

logging.basicConfig(level=logging.INFO)
logging.debug("Debug message")
logging.info("Inventory started")
logging.warning("using default configuration")
logging.error("Cannot write inventory")
logging.critical("Application terminated")