import logging


log_file_path = "app.log"


def setup_logger(app):
    # Configure logging to a file

    handler = logging.FileHandler(log_file_path)
    handler.setLevel(logging.INFO)  # Set the desired logging level

    # Create a formatter and set it for the handler
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(funcName)s - [L%(lineno)d]- %(message)s"
    )
    handler.setFormatter(formatter)

    # attach handler to app.logger
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)  # Set the desired logging level

    return app.logger


from datetime import datetime, time


def check_time_now_to_reset_log_file():
    current_time = datetime.now().time()
    target_time = time(23, 0, 0)
    if current_time > target_time:
        with open(log_file_path, "w"):
            print("Empty this file", log_file_path)
            pass
