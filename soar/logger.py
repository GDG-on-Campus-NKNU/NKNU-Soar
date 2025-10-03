import logging


def setup_logger(write_log_to_disk=False, log_file="app.log"):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if write_log_to_disk:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)

            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
