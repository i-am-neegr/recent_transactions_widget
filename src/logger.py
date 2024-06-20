import logging


def setup_logging():
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler()
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    return logger
