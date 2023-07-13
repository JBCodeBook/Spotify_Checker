import logging

def configure_logger():
    # Create a logger specific to your module or application
    logger = logging.getLogger("my_logger")

    # Set the logger level to DEBUG
    logger.setLevel(logging.DEBUG)

    # Create a file handler to write log messages to a file
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler to display log messages in the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Set the log message format
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the file handler and console handler to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create the logger instance
logger = configure_logger()
