import logging


def init_logger(dunder_name, testing_mode, output_log_file) -> logging.Logger:
    log_format = "%(asctime)s - " "%(levelname)s - " "%(message)s"
    logger = logging.getLogger(dunder_name)

    if testing_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if output_log_file is True:
        # Output full log
        fh = logging.FileHandler("app.log")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(log_format)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Output warning log
        fh = logging.FileHandler("app.warning.log")
        fh.setLevel(logging.WARNING)
        formatter = logging.Formatter(log_format)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Output error log
        fh = logging.FileHandler("app.error.log")
        fh.setLevel(logging.ERROR)
        formatter = logging.Formatter(log_format)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
