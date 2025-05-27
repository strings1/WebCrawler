import logging

def get_logger(name):
    """
    Returns a logger with the specified name. If no handlers are set, it adds a StreamHandler with a basic formatter.
    Args:
        name (str): The name of the logger.
    Returns:
        logging.Logger: A logger instance with a StreamHandler and a basic formatter.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger
